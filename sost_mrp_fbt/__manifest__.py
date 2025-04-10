# -*- coding: utf-8 -*-
{
	'name': "MRP Quantities and Suppliers",
	'category': 'MRP Quantities and Suppliers',
	'version': '18.0.1.0.0',
	'depends': ['mrp', 'product'],
	'data': [
		'security/ir.model.access.csv',
		'views/product_template.xml',
		'views/mrp_production_views.xml',
		'views/res_partner.xml',
		'views/stock_warehouse.xml',
		'wizard/bom_wizard.xml',
	],
	'license': 'LGPL-3',
}
