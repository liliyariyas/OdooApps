/** @odoo-module */

import { KanbanRecord } from '@web/views/kanban/kanban_record';

export class CatelogProductKanbanRecord extends KanbanRecord {
    onGlobalClick(ev) {
        if (ev.target.closest('.o_catelog_product_quantity')) {
            return;
        }
        const { openAction, fieldNodes } = this.props.archInfo;
        const { catelog_quantity } = fieldNodes;
        if (openAction && ['catelog_add_quantity', 'catelog_remove_quantity'].includes(openAction.action) && catelog_quantity && catelog_quantity.widget === 'catelog_product_quantity') {
            let fsmProductQty = this.props.record.data.catelog_quantity;
            if (openAction.action === 'catelog_add_quantity') {
                fsmProductQty++;
            } else {
                fsmProductQty--;
            }
            this.props.record.update({ catelog_quantity: fsmProductQty })
            return;
        }
        return super.onGlobalClick(ev);
    }
}
