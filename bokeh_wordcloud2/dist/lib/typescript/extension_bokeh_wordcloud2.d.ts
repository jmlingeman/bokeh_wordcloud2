import { WidgetView } from "@bokehjs/models/widgets/widget";
import * as p from "@bokehjs/core/properties";
import { CDSView } from "@bokehjs/models/sources/cds_view";
import { Widget } from "@bokehjs/models/widgets";
import { ColumnDataSource } from "@bokehjs/models/sources/column_data_source";
import { CallbackLike1 } from "@bokehjs/models/callbacks/callback";
import { BokehEvent } from "@bokehjs/core/bokeh_events";
export declare type JSOND = {
    [key: string]: unknown;
};
export declare const DTINDEX_NAME = "__bkdt_internal_index__";
export declare type Item = {
    [key: string]: any;
};
export declare type data_ob_color_cb = {
    word: string;
    weight: number;
    fontsize: number;
    distance: number;
    theta: number;
};
export declare type data_ob_weightFactor_cb = {
    size: number;
};
export declare class WordClickEvent extends BokehEvent {
    readonly word: string;
    readonly weight: number;
    constructor(word: string, weight: number);
    protected _to_json(): JSOND;
}
export declare class WordCloud2View extends WidgetView {
    model: WordCloud2 & {
        source: ColumnDataSource;
        view: CDSView;
        wordCol: string;
        sizeCol: string;
        width: number;
        height: number;
        background: string;
        color: string | string[] | ((...args: any[]) => string) | CallbackLike1<WordCloud2, Partial<data_ob_color_cb>, string>;
        fontWeight: number | ((...a: any[]) => any) | CallbackLike1<WordCloud2, Partial<data_ob_color_cb>, string> | null;
        fontFamily: string;
        weightFactor: number | ((...a: any[]) => any) | CallbackLike1<WordCloud2, Partial<data_ob_weightFactor_cb>, number> | null;
        classes: string | ((...a: any[]) => any) | CallbackLike1<WordCloud2, Partial<data_ob_color_cb>, string>;
        hover: CallbackLike1<WordCloud2, Partial<data_ob_color_cb>, null> | null;
        click: CallbackLike1<WordCloud2, Partial<data_ob_color_cb>, null> | null;
        rotateRatio: number;
        minRotation: number;
        maxRotation: number;
        rotationSteps: number;
        shape: string;
        gridSize: number;
    };
    private data;
    private DEFAULT_WEIGHT_FACTOR;
    initialize(): void;
    prepare(): void;
    connect_signals(): void;
    css_classes(): string[];
    get_sizes1(): [string, number][];
    render(): void;
}
export declare namespace WordCloud2 {
    type Attrs = p.AttrsOf<Props>;
    type Props = Widget.Props & {
        source: p.Property<ColumnDataSource>;
        view: p.Property<CDSView>;
        wordCol: p.Property<string>;
        sizeCol: p.Property<string>;
        color: p.Property<any>;
        fontWeight: p.Property<string | ((...a: any[]) => any) | CallbackLike1<WordCloud2, Partial<data_ob_color_cb>, string> | null>;
        classes: p.Property<string | ((...a: any[]) => any) | CallbackLike1<WordCloud2, Partial<data_ob_color_cb>, string> | null>;
        hover: p.Property<CallbackLike1<WordCloud2, Partial<data_ob_color_cb>, null> | null>;
        click: p.Property<CallbackLike1<WordCloud2, Partial<data_ob_color_cb>, null> | null>;
        rotateRatio: p.Property<number>;
        minRotation: p.Property<number>;
        maxRotation: p.Property<number>;
        rotationSteps: p.Property<number>;
        gridSize: p.Property<number>;
        fontFamily: p.Property<string>;
        shape: p.Property<string>;
        weightFactor: p.Property<number | ((...args: any[]) => number) | null>;
    };
}
export interface WordCloud2 extends Widget.Attrs {
}
export declare class WordCloud2 extends Widget {
    properties: Widget.Props;
    constructor(attrs?: Partial<WordCloud2.Attrs>);
    static initClass(): void;
}
