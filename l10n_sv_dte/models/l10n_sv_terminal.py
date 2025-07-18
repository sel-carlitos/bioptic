from odoo import _, api, fields, models
from odoo.exceptions import UserError


class SVTerminal(models.Model):
    _name = 'l10n_sv.terminal'
    _description = 'Terminal o punto de venta que pertenece a una Sucursal'

    name = fields.Char(string='Terminal', required=True, copy=False)
    code = fields.Char(required=True, size=4, copy=False)
    location_id = fields.Many2one('l10n_sv.location', string='Sucursal', required=True, copy=False)
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)

    # Tipos de secuencia para las facturas
    sequence_fe = fields.Many2one('ir.sequence', string='Factura electrónica')
    sequence_ccfe = fields.Many2one('ir.sequence', string='Comprobante de Crédito Fiscal Electrónico')
    sequence_nre = fields.Many2one('ir.sequence', string='Nota de Remisión Electrónica')
    sequence_nce = fields.Many2one('ir.sequence', string='Nota de crédito electrónica')
    sequence_nde = fields.Many2one('ir.sequence', string='Nota de débito electrónica')
    sequence_fex = fields.Many2one('ir.sequence', string='Factura electrónica de exportación')
    sequence_fsee = fields.Many2one('ir.sequence', string='Factura Sujeto Excluido Electrónico')
    sequence_cde = fields.Many2one('ir.sequence', string='Comprobante de Donación Electrónica')
    sequence_cre = fields.Many2one('ir.sequence', string='Comprobante de Retencion Electronico')

    _sql_constraints = [
        ('code_uniq', 'unique(code, company_id, location_id)', 'Código único por Sucursal y Compañía!'),
    ]

    state = fields.Selection(
        [
            ('draft', 'Draft'),
            ('active', 'Active'),
            ('cancelled', 'Cancelled'),
        ],
        default='draft',
        copy=False,
    )

    def action_confirm(self):
        for rec in self:
            location = self.env['l10n_sv.location'].browse(rec.location_id.id)
            vals = {'code': rec.code}
            rec.sequence_fe = self._create_sequence(
                name='Factura electrónica', code='01', pref='fe', vals=vals, location=location
            ).id
            rec.sequence_ccfe = self._create_sequence(
                name='Comprobante de Crédito Fiscal Electrónico', code='03', pref='ccfe', vals=vals, location=location
            ).id
            rec.sequence_nre = self._create_sequence(
                name='Nota de Remisión Electrónica', code='04', pref='nre', vals=vals, location=location
            ).id
            rec.sequence_nce = self._create_sequence(
                name='Nota de Crédito Electrónica', code='05', pref='nce', vals=vals, location=location
            ).id
            rec.sequence_nde = self._create_sequence(
                name='Nota de Débito Electrónica', code='06', pref='nde', vals=vals, location=location
            ).id
            rec.sequence_cre = self._create_sequence(
                name='Comprobante de Retencion Electrónico', code='07', pref='cre', vals=vals, location=location
            ).id
            rec.sequence_fex = self._create_sequence(
                name='Factura electrónica de exportación', code='11', pref='fee', vals=vals, location=location
            ).id
            rec.sequence_fsee = self._create_sequence(
                name='Factura Sujeto Excluido Electrónico', code='14', pref='fsee', vals=vals, location=location
            ).id
            rec.sequence_cde = self._create_sequence(
                name='Comprobante de Donación Electrónica', code='15', pref='cde', vals=vals, location=location
            ).id
            rec.state = 'active'

    @api.model
    def _get_sequence_code(self, code, pref, vals, location):
        sequence_code = '%s_%s_%s_%s' % (pref, location.code, vals['code'], code)
        return sequence_code

    @api.model
    def _create_sequence(self, name=None, code=None, pref=None, vals={}, location=None):
        code = self._get_sequence_code(code, pref, vals, location)
        seq = {
            'name': name or 'Sequence',
            'code': code,
            'implementation': 'no_gap',
            'padding': 15,
            'number_next': 1,
            'number_increment': 1,
            'use_date_range': False,
            'company_id': self.company_id.id,
        }
        seq = self.env['ir.sequence'].create(seq)
        return seq

    def action_cancel(self):
        self.ensure_one()
        msg = _('Are you sure want to cancel this Terminal? Once you cancel this Terminal cannot be used.')
        action = self.env.ref('l10n_sv_dte.l10n_sv_terminal_validate_wizard_action').read()[0]
        action['context'] = {
            'default_name': msg,
            'default_terminal_id': self.id,
            'action': 'cancel',
        }
        return action

    def action_view_sequence(self):
        self.ensure_one()
        action = self.env.ref('base.ir_sequence_form').read()[0]
        domain = [
            self.sequence_fe.id,
            self.sequence_nre.id,
            self.sequence_nde.id,
            self.sequence_nce.id,
            self.sequence_ccfe.id,
            self.sequence_fex.id,
            self.sequence_fsee.id,
            self.sequence_cde.id,
            self.sequence_cre.id,
        ]
        if domain:
            action['views'] = [
                (self.env.ref('base.sequence_view_tree').id, 'list'),
                (self.env.ref('base.sequence_view').id, 'form'),
            ]
            action['domain'] = [('id', 'in', domain)]
        else:
            action = {'type': 'ir.actions.act_window_close'}

        return action

    def gen_control_number(self, voucher_type_id):
        sequence = {
            '01': self.sequence_fe,
            '03': self.sequence_ccfe,
            '04': self.sequence_nre,
            '05': self.sequence_nce,
            '06': self.sequence_nde,
            '07': self.sequence_cre,
            '11': self.sequence_fex,
            '14': self.sequence_fsee,
            '15': self.sequence_cde,
        }
        if voucher_type_id.code in sequence:
            seq = sequence[voucher_type_id.code]
            if not seq:
                raise UserError(_('The voucher type has no defined sequence.'))

        try:
            consecutive = 'DTE-%s-%s%s-%s' % (
                voucher_type_id.code,
                self.location_id.code,
                self.code,
                sequence[voucher_type_id.code].next_by_id(),
            )
        except Exception as e:
            raise UserError('Error al obtener Numeración Consecutiva: \n %s' % e)
        return consecutive
