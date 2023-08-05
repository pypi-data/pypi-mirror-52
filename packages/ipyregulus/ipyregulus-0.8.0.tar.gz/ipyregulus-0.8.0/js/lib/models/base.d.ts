import { WidgetModel } from '@jupyter-widgets/base';
export declare class RegulusModel extends WidgetModel {
    defaults(): {
        _model_module: string;
        _model_module_version: string;
        _model_name: string;
        _view_module: string;
        _view_name: string;
        _view_module_version: string;
        _view_count: number;
    };
    static serializers: {
        [x: string]: {
            deserialize?: (value?: any, manager?: import("@jupyter-widgets/base").ManagerBase<any>) => any;
            serialize?: (value?: any, widget?: WidgetModel) => any;
        };
    };
    static model_module: string;
    static model_module_version: string;
}
