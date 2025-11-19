from odoo import api, fields, models, _
from odoo.tools.safe_eval import safe_eval
from odoo.exceptions import ValidationError

class L10nSvTagRule(models.Model):
    _name = "l10n_sv.tag.rule"
    _description = "Reglas dinámicas para asignar account.account.tag a account.move.line"
    _order = "sequence, id"

    name = fields.Char(required=True)
    active = fields.Boolean(default=True)
    sequence = fields.Integer(default=10)
    company_id = fields.Many2one('res.company', default=lambda s: s.env.company, index=True)
    filter_domain = fields.Char(string="Dominio (ORM)", help="Dominio para account.move.line. Ej: [('move_id.move_type','=','out_invoice'), ('move_id.partner_id.country_id.code','=','SV')]")
    tag_ids = fields.Many2many('account.account.tag', string="Etiquetas a aplicar")
    apply_on_post = fields.Boolean("Aplicar al publicar", default=True)
    retroactive = fields.Boolean("Aplicable retroactivamente (botón)", default=True)
    apply_mode = fields.Selection([('append', 'Agregar'), ('replace', 'Reemplazar')], default='append')
    note = fields.Text()

    @api.constrains('filter_domain')
    def _check_filter_domain(self):
        for rec in self:
            if not rec.filter_domain:
                continue
            try:
                dom = safe_eval(rec.filter_domain)
                if not isinstance(dom, (list, tuple)):
                    raise ValidationError(_("El dominio debe evaluarse a lista/tupla."))
            except Exception as e:
                raise ValidationError(_("Dominio inválido: %s") % e)
