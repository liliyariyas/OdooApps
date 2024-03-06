from ast import literal_eval
from collections import defaultdict

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.osv import expression


class SaleOrder(models.Model):
    _inherit = "sale.order"


    def action_view_material(self):

        self = self.with_company(self.company_id)

  

        kanban_view = self.env.ref('sale_catelog.view_product_product_kanban_material_catelog')
        search_view = self.env.ref('sale_catelog.product_search_form_view_inherit_catelog_sale')
        return {
            'type': 'ir.actions.act_window',
            'name': _('Choose Products'),
            'res_model': 'product.product',
            'views': [(kanban_view.id, 'kanban'), (False, 'form')],
            'search_view_id': [search_view.id, 'search'],
        
            'context': {
                'fsm_mode': True,
                'create': self.env['product.template'].check_access_rights('create', raise_exception=False),
                'catalog_sale_id': self.id,  # avoid 'default_' context key as we are going to create SOL with this context
               # 'pricelist': self.partner_id.property_product_pricelist.id,
                'hide_qty_buttons': self.sudo().state == 'done',
                #'default_invoice_policy': 'delivery',
            },
            'help': _("""<p class="o_view_nocontent_smiling_face">
                            No products found. Let's create one!
                        </p><p>
                            Keep track of the products you are using to complete your tasks, and invoice your customers for the goods.
                            Tip: using kits, you can add multiple products at once.
                        </p><p>
                            When your task is marked as done, your stock will be updated automatically. Simply choose a warehouse
                            in your profile from where to draw stock.
                        </p>""")
        }
