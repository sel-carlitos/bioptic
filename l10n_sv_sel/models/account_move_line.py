from odoo import api, fields, models


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    tax_totals = fields.Binary(
        string='Line totals Totals',
        compute='_compute_tax_totals',
        help='Edit Tax amounts if you encounter rounding issues.',
        exportable=False,
    )

    @api.depends_context('lang')
    @api.depends(
        'currency_rate',
        'tax_base_amount',
        'tax_line_id',
        'price_total',
        'price_subtotal',
        'move_id.invoice_payment_term_id',
        'move_id.partner_id',
        'move_id.currency_id',
    )
    def _compute_tax_totals(self):
        """Computed field used for custom widget's rendering.
        Only set on invoices.
        """
        for line in self:
            if line.move_id.is_invoice(include_receipts=True):
                base_line = line._get_rounded_base_and_tax_lines()
                line.tax_totals = self.env['account.tax']._get_tax_totals_summary(
                    base_lines=[base_line],
                    currency=line.move_id.currency_id,
                    company=line.move_id.company_id,
                    cash_rounding=line.move_id.invoice_cash_rounding_id,
                )
                line.tax_totals['display_in_company_currency'] = (
                    line.company_id.display_invoice_tax_company_currency
                    and line.company_currency_id != line.currency_id
                    and line.tax_totals['has_tax_groups']
                    and line.is_sale_document(include_receipts=True)
                )
            else:
                # Non-invoice moves don't support that field (because of multicurrency: all lines of the invoice share the same currency)
                line.tax_totals = None

    def _get_rounded_base_and_tax_lines(self, round_from_tax_lines=True):
        """Similar to account.move._get_rounded_base_and_tax_lines but scoped for a move line.
        Returns the base and tax lines for the taxes computation from the current line's move.
        """
        self.ensure_one()
        AccountTax = self.env['account.tax']
        move = self.move_id

        # Base lines
        base_aml = self.filtered(lambda line: line.display_type == 'product')

        base_line = move._prepare_product_base_line_for_taxes_computation(base_aml)

        tax_lines = []
        if move.id:
            # Add tax details
            AccountTax._add_tax_details_in_base_line(base_line, move.company_id)

            # Tax lines
            tax_aml = self.filtered('tax_repartition_line_id')
            tax_lines = [move._prepare_tax_line_for_taxes_computation(tax_aml)]

            AccountTax._round_base_lines_tax_details(
                [base_line], move.company_id, tax_lines=tax_lines if round_from_tax_lines else []
            )
        else:
            # For moves not stored yet
            base_line += move._prepare_epd_base_lines_for_taxes_computation_from_base_lines(base_aml)
            AccountTax._add_tax_details_in_base_lines(base_line, move.company_id)
            AccountTax._round_base_lines_tax_details([base_line], move.company_id)

        return base_line
