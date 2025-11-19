# -*- coding: utf-8 -*-
{
    "name": "l10n_sv - Dynamic tax tag rule",
    "version": "1.0.0",
    "summary": "Reglas dinámicas para asignar tax tags a account.move.line (l10n_sv)",
    "category": "Localization/Account",
    "author": "Sistemas-en-linea",
    "license": "LGPL-3",
    "depends": ["account"],
    "data": [
        "security/ir.model.access.csv",
        "wizard/wizard_apply_rule_views.xml",
        "views/account_tax.xml",
        "views/l10n_sv_tag_rule_views.xml",
    ],
    "installable": True,
    "application": False,
}
