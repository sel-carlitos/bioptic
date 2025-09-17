from odoo import _, api, fields, models
from odoo.exceptions import UserError


class L10nSvLocation(models.Model):
    _name = "l10n_sv.location"
    _description = "Sucursal de la empresa"

    name = fields.Char(string="Sucursal", required=True, copy=False)
    description = fields.Char(help="Nombre comercial en caso que difiera del nombre real.", copy=False)
    code = fields.Char(required=True, help="M001 para Sede Principal, S002 para Primera Tienda, etc.", size=4, copy=False)
    company_id = fields.Many2one('res.company', string="Company", default=lambda self: self.env.company)
    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("active", "Active"),
            ("cancelled", "Cancelled"),
        ],
        default="draft",
        copy=False,
    )

    # Tipos de secuencia para las facturas
    sequence_fe = fields.Many2one('ir.sequence', string="Factura electrónica")
    sequence_ccfe = fields.Many2one('ir.sequence', string="Comprobante de Crédito Fiscal Electrónico")
    sequence_nre = fields.Many2one('ir.sequence', string="Nota de Remisión Electrónica")
    sequence_nce = fields.Many2one('ir.sequence', string="Nota de crédito electrónica")
    sequence_nde = fields.Many2one('ir.sequence', string="Nota de débito electrónica")
    sequence_fex = fields.Many2one('ir.sequence', string="Factura electrónica de exportación")
    sequence_fsee = fields.Many2one('ir.sequence', string="Factura Sujeto Excluido Electrónico")
    sequence_cde = fields.Many2one('ir.sequence', string="Comprobante de Donación Electrónica")
    sequence_cre = fields.Many2one('ir.sequence', string="Comprobante de Retencion Electronico")

    _sql_constraints = [
        ('code_uniq', 'unique(code, company_id)', 'Código único por Compañia!'),
    ]

    def action_confirm(self):
        for location in self:
            terminal_vals = {"sequence_fe": self._create_sequence(name="Factura electrónica", code="01",
                                                                  pref="fe", location=location).id,
                             "sequence_ccfe": self._create_sequence(name="Comprobante de Crédito Fiscal Electrónico", code="03",
                                                                    pref="ccfe", location=location).id,
                             "sequence_nre": self._create_sequence(name="Nota de Remisión Electrónica", code="04",
                                                                   pref="nre", location=location).id,
                             "sequence_nce": self._create_sequence(name="Nota de Crédito Electrónica", code="05",
                                                                   pref="nce", location=location).id,
                             "sequence_nde": self._create_sequence(name="Nota de Débito Electrónica", code="06",
                                                                   pref="nde", location=location).id,
                             "sequence_cre": self._create_sequence(name="Comprobante de Retencion Electronico", code="07",
                                                                   pref="cre", location=location).id,
                             "sequence_fex": self._create_sequence(name="Factura electrónica de exportación", code="11",
                                                                   pref="fex", location=location).id,
                             "sequence_fsee": self._create_sequence(name="Factura Sujeto Excluido Electrónico", code="14",
                                                                    pref="fsee", location=location).id,
                             "sequence_cde": self._create_sequence(name="Comprobante de Donación Electrónica", code="15",
                                                                   pref="cde", location=location).id,
                             "state": "active",
                             }
            location.write(terminal_vals)

    @api.model
    def _get_sequence_code(self, pref, location, code):
        sequence_code = "%s_%s_%s" % (pref, location.code, code)
        return sequence_code

    @api.model
    def _create_sequence(self, name=None, code=None, pref=None, location=None):
        code = self._get_sequence_code(pref, location, code)
        seq = {
            'name': name or 'Sequence',
            'code': code,
            'implementation': 'no_gap',
            'padding': 15,
            'number_next': 1,
            'number_increment': 1,
            'use_date_range': False,
            'company_id': self.company_id.id
        }
        seq = self.env['ir.sequence'].create(seq)
        return seq

    def _action_cancel(self):
        for rec in self:
            rec.state = "cancelled"
            if rec.sequence_fe:
                rec.sequence_fe.active = False
            if rec.sequence_ccfe:
                rec.sequence_ccfe.active = False
            if rec.sequence_nre:
                rec.sequence_nre.active = False
            if rec.sequence_nce:
                rec.sequence_nce.active = False
            if rec.sequence_nde:
                rec.sequence_nde.active = False
            if rec.sequence_cre:
                rec.sequence_cre.active = False
            if rec.sequence_fex:
                rec.sequence_fex.active = False
            if rec.sequence_fsee:
                rec.sequence_fsee.active = False
            if rec.sequence_cde:
                rec.sequence_cde.active = False

            # Cancelar todas las terminales asociadas
            terminals = self.env["l10n_sv.terminal"].search([('location_id', '=', rec.id)])
            terminals.write({"state": "cancelled"})

    def action_cancel(self):
        self.ensure_one()

        msg = _(
            "Are you sure want to cancel this Location? " "Once you cancel this Location cannot be used."
        )
        action = self.env.ref("l10n_sv_dte.l10n_sv_terminal_validate_wizard_action").read()[0]
        action["context"] = {
            "default_name": msg,
            "default_location_id": self.id,
            "action": "cancel",
        }
        return action

    def action_view_sequence(self):
        self.ensure_one()
        action = self.env.ref("base.ir_sequence_form").read()[0]
        domain = [self.sequence_fe.id,  self.sequence_nre.id, self.sequence_nde.id, self.sequence_nce.id,
                  self.sequence_ccfe.id, self.sequence_fex.id, self.sequence_fsee.id, self.sequence_cde.id,
                  self.sequence_cre.id]
        if domain:
            action["views"] = [(self.env.ref("base.sequence_view_tree").id, "list"),
                               (self.env.ref("base.sequence_view").id, "form")]
            action["domain"] = [('id', 'in', domain)]
        else:
            action = {"type": "ir.actions.act_window_close"}

        return action

    def gen_control_number(self, voucher_type_id, terminal_code=None):
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
                raise UserError(_("The voucher type has no defined sequence."))

        try:
            consecutive = "DTE-%s-%s%s-%s" % (
                voucher_type_id.code,
                self.code,
                terminal_code,
                sequence[voucher_type_id.code].next_by_id())
        except Exception as e:
            raise UserError(_("Error getting Consecutive Numbering: \n %s" % e))
        return consecutive
