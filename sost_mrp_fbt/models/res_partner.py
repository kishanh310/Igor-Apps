from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = "res.partner"

    supplier_code = fields.Integer(string="Supplier Code")
    is_supplier_code = fields.Boolean(
        string="Supplier Code Readonly", compute="_compute_supplier_code"
    )

    @api.depends('is_company', 'parent_id')
    def _compute_supplier_code(self):
        for partner in self:
            if partner.company_type == 'person' and partner.parent_id:
                partner.is_supplier_code = True
            else:
                partner.is_supplier_code = False


    @api.model
    def create(self, vals):
        if vals.get('parent_id'):
            parent = self.browse(vals['parent_id'])
            vals['supplier_code'] = parent.supplier_code
        return super().create(vals)

    def write(self, vals):
        if 'parent_id' in vals:
            parent = self.browse(vals['parent_id'])
            vals['supplier_code'] = parent.supplier_code
        if 'supplier_code' in vals:
            for child_id in self.child_ids:
                child_id.supplier_code = vals['supplier_code']
        return super().write(vals)
 