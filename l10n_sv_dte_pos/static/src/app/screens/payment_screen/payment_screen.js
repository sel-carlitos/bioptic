/** @odoo-module */

import { PaymentScreen } from "@point_of_sale/app/screens/payment_screen/payment_screen";
import { patch } from "@web/core/utils/patch";
import { _t } from "@web/core/l10n/translation";

patch(PaymentScreen.prototype, {
    toggleIsToInvoice() {
        if (this.pos.is_sv_country()) {
            if (this.currentOrder.invoice_type == "consumo") {
                this.currentOrder.invoice_type = "factura";
            } else {
                this.currentOrder.invoice_type = "consumo";
            }
            this.render(true);
        } else {
            super.toggleIsToInvoice(...arguments);
        }
    },
    highlightInvoiceButton() {
        console.log(this);
        if (this.pos.is_sv_country()) {
            return this.currentOrder.isFactura();
        }
        return this.currentOrder.is_to_invoice();
    },
});
