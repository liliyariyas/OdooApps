/** @odoo-module */

import { KanbanRenderer } from "@web/views/kanban/kanban_renderer";
import { CatelogProductKanbanRecord } from "./catelog_product_kanban_record";

export class CatelogProductKanbanRenderer extends KanbanRenderer { }

CatelogProductKanbanRenderer.components = {
    ...KanbanRenderer.components,
    KanbanRecord: CatelogProductKanbanRecord,
};
