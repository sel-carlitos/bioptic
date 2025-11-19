from odoo import api, fields, models


class AccountAccountTag(models.Model):
    _inherit = "account.account.tag"

    code = fields.Char(string="Code")
    operation = fields.Selection(
        [
            ("+", "+"),
            ("-", "-"),
            ("=", "="),
            ("text", "Text"),
            ("compare", "Compare"),
            ("manual", "Manual"),
        ],
        string="Operation",
    )

    @api.depends("applicability", "country_id")
    @api.depends_context("company")
    def _compute_display_name(self):
        super()._compute_display_name()

        is_debug = True if self.env.user.has_group('base.group_no_one') else False

        for tag in self:
            if is_debug:
                if tag.code:
                    tag.display_name = f"{tag.name} [{tag.code}]"
                else:
                    tag.display_name = tag.name
            else:
                tag.display_name = tag.code or tag.name
