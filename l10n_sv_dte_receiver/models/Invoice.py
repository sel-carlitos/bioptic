# -*- coding: utf-8 -*-


class Invoice:

    def __init__(self):
        self.lines = []

    def addLine(self, value):
        self.lines.append(value)

    def getLines(self): return self.lines


class InvoiceLine:

    def __init__(self, name=None, description=None, quantity=None, price=None, uom_id=None, total=None, tax_ids=None,
                 discount=0, product_id=None):
        self.name = name
        self.description = description
        self.quantity = quantity
        self.price = price
        self.uom_id = uom_id
        self.total = total
        self.taxs = tax_ids
        self.discount = discount
        self.product_id = product_id

    def getUomId(self):
        return self.uom_id

    def setUomId(self, uom_id):
        self.uom_id = uom_id

    def getProduct(self):
        return self.product_id

    def setProduct(self, product_id):
        self.product_id = product_id

    # def getTaxs(self):
    #     taxs = [tax.id for tax in self.taxs]
    #     return taxs

    def PrepareInvoiceLine(self):
        # vals = {'name': self.name, 'price_subtotal': self.total, 'quantity': self.quantity, 'price_unit': self.price,
        #         'discount': self.discount, 'discount_type_code': self.discount_type_code,
        #         'tax_ids': [(6, 0, self.getTaxs())]}
        vals = {'name': self.name, 'price_subtotal': self.total, 'quantity': self.quantity, 'price_unit': self.price,
                'discount': self.discount,
                'tax_ids': [(6, 0, self.taxs)]}

        if self.getProduct():
            vals['product_id'] = self.product_id

        if self.getUomId():
            vals['product_uom_id'] = self.uom_id

        return vals

    def PrepareDescuentosORecargosLine(self):
        vals = {
            'name': self.name,
            'quantity': self.quantity,
            'price_unit': self.price,
        }

        return vals

    def __str__(self):
        return '<InvoiceLine>: (name={}, quantity={}, price_unit={}, discount={}, price_subtotal={})'.format(self.name, self.quantity, self.price, self.discount, self.total)
