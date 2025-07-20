from odoo import api, fields, models


class Partner(models.Model):
    _inherit = 'res.partner'

    res_municipality_id = fields.Many2one(
        'res.municipality',
        'Municipality',
        domain="[('state_id', '=', state_id)]",
    )

    @api.model
    def default_get(self, fields_list):
        """
        Overrides the default_get method to set default values for country
        and language when creating a new partner.
        """
        # Get default values from the parent class
        res = super().default_get(fields_list)

        # Set default country from the company's fiscal country
        company = self.env.company
        if company and company.account_fiscal_country_id:
            res['country_id'] = company.account_fiscal_country_id.id

        # Set default language from the current user's language setting
        # self.env.user references the current user's record
        if self.env.user.lang:
            res['lang'] = self.env.user.lang

        return res
