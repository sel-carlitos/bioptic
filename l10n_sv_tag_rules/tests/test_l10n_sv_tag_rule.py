from odoo.tests.common import TransactionCase
from odoo import fields

class TestL10nSvTagRule(TransactionCase):

    def setUp(self):
        super().setUp()
        self.Rule = self.env['l10n_sv.tag.rule']
        self.Move = self.env['account.move']
        self.Line = self.env['account.move.line']
        self.Tag = self.env['account.account.tag']

        # crear tag
        self.tag = self.Tag.create({'name': 'SV-TAX'})

        # crear partner y journal (suponiendo que existan al menos uno)
        country_sv = self.env['res.country'].search([('code', '=', 'SV')], limit=1)
        if not country_sv:
            country_sv = self.env['res.country'].create({'name':'El Salvador', 'code':'SV'})
        self.partner_sv = self.env['res.partner'].create({'name':'Cliente SV', 'country_id': country_sv.id})
        self.journal = self.env['account.journal'].search([], limit=1)

    def _create_invoice(self):
        move = self.Move.create({
            'move_type': 'out_invoice',
            'partner_id': self.partner_sv.id,
            'journal_id': self.journal.id,
            'invoice_date': fields.Date.context_today(self),
        })
        account = self.env['account.account'].search([], limit=1)
        if not account:
            account = self.env['account.account'].create({'name': 'Test', 'code': '9999', 'user_type_id': self.env.ref('account.data_account_type_revenue').id})
        self.Line.create({
            'move_id': move.id,
            'account_id': account.id,
            'name': 'Line test',
            'debit': 0.0,
            'credit': 100.0,
        })
        return move

    def test_apply_on_post_simple(self):
        rule = self.Rule.create({
            'name': 'Tag SV invoices',
            'filter_domain': "[(\'move_id.move_type\',\'=\', \'out_invoice\'), (\'move_id.partner_id.country_id.code\',\'=\', \'SV\')]",
            'tag_ids': [(4, self.tag.id)],
            'apply_on_post': True,
        })
        move = self._create_invoice()
        move.action_post()
        self.assertTrue(any(self.tag.id in line.tax_tag_ids.ids for line in move.line_ids))

    def test_apply_retroactive_button(self):
        rule = self.Rule.create({
            'name': 'Tag SV retro',
            'filter_domain': "[(\'move_id.move_type\',\'=\', \'out_invoice\'), (\'move_id.partner_id.country_id.code\',\'=\', \'SV\')]",
            'tag_ids': [(4, self.tag.id)],
            'apply_on_post': False,
            'retroactive': True,
        })
        move = self._create_invoice()
        self.assertFalse(any(self.tag.id in line.tax_tag_ids.ids for line in move.line_ids))
        self.env['account.move'].apply_l10n_sv_rules_to_moves(self.env['account.move'].browse([move.id]), rules=rule)
        self.assertTrue(any(self.tag.id in line.tax_tag_ids.ids for line in move.line_ids))
