from odoo import fields, models
from odoo.exceptions import UserError


class L10nSvApplyRuleWizard(models.TransientModel):
    _name = "l10n_sv.apply.rule.wizard"
    _description = "Wizard: aplicar regla l10n_sv a movimientos existentes"

    rule_id = fields.Many2one("l10n_sv.tag.rule", required=True)
    company_id = fields.Many2one(
        "res.company",
        default=lambda s: s.env.company,
    )
    date_from = fields.Date()
    date_to = fields.Date()
    journal_ids = fields.Many2many("account.journal")
    move_state = fields.Selection(
        [
            ("draft", "Draft"),
            ("posted", "Posted"),
        ],
        default="posted",
    )

    def action_apply(self):
        Move = self.env["account.move"]
        domain = [("company_id", "=", self.company_id.id)]
        if self.date_from:
            domain.append(("invoice_date", ">=", self.date_from))
        if self.date_to:
            domain.append(("invoice_date", "<=", self.date_to))
        if self.journal_ids:
            domain.append(("journal_id", "in", self.journal_ids.ids))
        if self.move_state:
            domain.append(("state", "=", self.move_state))
        moves = Move.search(domain)
        if not moves:
            raise UserError("No se encontraron movimientos para los filtros indicados.")
        moves.apply_l10n_sv_rules_to_moves(moves, rules=self.rule_id, batch_size=500)
        return {"type": "ir.actions.act_window_close"}
