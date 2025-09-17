# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError


class SVTerminal(models.Model):
    _name = "l10n_sv.terminal"
    _description = "Terminal o punto de venta que pertenece a una Sucursal"

    name = fields.Char(string="Terminal", required=True, copy=False)
    code = fields.Char(required=True, size=4, copy=False, help="Ej: P001 para el primer punto de venta, P002 para el segundo, etc.")
    location_id = fields.Many2one('l10n_sv.location', string='Sucursal', required=True, copy=False)
    company_id = fields.Many2one('res.company', string="Company",
                                 default=lambda self: self.env.company)

    _sql_constraints = [
        ('code_uniq', 'unique(code, company_id, location_id)', 'Código único por Sucursal y Compañia!'),
    ]

    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("active", "Active"),
            ("cancelled", "Cancelled"),
        ],
        default="draft",
        copy=False,
    )

    def action_confirm(self):
        for rec in self:
            if rec.location_id.state == 'draft':
                rec.location_id.action_confirm()

            if rec.location_id.state == 'cancelled':
                raise UserError(_("The location must be active before confirming the terminal."))

            rec.write({"state": "active"})

    def action_cancel(self):
        self.ensure_one()
        msg = _(
            "Are you sure want to cancel this Terminal? " "Once you cancel this Terminal cannot be used."
        )
        action = self.env.ref("l10n_sv_dte.l10n_sv_terminal_validate_wizard_action").read()[0]
        action["context"] = {
            "default_name": msg,
            "default_terminal_id": self.id,
            "action": "cancel",
        }
        return action

    def _action_cancel(self):
        for rec in self:
            rec.state = "cancelled"

    def gen_control_number(self, voucher_type_id):
        if self.location_id.state != 'active':
            raise UserError(_(f"The terminal {self.name} has not location active."))
        return self.location_id.gen_control_number(voucher_type_id, self.code)
