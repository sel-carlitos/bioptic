/** @odoo-module */

import { PartnerLine } from "@point_of_sale/app/screens/partner_list/partner_line/partner_line";
import { patch } from "@web/core/utils/patch";

patch(PartnerLine.prototype, {
    setup() {
        super.setup(...arguments);
//        console.log(this);
    },
});
