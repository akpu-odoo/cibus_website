# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    variable_weight = fields.Boolean(string="Variable Weight")

    def _get_combination_info(self, combination=False, product_id=False, add_qty=1.0, parent_combination=False, only_template=False):
        combination_info = super(ProductTemplate, self)._get_combination_info(combination, product_id, add_qty, parent_combination, only_template)
        combination_info['variable_weight'] = False
        if not self.env.context.get('uid'):
            combination_info['product_packaging_ids'] = []
            return combination_info
        
        product_id = self.env['product.product'].browse(combination_info.get('product_id'))
        combination_info['product_packaging_ids'] = []
        combination_info['variable_weight'] = product_id.variable_weight
        if product_id.packaging_ids:
            if not product_id.variable_weight:
                combination_info['product_packaging_ids'].append({
                    'id': False,
                    'name':"No packaging",
                    'qty': 1.0  
                })
            for rec in product_id.packaging_ids:
                combination_info['product_packaging_ids'].append({
                    'id': rec.id,
                    'name': rec.name,
                    'qty': rec.qty  
                })
        return combination_info