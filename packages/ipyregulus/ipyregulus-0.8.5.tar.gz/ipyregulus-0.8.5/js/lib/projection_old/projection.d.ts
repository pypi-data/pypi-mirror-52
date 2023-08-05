import { DOMWidgetView, unpack_models } from '@jupyter-widgets/base';
import { Message } from '@phosphor/messaging';
import { RegulusViewModel } from "../RegulusWidget";
import { Partition } from '../models/partition';
import './projection.css';
export declare class ProjectionOldModel extends RegulusViewModel {
    defaults(): any;
    static serializers: {
        data: {
            deserialize: typeof unpack_models;
        };
        tree_model: {
            deserialize: typeof unpack_models;
        };
    };
}
export declare class ProjectionOldView extends DOMWidgetView {
    initialize(parameters: any): void;
    render(): void;
    processPhosphorMessage(msg: Message): void;
    on_title_changed(): void;
    on_data_changed(): void;
    collect(pts: any, idx: any, from: any, to: any): any;
    on_tree_changed(): void;
    on_color_changed(): void;
    on_show_changed(): void;
    d3el: any;
    panel: any;
    partitions: Map<number, Partition>;
}
