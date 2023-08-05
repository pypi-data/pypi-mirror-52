import { ManagerBase } from '@jupyter-widgets/base';
import { RegulusModel } from './base';
export declare class TreeModel extends RegulusModel {
    defaults(): {
        _model_name: string;
        root: any;
        attrs: any;
        _model_module: string;
        _model_module_version: string;
        _view_module: string;
        _view_name: string;
        _view_module_version: string;
        _view_count: number;
    };
    static serializers: {
        root: {
            deserialize: typeof unpack_tree;
        };
    };
}
declare class Node {
    constructor(parent: Node, data: any);
    parent: Node;
    children: Node[];
}
declare function unpack_tree(array: any, _: ManagerBase<any>): Node;
export {};
