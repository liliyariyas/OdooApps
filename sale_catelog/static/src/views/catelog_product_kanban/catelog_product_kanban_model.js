/** @odoo-module */

import { KanbanModel } from '@web/views/kanban/kanban_model';
import { CatelogProductRecord } from './catelog_product_record';

export class CatelogProductKanbanModel extends KanbanModel { }

CatelogProductKanbanModel.Record = CatelogProductRecord;
