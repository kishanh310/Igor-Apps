from odoo import models, fields, api
from odoo.exceptions import ValidationError

class BomWizard(models.TransientModel):
    _name = "bom.wizard"
    _description = "BoM Wizard"

    line_ids = fields.One2many("bom.wizard.line", "wizard_id", string="BoM Lines")
    mrp_id = fields.Many2one('mrp.production')

class BomWizardLine(models.TransientModel):
    _name = "bom.wizard.line"
    _description = "BoM Wizard Line"

    wizard_id = fields.Many2one("bom.wizard", string="Wizard")
    product_id = fields.Many2one("product.product", string="Product")
    bom_id = fields.Many2one("mrp.bom", string="BOM")
    is_selected = fields.Boolean(string="Select")
    product_uom = fields.Many2one(comodel_name='uom.uom', string="Unit of Measure", readonly=True)

    def confirm_action(self):
        self.wizard_id.mrp_id.bom_id = self.bom_id.id
        return {'type': 'ir.actions.act_window_close'}