import { PaymentScreen } from "@point_of_sale/app/screens/payment_screen/payment_screen";
import { patch } from "@web/core/utils/patch";
import { _t } from "@web/core/l10n/translation";
import { AlertDialog } from "@web/core/confirmation_dialog/confirmation_dialog";

patch(PaymentScreen.prototype, {
    async validateOrder(isForceValidate) {
        const order = this.currentOrder;
        const partner = order.get_partner();
        const amount_total = order.get_total_with_tax();
//        if (amount_total == 0){
//            order.set_to_invoice(false);
//        }

        if (partner && order.is_sv_country() && order.invoice_type == 'consumo'){
            if (amount_total >= 25000){
                let partner = this.currentOrder.get_partner()
                if (!partner.l10n_sv_identification_id) {
                    this.dialog.add(AlertDialog, {
                        title: _t("Validation Error"),
                        body: _t("If the invoice amount is greater than $25,000.00 the customer should have a VAT and Identification Type to validate the invoice."),
                    });
                    return;
                }
            }
        }

        return await super.validateOrder(...arguments);
    },
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
        if (this.pos.is_sv_country()) {
            return this.currentOrder.isFactura();
        }
        return this.currentOrder.is_to_invoice();
    },
});
