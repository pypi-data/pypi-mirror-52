import { DOMWidgetView, unpack_models } from '@jupyter-widgets/base';
import { Message } from '@phosphor/messaging';
import { RegulusViewModel } from "../RegulusWidget";
import Panel from './panel';
import './graph.css';
export declare class GraphModel extends RegulusViewModel {
    defaults(): any;
    static serializers: {
        axes: {
            deserialize: typeof unpack_models;
        };
    };
}
export declare class GraphView extends DOMWidgetView {
    initialize(parameters: any): void;
    render(): void;
    processPhosphorMessage(msg: Message): void;
    model_changed(): void;
    axes_changed(): void;
    update_axes(model: any, value: any, options: any): void;
    panel: Panel;
}
