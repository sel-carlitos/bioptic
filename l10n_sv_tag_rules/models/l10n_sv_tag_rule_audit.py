from odoo import fields, models


class L10nSvTagRuleAudit(models.Model):
    _name = "l10n_sv.tag.rule.audit"
    _description = "Auditoría de ejecuciones de reglas l10n_sv"
    _order = "create_date desc"

    rule_id = fields.Many2one(
        "l10n_sv.tag.rule",
        required=True,
        ondelete="cascade",
    )
    user_id = fields.Many2one(
        "res.users",
        default=lambda s: s.env.user,
        readonly=True,
    )
    move_count = fields.Integer()
    line_count = fields.Integer()
    note = fields.Text()
    state = fields.Selection(
        [
            ("success", "Éxito"),
            ("partial", "Parcial"),
            ("error", "Error"),
        ],
        default="success",
    )
    create_date = fields.Datetime(readonly=True)
