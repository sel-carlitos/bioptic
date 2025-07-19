import { PaymentScreen } from "@point_of_sale/app/screens/payment_screen/payment_screen";
import { patch } from "@web/core/utils/patch";

patch(PaymentScreen.prototype, {

    shouldDownloadInvoice() {
        return this.pos.is_sv_country()
            ? this.pos.config.print_pdf
            : super.shouldDownloadInvoice();
    },
});
