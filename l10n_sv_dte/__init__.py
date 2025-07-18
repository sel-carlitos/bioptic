from . import models
from . import wizard


def _l10n_sv_edi_post_init(env):
    for company in env['res.company'].search([('chart_template', '=', 'sv')]):
        Template = env['account.chart.template'].with_company(company)
        Template._load_data({'account.tax': Template._get_sv_edi_account_tax()})
        Template._load_data({'account.tax.group': Template._get_do_edi_account_tax_group()})
