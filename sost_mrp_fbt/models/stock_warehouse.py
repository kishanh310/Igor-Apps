from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = "stock.warehouse"

    show_in_mrp = fields.Boolean(string="Show In MRP", copy=False)

    @api.onchange('show_in_mrp')
    def onchange_show_in_mrp(self):
    	if self.show_in_mrp:
    		self.create_dynamic_fields()
    	else:
    		self.delete_dynamic_fields()

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
                    warehouse_field = self.env['ir.model.fields'].sudo().create({'name': field_name.lower(),
                                                                                 'field_description': field_name[2:].replace('_', ' ').title(),
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
            for suffix in ['onhand_qty', 'free_qty']:
                warehouse_code = warehouse_id.code.replace(' ', '_')
                field_name = f"x_{warehouse_code.lower()}_{suffix}"
                view_name = 'bom.line%s' % field_name
                existing_field = self.env['ir.model.fields'].search([
                    ('name', '=', field_name),
                    ('model', '=', 'bom.wizard.line'),
                ], limit=1)
                view_id = self.env['ir.ui.view'].sudo().search([('name', '=', view_name)])
                view_id.sudo().unlink()
                existing_field.sudo().unlink()
