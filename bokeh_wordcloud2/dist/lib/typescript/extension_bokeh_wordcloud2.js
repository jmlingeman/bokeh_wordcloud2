var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
// import {DataProvider} from "models/widgets/tables/data_table";
import { WidgetView } from "@bokeh/bokehjs/models/widgets/widget";
import * as p from "@bokeh/bokehjs/core/properties";
import { CDSView } from "@bokeh/bokehjs/models/sources/cds_view";
import { Widget } from "@bokeh/bokehjs/models/widgets";
import { ColumnDataSource } from "@bokeh/bokehjs/models/sources/column_data_source";
import { keys } from "@bokeh/bokehjs/core/util/object";
import { range } from "@bokeh/bokehjs/core/util/array";
import { BokehEvent } from "@bokeh/bokehjs/core/bokeh_events";
export const DTINDEX_NAME = "__bkdt_internal_index__";
function event(event_name) {
    return function (cls) {
        cls.prototype.event_name = event_name;
    };
}
// @setExperimentalDecorators
let WordClickEvent = class WordClickEvent extends BokehEvent {
    constructor(word, weight) {
        super();
        this.word = word;
        this.weight = weight;
    }
    _to_json() {
        const { word, weight } = this;
        return { weight, word };
    }
};
WordClickEvent.__name__ = "WordClickEvent";
WordClickEvent = __decorate([
    event("word_click_event")
], WordClickEvent);
export { WordClickEvent };
// export type myCB<T> = CallbackLike<T, [string,number,number,number,number], Ret>
class DataProvider {
    constructor(source, view) {
        this.source = source;
        this.view = view;
        if (DTINDEX_NAME in this.source.data)
            throw new Error(`special name ${DTINDEX_NAME} cannot be used as a data table column`);
        // Convert the bitset into indicies
        var idx = [];
        for (const i of this.view.indices) {
            idx.push(i);
        }
        this.index = idx;
    }
    getLength() {
        return this.index.length;
    }
    getItem(offset) {
        const item = {};
        for (const field of keys(this.source.data)) {
            item[field] = this.source.data[field][this.index[offset]];
        }
        item[DTINDEX_NAME] = this.index[offset];
        return item;
    }
    getRecords() {
        return range(0, this.getLength()).map((i) => this.getItem(i));
    }
}
DataProvider.__name__ = "DataProvider";
function Counter(objects) {
    const d = {};
    for (let itm of objects) {
        d[itm] = d[itm] ? d[itm] + 1 : 1;
    }
    return d;
}
function sortedCounter(objects) {
    const d = Counter(objects);
    const arr = Object.keys(d).map((k) => [k, d[k]]);
    return arr.sort((a, b) => b[1] - a[1]);
}
function choose(choices) {
    var index = Math.floor(Math.random() * choices.length);
    return choices[index];
}
function choose_str(original_list) {
    return choose(original_list);
}
export class WordCloud2View extends WidgetView {
    DEFAULT_WEIGHT_FACTOR(size) {
        return Math.pow(size, 2.3) * this.model.height / 1024;
    }
    initialize() {
        this.DEFAULT_WEIGHT_FACTOR = this.DEFAULT_WEIGHT_FACTOR.bind(this);
        super.initialize();
        this.prepare();
    }
    prepare() {
        if (this.model.fontWeight && typeof this.model.fontWeight['execute'] === "function") {
            const cb_func = this.model.weightFactor;
            this.model.fontWeight = (word, weight, font_size) => {
                const data = { word: word, weight: weight, font_size: font_size };
                return cb_func.execute(this.model, data);
            };
        }
        if (this.model.weightFactor && typeof this.model.weightFactor['execute'] === "function") {
            const cb_func = this.model.weightFactor;
            this.model.weightFactor = (size) => {
                const data = { size: size };
                return cb_func ? cb_func.execute(this.model, data) : this.DEFAULT_WEIGHT_FACTOR;
            };
        }
        if (this.model.classes && typeof this.model.classes['execute'] === "function") {
            const cb_func = this.model.classes;
            this.model.classes = (word, weight, font_size) => {
                const data = { word: word, weight: weight, font_size: font_size };
                return cb_func.execute(this.model, data);
            };
        }
        if (this.model.color && typeof this.model.color['execute'] === "function") {
            // its a callback
            const cb_func = this.model.color;
            this.model.color = (word, weight, font_size, distance, theta) => {
                const data = { word: word, weight: weight, font_size: font_size, distance: distance, theta: theta };
                return cb_func.execute(this.model, data);
            };
        }
        else if (typeof this.model.color === "object" && typeof this.model.color['slice'] === "function") {
            // its a list??
            const original_list = this.model.color;
            this.model.color = () => choose_str(original_list);
        }
        else if (typeof this.model.color === "string") {
            const col = this.model.source.get_column(this.model.color);
            if (col && col.length > 0) {
                const data = {};
                const colors = this.model.source.get_column(this.model.color);
                const keys = this.model.source.get_column(this.model.wordCol);
                if (keys && keys.length && colors && colors.length) {
                    for (let i = 0; i < keys.length; i++) {
                        if (keys[i] && colors[i]) {
                            data[keys[i]] = colors[i];
                        }
                    }
                }
                this.model.color = (word) => data[word];
            }
        }
    }
    // private grid: SlickGrid
    // update_data() {
    //     this.model.view.compute_indices()
    //     this.data.constructor(this.model.source, this.model.view)
    //     this.render()
    // }
    connect_signals() {
        super.connect_signals();
        // this.connect(this.model.change, () => this.render())
        //
        // this.connect(this.model.source.streaming, () => this.updateGrid())
        // this.connect(this.model.source.patching, () => this.updateGrid())
        this.connect(this.model.source.change, () => {
            this.prepare();
            this.render();
        });
        // this.connect(this.model.source.properties.data.change, () => this.updateGrid())
        //
        // this.connect(this.model.source.selected.change, () => this.updateSelection())
        // this.connect(this.model.source.selected.properties.indices.change, () => this.updateSelection())
    }
    css_classes() {
        return super.css_classes().concat("bk-data-table");
    }
    get_sizes1() {
        if (!this.model.sizeCol) {
            let words = [];
            this.data.getRecords().map(record => {
                const results = record[this.model.wordCol].toUpperCase().match(/([A-Z]+)/);
                words.push(...results);
            });
            return sortedCounter(words).slice(0, 50);
            // console.log(sortedCounter(this.model.source.get_column(this.model.wordCol) as unknown as string[]));
        }
        const s = [];
        this.data.getRecords().map((item) => {
            s.push([item[this.model.wordCol], item[this.model.sizeCol]]);
        });
        return s;
    }
    render() {
        super.render();
        this.data = new DataProvider(this.model.source, this.model.view);
        let sizes = this.get_sizes1();
        const canvas = document.createElement("canvas");
        canvas.width = this.model.width;
        canvas.height = this.model.height;
        // const colors: string[] = this.model.colors ? this.model.colors : [this.model.color,];
        const default_grid_size = Math.round(16 * this.model.width / 1024);
        const opts = {
            list: sizes,
            fontFamily: this.model.fontFamily ? this.model.fontFamily : 'Times, serif',
            gridSize: this.model.gridSize ? this.model.gridSize : default_grid_size,
            weightFactor: this.model.weightFactor ? this.model.weightFactor : this.DEFAULT_WEIGHT_FACTOR,
            color: this.model.color,
            rotateRatio: this.model.rotateRatio,
            minRotation: this.model.minRotation,
            maxRotation: this.model.maxRotation,
            rotationSteps: this.model.rotationSteps,
            shuffle: false,
            backgroundColor: this.model.background,
            drawOutOfBound: false,
            classes: this.model.classes,
            fontWeight: this.model.fontWeight,
            shape: this.model.shape,
            click: (target, dimensions, event) => {
                let source = undefined;
                if (this.model.sizeCol) {
                    const len_recs = this.data.getLength();
                    for (let i = 0; i < len_recs; i++) {
                        const itm = this.data.getItem(i);
                        if (itm[this.model.wordCol] === target[0] && itm[this.model.sizeCol] === target[1]) {
                            source = this.data.source;
                            source.selected.indices = [i];
                            break;
                        }
                    }
                }
                if (source === undefined) {
                    source = new ColumnDataSource({
                        data: {
                            word: [target[0],],
                            weight: [target[1],]
                        }
                    });
                    source.selected.indices = [0]; // update our "selected" indices ...
                }
                const data = { word: target[0], weight: target[1], extra: target[2],
                    dimensions: dimensions, event: event, source: source };
                // trigger event to python
                // this.model.trigger_event(new WordClickEvent(data.word,data.weight))
                // trigger user js click handler
                if (this.model.click)
                    this.model.click.execute(this.model, data);
            },
            hover: (!this.model.hover) ? null : (...args) => {
                if (this.model.hover) {
                    if (!args || !args[0])
                        return;
                    const data = { word: args[0][0], weight: args[0][1], dimensions: args[1], event: args[2] };
                    this.model.hover.execute(this.model, data);
                }
            },
        };
        this.el.appendChild(canvas);
        WordCloud(canvas, opts);
    }
}
WordCloud2View.__name__ = "WordCloud2View";
export class WordCloud2 extends Widget {
    constructor(attrs) {
        super(attrs);
    }
    static initClass() {
        this.prototype.type = 'WordCloud2';
        this.prototype.default_view = WordCloud2View;
        this.define({
            // every property here should be defined in the namespace above
            // and in the pyfile with exactly the same name
            source: [p.Instance],
            view: [p.Instance, () => new CDSView()],
            wordCol: [p.String],
            sizeCol: [p.String],
            color: [p.Any, "blue"],
            fontWeight: [p.Any, "normal"],
            classes: [p.Any, null],
            hover: [p.Instance, null],
            click: [p.Instance, null],
            rotateRatio: [p.Number, 1],
            minRotation: [p.Number, 0],
            maxRotation: [p.Number, Math.PI / 2],
            rotationSteps: [p.Number, 32],
            gridSize: [p.Number, 16],
            fontFamily: [p.String, "Times, Serif"],
            shape: [p.String, "square"],
            weightFactor: [p.Any, null],
        });
        this.override({
            width: 600,
            height: 400,
            background: "#FFFFFF",
        });
    }
}
WordCloud2.__name__ = "WordCloud2";
WordCloud2.initClass();
//# sourceMappingURL=extension_bokeh_wordcloud2.js.map