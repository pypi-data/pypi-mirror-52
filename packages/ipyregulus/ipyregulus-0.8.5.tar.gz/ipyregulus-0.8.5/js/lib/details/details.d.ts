import { DOMWidgetView, unpack_models } from '@jupyter-widgets/base';
import { Message } from '@phosphor/messaging';
import { RegulusViewModel } from "../RegulusWidget";
import { Partition } from '../models/partition';
import './details.css';
export declare class DetailsModel extends RegulusViewModel {
    defaults(): any;
    static serializers: {
        data: {
            deserialize: typeof unpack_models;
        };
        tree_model: {
            deserialize: typeof unpack_models;
        };
    };
    static model_name: string;
    static view_name: string;
}
export declare class DetailsView extends DOMWidgetView {
    render(): void;
    processPhosphorMessage(msg: Message): void;
    title_changed(): void;
    d3el: any;
    panel: any;
    partitions: Map<number, Partition>;
}
