import { PosOrder } from "@point_of_sale/app/models/pos_order";
import { patch } from "@web/core/utils/patch";


patch(PosOrder.prototype, {
    setup(vals) {
        super.setup(...arguments);
        if (this.is_sv_country()) {
            this.to_invoice = vals.to_invoice === false ? vals.to_invoice : true;
            this.invoice_type = vals.invoice_type || "consumo";
        }

        if (!this.get_partner()) {
            let pos_default_partner = this.config.default_partner_id;
            if (pos_default_partner) {
                this.set_partner(pos_default_partner);

            }
        }
    },
    is_sv_country() {
        return this.company.country_id?.code === "SV";
    },
    is_to_invoice() {
        if (this.is_sv_country()) {
            return true;
        }
        return super.is_to_invoice(...arguments);
    },
    set_to_invoice(to_invoice) {
        if (this.is_sv_country()) {
            this.assert_editable();
            this.to_invoice = true;
        } else {
            super.set_to_invoice(...arguments);
        }
    },
    isFactura() {
        if (this.invoice_type == "consumo") {
            return false;
        }
        return true;
    },
    export_for_printing(baseUrl, headerData) {
        const result = super.export_for_printing(...arguments);
        if (!this.is_sv_country()){
            return result;
        }

//        if (this.get_partner()) {
//            result.partner = this.get_partner();
//        }
        result.origin_dte = this.origin_dte;
        result.QR_code = this.QR_code;
        return result;
    },
    wait_for_push_order() {
        var result = super.wait_for_push_order(...arguments);
        result = Boolean(result || this.is_sv_country());
        return result;
    },
});
