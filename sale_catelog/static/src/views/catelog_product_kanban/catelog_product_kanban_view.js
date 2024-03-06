/** @odoo-module */

import { registry } from "@web/core/registry";
import { kanbanView } from '@web/views/kanban/kanban_view';
import { CatelogProductKanbanModel } from "./catelog_product_kanban_model";
import { CatelogProductKanbanRenderer } from "./catelog_product_kanban_renderer";

export const catelogProductKanbanView = {
    ...kanbanView,
    Model: CatelogProductKanbanModel,
    Renderer: CatelogProductKanbanRenderer,
};

registry.category('views').add('catelog_product_kanban', catelogProductKanbanView);
