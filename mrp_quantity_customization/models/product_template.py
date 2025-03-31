from odoo import models, fields, api

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    minimal_qty = fields.Integer('Minimal Qty', default=1)
    main_compoment = fields.Boolean()

    def write(self,vals):
        res = super(ProductTemplate,self).write(vals)
        for variant in self.product_variant_ids:
            if vals.get('minimal_qty'):
                variant.minimal_qty = vals.get('minimal_qty')
            if vals.get('main_compoment'):
                variant.main_compoment = vals.get('main_compoment')
        return res

class ProductProduct(models.Model):
    _inherit = 'product.product'

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
        
        return res