import {
    formatDate,
    deserializeDateTime
} from "@web/core/l10n/dates";
import { PosStore } from "@point_of_sale/app/store/pos_store";
import { patch } from "@web/core/utils/patch";

patch(PosStore.prototype, {
    async setup() {
        await super.setup(...arguments);
    },
    is_sv_country() {
        return this.company.country_id?.code == "SV";
    },
    getReceiptHeaderData(order) {
        const result = super.getReceiptHeaderData(...arguments);
        if (!this.is_sv_country() || !order) {
            return result;
        }
        result.l10n_sv_generation_code = order.l10n_sv_generation_code;
        result.l10n_sv_document_number = order.l10n_sv_document_number;
        result.l10n_sv_voucher_type_name = order.l10n_sv_voucher_type_id.name;
        result.origin_dte = order.origin_dte;
        result.partner = order.get_partner();
        return result;
    },
});

