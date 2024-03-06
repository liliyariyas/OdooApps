from collections import defaultdict

from odoo import _, api, fields, models
from odoo.tools import float_round


class ProductProduct(models.Model):
    _inherit = 'product.product'

    catelog_quantity = fields.Float('Catelog Quantity', compute="_compute_catelog_quantity", inverse="_inverse_catelog_quantity", search="_search_catelog_quantity")




    @api.depends_context('catalog_sale_id')
    def _compute_catelog_quantity(self):
        sale = self._get_contextual_catelog_sale()
 
        if sale:

            SaleOrderLine = self.env['sale.order.line']
            sale = sale.sudo()
            SaleOrderLine = SaleOrderLine.sudo()                
                

            products_qties = SaleOrderLine._read_group(
                [('id', 'in', sale.order_line.ids)],
                ['product_id', 'product_uom_qty'], ['product_id'])
                
            qty_dict = dict([(x['product_id'][0], x['product_uom_qty']) for x in products_qties if x['product_id']])
            for product in self:
                product.catelog_quantity = qty_dict.get(product.id, 0)
        else:
            self.catelog_quantity = False

    def _inverse_catelog_quantity(self):
        sale = self._get_contextual_catelog_sale()
        
      
        if sale:
            SaleOrderLine_sudo = self.env['sale.order.line'].sudo()
            sale_lines_read_group = SaleOrderLine_sudo._read_group([
                ('order_id', '=', sale.id),
                ('product_id', 'in', self.ids)],
                ['product_id', 'sequence', 'ids:array_agg(id)'],
                ['product_id', 'sequence'],
                lazy=False)
            sale_lines_per_product = defaultdict(lambda: self.env['sale.order.line'])
            for sol in sale_lines_read_group:
                sale_lines_per_product[sol['product_id'][0]] |= SaleOrderLine_sudo.browse(sol['ids'])
            for product in self:
                sale_lines = sale_lines_per_product.get(product.id, self.env['sale.order.line'])
                all_editable_lines = sale_lines.filtered(lambda l: l.qty_delivered == 0 or l.qty_delivered_method == 'manual' or l.state != 'done')
                diff_qty = product.catelog_quantity - sum(sale_lines.mapped('product_uom_qty'))
                if all_editable_lines:  # existing line: change ordered qty (and delivered, if delivered method)
                    if diff_qty > 0:
                        vals = {
                            'product_uom_qty': all_editable_lines[0].product_uom_qty + diff_qty,
                        }
                        if all_editable_lines[0].qty_delivered_method == 'manual':
                            vals['qty_delivered'] = all_editable_lines[0].product_uom_qty + diff_qty
                        all_editable_lines[0].with_context(catelog_no_message_post=True).write(vals)
                        continue
                    # diff_qty is negative, we remove the quantities from existing editable lines:
                    for line in all_editable_lines:
                        new_line_qty = max(0, line.product_uom_qty + diff_qty)
                        diff_qty += line.product_uom_qty - new_line_qty
                        vals = {
                            'product_uom_qty': new_line_qty
                        }
                        if line.qty_delivered_method == 'manual':
                            vals['qty_delivered'] = new_line_qty
                        line.with_context(catelog_no_message_post=True).write(vals)
                        if diff_qty == 0:
                            break
                            
                            
                elif diff_qty > 0:  # create new SOL
                
                
                    vals = {
                        'order_id': sale.id,
                        'product_id': product.id,
                        'product_uom_qty': diff_qty,
                        'product_uom': product.uom_id.id,
                    }
                    if product.service_type == 'manual':
                        vals['qty_delivered'] = diff_qty

                    sol = SaleOrderLine_sudo.create(vals)
                    if sale.pricelist_id.discount_policy != 'without_discount':
                        sol.discount = 0.0
                    if not sol.qty_delivered_method == 'manual':
                        sol.qty_delivered = 0

    @api.model
    def _search_catelog_quantity(self, operator, value):
        if not (isinstance(value, int) or (isinstance(value, bool) and value is False)):
            raise ValueError(_('Invalid value: %s', value))
        if operator not in ('=', '!=', '<=', '<', '>', '>=') or (operator == '!=' and value is False):
            raise ValueError(_('Invalid operator: %s', operator))

        sale = self._get_contextual_catelog_sale()
        if not sale:
            return []
        op = 'inselect'
        if value is False:
            value = 0
            operator = '>='
            op = 'not inselect'
        query = """
            SELECT sol.product_id
              FROM sale_order_line sol
         LEFT JOIN sale_order so
                ON sol.order_id = so.id
             WHERE 
               sol.product_uom_qty {} %s
        """.format(operator)
        return [('id', op, (query, (value)))]

    @api.model
    def _get_contextual_catelog_sale(self):
        sale_id = self.env.context.get('catalog_sale_id')
        if sale_id:
            return self.env['sale.order'].browse(sale_id)
        return self.env['sale.order']

    def set_catelog_quantity(self, quantity):
        sale = self._get_contextual_catelog_sale()
        # project user with no sale rights should be able to change material quantities
        if not sale or quantity and quantity < 0 : #or not self.user_has_groups('project.group_project_user'):
            return
        self = self.sudo()

        # don't add material on locked SO
        if sale.sudo().state == 'done':
            return False
   
        wizard_product_lot = self.action_assign_serial()
        if wizard_product_lot:
            return wizard_product_lot
        self.catelog_quantity = float_round(quantity, precision_rounding=self.uom_id.rounding)
        return True

    # Is override by fsm_stock to manage lot
    def action_assign_serial(self):
        return False

    def catelog_add_quantity(self):
        return self.set_catelog_quantity(self.sudo().catelog_quantity + 1)

    def catelog_remove_quantity(self):
        catelog_product_qty = self.sudo().catelog_quantity
        catelog_product_qty = catelog_product_qty - 1 if catelog_product_qty > 1 else 0
        return self.set_catelog_quantity(catelog_product_qty)
