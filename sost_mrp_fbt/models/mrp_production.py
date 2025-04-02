# -*- coding: utf-8 -*-

import math
from odoo import api, fields, models, _


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    def button_add_bom(self):
        self.ensure_one()
        picking_type_id = self._context.get('default_picking_type_id')
        picking_type = picking_type_id and self.env['stock.picking.type'].browse(picking_type_id)
        bom_ids = self.env['mrp.bom'].search([('product_tmpl_id', '=', self.product_id.product_tmpl_id.id)])
        bom_dict = {}
        for bom_id in bom_ids:
            for component in bom_id.bom_line_ids:
                if component.product_id.main_compoment:
                   bom_dict.update({bom_id.id: component.product_id.id})

        return {
            'type': 'ir.actions.act_window',
            'name': 'Select BoM',
            'res_model': 'bom.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_mrp_id': self.id,
                'default_line_ids': [(0, 0, {'product_id': product, 'bom_id': bom}) for bom, product in bom_dict.items()],
            },
        }

    def button_recalculate_qty(self):
        if not self.move_raw_ids:
            return  

        if self.move_raw_ids and self.move_raw_ids.filtered(lambda x:x.product_id.main_compoment):
        
            component_id = False

            for component in self.move_raw_ids:
                if component.product_id.main_compoment:
                    component_id = component
                    break

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


class MrpBom(models.Model):
    _inherit = 'mrp.bom'

    supplier_code = fields.Integer(string="Supplier Code", copy=False)

    def update_supliier_code(self):
        main_component = self.bom_line_ids.filtered(lambda line: line.product_id.main_compoment)
        if main_component and main_component[0].product_id.supplier_code:
            self.supplier_code = main_component[0].product_id.supplier_code

    
    def write(self, vals):
        res = super(MrpBom, self).write(vals)
        if 'bom_line_ids' in vals:
            for bom in self:
                bom.supplier_code = 0
                bom.update_supliier_code()
        return res

    @api.model
    def create(self, vals):
        res = super(MrpBom, self).create(vals)
        res.update_supliier_code()
        return res

