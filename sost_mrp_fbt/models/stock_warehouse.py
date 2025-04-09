from odoo import models, fields, api


class StockWarehouse(models.Model):
    _inherit = "stock.warehouse"

    show_in_mrp = fields.Boolean(string="Show In MRP")


    def write(self, vals):
        if 'code' in vals:
            self.delete_dynamic_fields()
        res = super(StockWarehouse, self).write(vals)
        if 'show_in_mrp' in vals:
            if vals.get('show_in_mrp'):
                self.create_dynamic_fields()
            else:
                self.delete_dynamic_fields()
        if 'code' in vals and self.show_in_mrp:
            self.create_dynamic_fields()
        return res

    def create_dynamic_fields(self):
        for warehouse_id in self:
            for suffix in ['onhand_qty', 'free_qty']:
                warehouse_code = warehouse_id.code.replace(' ', '_')
                field_name = f"x_{warehouse_code.lower()}_{suffix}"
                existing_field = self.env['ir.model.fields'].search([
                    ('name', '=', field_name),
                    ('model', '=', 'bom.wizard.line'),
                ], limit=1)
                if not existing_field:
                    label_suffix = 'Onhand' if suffix == 'onhand_qty' else 'Free'
                    field_description = f"{warehouse_id.code}/" + label_suffix
                    warehouse_field = self.env['ir.model.fields'].sudo().create({'name': field_name.lower(),
                                                                                 'field_description': field_description,
                                                                                 'model_id': self.env.ref('sost_mrp_fbt.model_bom_wizard_line').id,
                                                                                 'ttype': 'integer',
                                                                                 })

                    inherit_id = self.env.ref(
                        'sost_mrp_fbt.view_bom_wizard_form')
                    arch_base = f'''<?xml version="1.0"?>
                                  <data>
                                  <field name="bom_id" position="after">
                                  <field name="{warehouse_field.name}"/>
                                  </field>
                                  </data>'''

                    view_id = self.env['ir.ui.view'].sudo().create({'name': 'bom.line%s' % field_name,
                                                                    'type': 'form',
                                                                    'model': 'bom.wizard',
                                                                    'mode': 'extension',
                                                                    'inherit_id': inherit_id.id,
                                                                    'arch_base': arch_base,
                                                                    'active': True})

    def delete_dynamic_fields(self):
        for warehouse_id in self:
            if warehouse_id.code:
                for suffix in ['onhand_qty', 'free_qty']:
                    warehouse_code = warehouse_id.code.replace(' ', '_')
                    field_name = f"x_{warehouse_code.lower()}_{suffix}"
                    view_name = 'bom.line%s' % field_name
                    existing_field = self.env['ir.model.fields'].search([
                        ('name', '=', field_name),
                        ('model', '=', 'bom.wizard.line'),
                    ], limit=1)
                    view_id = self.env['ir.ui.view'].sudo().search(
                        [('name', '=', view_name)])
                    view_id.sudo().unlink()
                    existing_field.sudo().unlink()
