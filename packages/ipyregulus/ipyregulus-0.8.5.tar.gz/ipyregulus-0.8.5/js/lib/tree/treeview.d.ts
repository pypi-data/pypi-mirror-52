import { DOMWidgetView, unpack_models } from "@jupyter-widgets/base";
import { Message } from '@phosphor/messaging';
import './tree.css';
import { RegulusViewModel } from "../RegulusWidget";
export declare class TreeViewModel extends RegulusViewModel {
    defaults(): any;
    static serializers: {
        tree_model: {
            deserialize: typeof unpack_models;
        };
        selected: {
            serialize: (s: any) => unknown[];
            deserialize: (array: any) => Set<unknown>;
        };
    };
}
export declare class TreeView extends DOMWidgetView {
    render(): void;
    processPhosphorMessage(msg: Message): void;
    on_show_attr_changed(): void;
    on_tree_changed(): void;
    on_title_changed(): void;
    on_tree_updated(): void;
    on_attr_changed(): void;
    on_attrs_changed(): void;
    on_show_changed(): void;
    on_highlight_changed(): void;
    on_selected_changed(): void;
    on_details_changed(): void;
    on_range_changed(): void;
    on_x_changed(): void;
    on_y_changed(): void;
    on_highlight(id: any): void;
    on_select(id: any, is_on: any): void;
    on_details(id: any, is_on: any): void;
    d3el: any;
    panel: any;
    tree: any;
}
