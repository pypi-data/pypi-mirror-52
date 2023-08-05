import { RegulusModel } from './base';
import ndarray = require('ndarray');
export declare class RegulusData extends RegulusModel {
    defaults(): {
        _model_name: string;
        pts_loc: any[];
        pts: ndarray<any>;
        pts_idx: any[];
        pts_extent: any[];
        attrs: ndarray<any>;
        attrs_idx: any[];
        attrs_extent: any[];
        partitions: any[];
        measure: string;
        _model_module: string;
        _model_module_version: string;
        _view_module: string;
        _view_name: string;
        _view_module_version: string;
        _view_count: number;
    };
    pts_loc: number[];
    pts: ndarray;
    pts_idx: string[];
    pts_extent: number[];
    attrs: ndarray;
    attrs_idx: string[];
    attrs_extent: number[];
    partitions: [];
    measure: string;
    static serializers: {
        pts: {
            deserialize: typeof import("jupyter-dataserializers").JSONToUnionArray;
            serialize: typeof import("jupyter-dataserializers").unionToJSON;
        };
        attrs: {
            deserialize: typeof import("jupyter-dataserializers").JSONToUnionArray;
            serialize: typeof import("jupyter-dataserializers").unionToJSON;
        };
    };
    static model_name: string;
}
