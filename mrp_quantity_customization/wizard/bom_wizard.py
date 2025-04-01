from odoo import models, fields, api
from odoo.exceptions import ValidationError


class BomWizard(models.TransientModel):
    _name = "bom.wizard"
    _description = "BoM Wizard"

    line_ids = fields.One2many("bom.wizard.line", "wizard_id", string="BoM Lines")
    mrp_id = fields.Many2one('mrp.production')

    def confirm_action(self):
        line_id = self.line_ids.filtered(lambda x: x.is_selected)
        if len(line_id) > 1:
            raise ValidationError('Please Select Only One product')

        self.mrp_id.bom_id = line_id.bom_id.id


class BomWizardLine(models.TransientModel):
    _name = "bom.wizard.line"
    _description = "BoM Wizard Line"

    wizard_id = fields.Many2one("bom.wizard", string="Wizard")
    product_id = fields.Many2one("product.product", string="Product")
    bom_id = fields.Many2one("mrp.bom", string="BOM")
    is_selected = fields.Boolean(string="Select") 


