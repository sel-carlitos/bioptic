def update_group_tax(env):
    """Update the tax group with the l10n_sv_code."""
    tax_group = env.ref('account.1_tax_group_13', raise_if_not_found=False)
    if tax_group:
        tax_group.l10n_sv_code = '20'
