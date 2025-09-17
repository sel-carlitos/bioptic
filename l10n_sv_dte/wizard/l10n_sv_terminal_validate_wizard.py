# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class TerminalValidateWizard(models.TransientModel):
    """
    This Wizard purpose is to warn the user when attempt to change
    sequence state.
    """

    _name = "l10n_sv.terminal.validate_wizard"
    _description = "Terminal Validate Wizard"

    name = fields.Char()
    terminal_id = fields.Many2one("l10n_sv.terminal", string="Terminal")
    location_id = fields.Many2one("l10n_sv.location", string="Location")

    def confirm_cancel(self):
        self.ensure_one()
        if self.terminal_id:
            action = self._context.get("action", False)
            if action == "cancel":
                self.terminal_id._action_cancel()
            # if action == "confirm":
            #     self.terminal_id._action_confirm()
            # elif action == "cancel":
            #     self.terminal_id._action_cancel()
        elif self.location_id:
            action = self._context.get("action", False)
            if action == "cancel":
                self.location_id._action_cancel()
            # if action == "confirm":
            #     self.location_id._action_confirm()
            # elif action == "cancel":
            #     self.location_id._action_cancel()
        else:
            raise ValidationError(_("There is no terminal to perform this action."))
