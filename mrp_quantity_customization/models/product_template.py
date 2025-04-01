from odoo import models, fields, api, _

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    @api.model
    def _get_supplier_code(self):
        supplier_codes = self.env['res.partner'].search([('supplier_code', '!=', False)]).mapped('supplier_code')
        unique_codes = list(set(supplier_codes))
        selection_list = [(str(code), code) for code in unique_codes]
        return  [('new', 'new')] + selection_list

    supplier_code = fields.Selection(selection=lambda self: self._get_supplier_code(), string="Supplier Code", default='new')
    minimal_qty = fields.Integer('Minimal Qty', default=1)
    main_compoment = fields.Boolean()

    def write(self,vals):
        res = super(ProductTemplate,self).write(vals)
        for variant in self.product_variant_ids:
            if vals.get('minimal_qty'):
                variant.minimal_qty = vals.get('minimal_qty')
            if vals.get('main_compoment'):
                variant.main_compoment = vals.get('main_compoment')
            if vals.get('supplier_code'):
                variant.supplier_code = vals.get('supplier_code')
        return res

class ProductProduct(models.Model):
    _inherit = 'product.product'


    supplier_code = fields.Selection(selection=lambda self: self.product_tmpl_id._get_supplier_code(), string="Supplier Code")
    minimal_qty = fields.Integer(
        string="Minimal Qty",
        copy=True
    )
    main_compoment = fields.Boolean(copy=True)

    def create(self,vals):
        res = super(ProductProduct,self).create(vals)
        if res.product_tmpl_id:
            res.minimal_qty = res.product_tmpl_id.minimal_qty
            res.main_compoment = res.product_tmpl_id.main_compoment
            res.supplier_code = res.product_tmpl_id.supplier_code
        return res