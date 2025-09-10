import { TicketScreen } from "@point_of_sale/app/screens/ticket_screen/ticket_screen";
import { patch } from "@web/core/utils/patch";

patch(TicketScreen.prototype, {
    async onDoRefund() {
        //Este metodo es llamado al dar clik en Refund

        if (this.pos.is_sv_country()) {
            let order = this.getSelectedOrder();
            let partner = order.get_partner();
            const destinationOrder =
                this.props.destinationOrder &&
                this.props.destinationOrder.lines.every(
                    (l) =>
                        l.quantity >= 0 || order.lines.some((ol) => ol.id === l.refunded_orderline_id)
                ) &&
                partner === this.props.destinationOrder.get_partner() &&
                !this.pos.doNotAllowRefundAndSales()
                    ? this.props.destinationOrder
                    : this._getEmptyOrder(partner);

            if (destinationOrder){
                destinationOrder.set_partner(partner)
            }
        }

        await super.onDoRefund(...arguments);
    }
});
