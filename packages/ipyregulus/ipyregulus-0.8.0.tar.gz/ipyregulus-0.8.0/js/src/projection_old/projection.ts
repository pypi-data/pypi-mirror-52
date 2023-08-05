import {
    DOMWidgetView, unpack_models
} from '@jupyter-widgets/base';

import {
   Message
} from '@phosphor/messaging';

import {
  RegulusViewModel
} from "../RegulusWidget";

import {
  Partition
} from '../models/partition';

import * as d3 from 'd3';

import Panel from './panel';

import './projection.css';
import template from './projection.html';


export
class ProjectionOldModel extends RegulusViewModel {
  defaults() {
    return  {
      ...super.defaults(),
      _model_name: 'ProjectionOldModel',
      _view_name: 'ProjectionOldView',

      title: '',
      data: null,
      tree_model: null,
      measure: null,
      color: null,
      show: [],
    };
  }

  static serializers = {
    ...RegulusViewModel.serializers,
    data: {deserialize: unpack_models},
    tree_model: {deserialize: unpack_models},
  };
}

export
class ProjectionOldView extends DOMWidgetView {
  initialize(parameters: any): void {
    super.initialize(parameters);
    this.model.on('change:title', this.on_title_changed, this);
    this.model.on('change:data', this.on_data_changed, this);
    this.model.on('change:tree_model', this.on_tree_changed, this);
    this.model.on('change:show', this.on_show_changed, this);
    this.model.on('change:color', this.on_color_changed, this);
  }

  render() {
    this.d3el = d3.select(this.el)
      .classed('rg_projection', true);

    this.d3el.html(template);
    this.panel = Panel().el(d3.select(this.el));

    setTimeout( () => {
      console.log('projection setup');
      this.panel.resize();
      this.on_title_changed();
      this.on_data_changed();
      this.on_tree_changed();
    }, 0);
  }

  processPhosphorMessage(msg:Message) {
    // console.log('Tree phosphor message', msg);
    switch (msg.type) {
      case 'after-attach':
        d3.select(this.el.parentNode).classed('rg_projection', true);
        break;
      case 'resize':
        this.panel.resize();
        break;
    }
  }

  on_title_changed() {
    this.d3el.select('.title').text(this.model.get('title'));
  }

  on_data_changed() {
    let data = this.model.get('data');
    if (data) {
      // axes info
      let pts = data.get('pts');
      let pts_idx = data.get('pts_idx');
      let axes = this.collect(pts, pts_idx, 0, pts.shape[1]);

      let attrs = data.get('attrs');
      let attrs_idx = data.get('attrs_idx');
      let measure = data.get('measure');
      let m = attrs_idx.indexOf(measure);
      axes = axes.concat( this.collect(attrs, attrs_idx, m, m+1));
      this.panel.axes(axes);

      // partitions
      let pts_loc = data.get('pts_loc');
      this.partitions = new Map( data.get('partitions').map(p => [p.id, new Partition(p, pts_loc)]));
    }
  }

  collect(pts, idx, from, to) {
    let n = pts.shape[0];
    let axes = idx.slice(from, to).map((col, i) => ({name:col, min:0, max:0}));
    let v = 0;
    for (let axis=0, d=from; d<to; axis++, d++) {
      axes[axis].min= axes[axis].max = pts.get(0, d);
    }
    for (let i=1; i<n; i++) {
      for (let axis=0, d=from; d<to; axis++, d++) {
        let a = axes[axis];
        v = pts.get(i, d);
        if (v < a.min) a.min = v;
        else if (a.max < v) a.max = v;
      }
    }
    return axes;
  }

  on_tree_changed() {
    let tree = this.model.get('tree_model');
    if (tree) {
      console.log('tree');

    }
  }

  on_color_changed() {
    let name = this.model.get('color');
    let data = this.model.get('data');
    let attrs = data.get('attrs');
    let attrs_idx = data.get('attrs_idx');
    let color_idx = attrs_idx.indexOf(name);
    let show = this.model.get('show');

    let colors: Array<number> = [];
    if (color_idx > -1) {
      let colors_array = attrs.pick(null, color_idx);

      if (this.partitions) {
        for (let p of show) {
          let partition = this.partitions.get(p);
          if (!partition) continue;
          let pts_idx = partition.index();
          for (let idx of pts_idx) {
            colors.push(colors_array.get(idx, 0));
          }
        }
      }
    }
    this.panel.colors(colors);
  }

  on_show_changed() {
    let show = this.model.get('show');
    let data = this.model.get('data');
    let data_pts = data.get('pts');
    let attrs = data.get('attrs');
    let attrs_idx = data.get('attrs_idx');
    let measure_name = data.get('measure');
    let measure_idx = attrs_idx.indexOf(measure_name);
    let measure = attrs.pick(null,measure_idx);

    let pts: Array<any> = [];
    if (this.partitions) {
      for (let p of show) {
        let partition = this.partitions.get(p);
        if (!partition) continue;

        let pts_idx =  partition.index();
        for (let idx of pts_idx) {
          let pt:number[] = [];
          let i;
          for (i=0; i< data_pts.shape[1]; i++)
            pt[i] = (data_pts.get(idx, i));

          pt[i] = measure.get(idx);
          // for (let j=0; j< data_attrs.shape[1]; j++)
          //   pt[i+j] = (data_attrs.get(idx, j));
          pts.push({ value: pt});
        }
      }
    }
    this.panel.pts(pts);
    this.on_color_changed();
  }

  d3el: any;
  panel: any;
  partitions: Map<number, Partition> = new Map();
}