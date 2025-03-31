# -*- coding: utf-8 -*-

import math
from odoo import fields, models, _


class MrpProduction(models.Model):
    _inherit = 'mrp.production'


    def button_recalculate_qty(self):
        if not self.move_raw_ids:
            return  

        if self.move_raw_ids and self.move_raw_ids.filtered(lambda x:x.product_id.main_compoment):
        
            component_id = False

            for component in self.move_raw_ids:
                if component.product_id.main_compoment:
                    component_id = component
                    continue

            main_component = component_id.product_id.main_compoment if component_id else False

            if main_component and component_id and component_id.product_id.minimal_qty > 0:
                product_uom_qty = component_id.product_uom_qty
                minimal_qty = component_id.product_id.minimal_qty
                qty_div = product_uom_qty / minimal_qty
                qty_trunk = math.trunc(qty_div)
                qty_min = qty_div - qty_trunk
                main_qty = 1 if qty_min > 0 else 0
                mo_qty = qty_trunk + main_qty
                product_qty = mo_qty * minimal_qty

                mo_qty = product_uom_qty / self.product_qty
                mo_main_qty =  math.trunc(product_qty / mo_qty)

                self.product_qty = mo_main_qty
                comp_id = self.move_raw_ids.filtered(lambda x:x.product_id.id == component_id.product_id.id)
                comp_id.write({'product_uom_qty':product_qty})