import {
    DOMWidgetView, unpack_models
} from '@jupyter-widgets/base';

import {
   Message
} from '@phosphor/messaging';

import {
  RegulusViewModel
} from "../RegulusWidget";

import * as d3 from 'd3';

import Panel from './panel';

import './graph.css';
import template from './graph.html';


export
class GraphModel extends RegulusViewModel {
  defaults() {
    return  {
      ...super.defaults(),
      _model_name: 'GraphModel',
      _view_name: 'GraphView',

      axes: [],
      graph: [],
      show: [],
      color: ''
    };
  }

  static serializers = {
    ...RegulusViewModel.serializers,
    axes: {deserialize: unpack_models}
  };
}

export
class GraphView extends DOMWidgetView {
  initialize(parameters: any): void {
    super.initialize(parameters);
    this.listenTo(this.model, 'change', this.model_changed);
  }

  render() {
     d3.select(this.el)
      .classed('rg_graph', true)
      .html(template);

     this.panel = Panel().el(d3.select(this.el));
     this.axes_changed();
     this.panel.graph(this.model.get('graph'));
     this.panel.color(this.model.get('color'));
     this.panel.show(this.model.get('show'));
     //this.panel.redraw();
  }

  processPhosphorMessage(msg:Message) {
    // console.log('msg:', msg);
    switch (msg.type) {
      case 'after-attach':
        d3.select(this.el.parentNode).classed('rg_graph', true);
        this.panel.resize();
        break;
      case 'resize':
        if (this.panel)
          this.panel.resize();
        break;
    }
  }

  model_changed() {
    console.log('model changed:', this.model.changedAttributes());
    for (let [name, value] of Object.entries(this.model.changedAttributes())) {
      switch (name) {
        case 'axes':
          this.axes_changed();
          break;
        case 'color':
          this.panel.color(this.model.get('color'));
          break;
        case 'graph':
          this.panel.graph(this.model.get('graph'));
          break;
        case 'show':
          this.panel.show(this.model.get('show'));
          break;
        // case 'graph':
        //   let g = this.model.get('graph');
        //   let map = new Map();
        //   for (let p of g.pts) {
        //     map.set(p.id, p)
        //   }
        //   let partitions:[any] = g.partitions;
        //   for (let partition of partitions) {
        //     partition.min = map.get(partition.min_idx);
        //     partition.max = map.get(partition.max_idx);
        //   }
        //   this.panel.graph(g);
        //   break;
        default:
          break;
      }
    }
    this.panel.redraw();
  }

  axes_changed() {
    console.log('axes changed');
    for (let p of this.model.previous('axes') || []) {
      this.stopListening(p);
    }
    let axes = this.model.get('axes');
    for (let a of axes) {
      this.listenTo(a, 'change', this.update_axes);
    }
    console.log('axes = ', axes);
    this.panel.axes(axes).redraw();
  }

  update_axes(model, value, options) {
    this.panel.update_axis(model);
  }

  panel: Panel;
}