from odoo import api, models
from odoo.tools.safe_eval import safe_eval


class AccountMove(models.Model):
    _inherit = "account.move"

    @api.model
    def _eval_rule_domain(self, rule):
        if not rule.filter_domain:
            return []
        try:
            dom = safe_eval(rule.filter_domain)
            if not isinstance(dom, (list, tuple)):
                return []
            return list(dom)
        except Exception as e:
            # registrar en ir.logging para debugging
            try:
                self.env["ir.logging"].sudo().create(
                    {
                        "name": "l10n_sv.tag.rule domain eval error",
                        "type": "server",
                        "level": "ERROR",
                        "message": f"Error safe_eval rule {rule.id}: {e}",
                        "path": "l10n_sv.tag.rule._eval_rule_domain",
                    }
                )
            except Exception:
                # en entornos donde ir.logging no esté disponible, swallow
                pass
            return []

    @api.model
    def apply_l10n_sv_rules_to_moves(
        self, moves, rules=None, batch_size=1000, log_audit=True
    ):
        Rule = self.env["l10n_sv.tag.rule"]
        Line = self.env["account.move.line"]
        Audit = self.env["l10n_sv.tag.rule.audit"]

        if rules is None:
            company_ids = list(set(moves.mapped("company_id.id")))
            rules = Rule.search(
                [
                    ("active", "=", True),
                    "|",
                    ("company_id", "=", False),
                    ("company_id", "in", company_ids),
                ],
                order="sequence, id",
            )

        total_lines = 0
        for rule in rules:
            dom = self._eval_rule_domain(rule)
            search_dom = [("move_id", "in", moves.ids)] + dom
            offset = 0
            affected_lines = 0
            while True:
                lines = Line.search(search_dom, offset=offset, limit=batch_size)
                if not lines:
                    break
                if rule.apply_mode == "replace":
                    lines.write({"tax_tag_ids": [(6, 0, rule.tag_ids.ids)]})
                else:
                    for line in lines:
                        missing = [
                            t for t in rule.tag_ids.ids if t not in line.tax_tag_ids.ids
                        ]
                        if missing:
                            line.write({"tax_tag_ids": [(4, t) for t in missing]})
                affected_lines += len(lines)
                offset += batch_size
            total_lines += affected_lines
            if log_audit:
                try:
                    Audit.sudo().create(
                        {
                            "rule_id": rule.id,
                            "move_count": len(moves),
                            "line_count": affected_lines,
                            "note": f"Aplicado por usuario {self.env.user.id}",
                            "state": "success",
                        }
                    )
                except Exception:
                    pass
        return total_lines

    def action_post(self):
        moves = self.filtered(lambda m: True)
        rules = self.env["l10n_sv.tag.rule"].search(
            [
                ("apply_on_post", "=", True),
                ("active", "=", True),
                "|",
                ("company_id", "=", False),
                ("company_id", "in", moves.mapped("company_id.id")),
            ],
            order="sequence, id",
        )
        if rules:
            self.apply_l10n_sv_rules_to_moves(moves, rules=rules, batch_size=500)
        return super().action_post()
