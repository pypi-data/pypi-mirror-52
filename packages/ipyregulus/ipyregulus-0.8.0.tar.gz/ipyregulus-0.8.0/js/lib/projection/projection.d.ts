import { DOMWidgetView, unpack_models } from '@jupyter-widgets/base';
import { Message } from '@phosphor/messaging';
import { RegulusViewModel } from "../RegulusWidget";
import Panel from './panel';
import './projection.css';
export declare class ProjectionModel extends RegulusViewModel {
    defaults(): any;
    static serializers: {
        axes: {
            deserialize: typeof unpack_models;
        };
    };
}
export declare class ProjectionView extends DOMWidgetView {
    initialize(parameters: any): void;
    render(): void;
    processPhosphorMessage(msg: Message): void;
    pts_changed(model: any, value: any, options: any): void;
    axes_changed(model: any, value: any, options: any): void;
    update_axes(model: any, value: any, options: any): void;
    colors_changed(model: any, value: any, options: any): void;
    panel: Panel;
}
