import math
from bokeh.core.property.container import Array, List
from bokeh.core.property.either import Either
from bokeh.core.property.enum import Enum
from bokeh.core.property.instance import Instance
from bokeh.core.property.primitive import String, Float, Int
from bokeh.events import Event
from bokeh.models import (
    DataSource,
    CDSView,
    Widget,
    CustomJS,
    Callback,
    ColumnDataSource,
    Button,
)

# from bokeh.sphinxext.util import


class WordClick(Event):
    """
    Custom Event that is fired when the user clicks a word
    """

    event_name = "word_click_event"
    word = None
    weight = None

    def __init__(self, model, word, weight):
        if model is not None and not isinstance(model, WordCloud2):
            msg = "{clsname} event only applies to button models"
            raise ValueError(msg.format(clsname=self.__class__.__name__))
        self.word = word
        self.weight = weight

        super(WordClick, self).__init__(model=model)

    def __str__(self):
        return "<WordClickEvent word=%r weight=%r>" % (self.word, self.weight)

    def __repr__(self):
        return str(self)


class _WordCloud2Meta(Widget):
    JS_CODE = """
// import {DataProvider} from "models/widgets/tables/data_table";
import {WidgetView} from "models/widgets/widget";
import {Arrayable} from "core/types";
import * as p from "core/properties";
import {CDSView} from "models/sources/cds_view";
import {Widget} from "models/widgets";
import {ColumnDataSource} from "models/sources/column_data_source";
import {keys} from "core/util/object";
import {range} from "core/util/array";
// import {CallbackLike0} from "models/callbacks/callback";
import {CallbackLike1} from "models/callbacks/callback";
import {BokehEvent} from "core/bokeh_events";
import {Class} from "core/class";
// import {ColumnarDataSource} from "api";
export type JSOND = {[key: string]: unknown}
export const DTINDEX_NAME = "__bkdt_internal_index__"
export type Item = { [key: string]: any }
export type data_ob_color_cb={
    word:string,weight:number,fontsize:number,distance:number,theta:number
}
export type data_ob_weightFactor_cb={
    size:number
}

function event(event_name: string) {
  return function(cls: Class<BokehEvent>) {
    cls.prototype.event_name = event_name
  }
}
// @setExperimentalDecorators
@event("word_click_event")
export class WordClickEvent extends BokehEvent{
    constructor(readonly word:string,readonly weight:number){
        super()
    }
    protected _to_json(): JSOND {
        const {word,weight} = this
        return {weight,word}
    }
}
// export type myCB<T> = CallbackLike<T, [string,number,number,number,number], Ret>
class DataProvider {

    readonly index: number[]

    constructor(readonly source: ColumnDataSource, readonly view: CDSView) {
        if (DTINDEX_NAME in this.source.data)
            throw new Error(`special name ${DTINDEX_NAME} cannot be used as a data table column`)
        // Convert the bitset into indicies
        var idx: number[] = []
        for (const i of this.view.indices) {
          idx.push(i)
        }
        this.index = idx
    }

    getLength(): number {
        return this.index.length
    }

    getItem(offset: number): Item {
        const item: Item = {}
        for (const field of keys(this.source.data)) {
            item[field] = this.source.data[field][this.index[offset]]
        }
        item[DTINDEX_NAME] = this.index[offset]
        return item
    }

    getRecords(): Item[] {
        return range(0, this.getLength()).map((i) => this.getItem(i))
    }

}

declare function WordCloud(...args: any[]): any

function Counter(objects:string[]):{[key:string]:number}{
    const d:{[key:string]:number} = {}
    for(let itm of objects){
        d[itm] = d[itm]?d[itm]+1:1
    }
    return d
}
function sortedCounter(objects:string[]):[string,number][]{
    const d = Counter(objects);
    const arr = Object.keys(d).map((k:string)=>[k as string,d[k] as number]);
    return arr.sort((a:[string,number],b:[string,number])=>b[1]-a[1]) as [string,number][];
}
function choose<T>(choices:T[]):T{
  var index = Math.floor(Math.random() * choices.length);
  return choices[index];
}
function choose_str(original_list: string[]) : string{
    return choose<string>(original_list);
}
interface IAttr{
    [key:string]:any
}
export class WordCloud2View extends WidgetView {
    model: WordCloud2 & {
        source: ColumnDataSource;
        view: CDSView;
        wordCol: string;
        sizeCol: string;
        width: number;
        height: number;
        background: string;
        color:string|string[]|((...args:any[]) => string)|CallbackLike1<WordCloud2,Partial<data_ob_color_cb>,string>;
        fontWeight:number|((...a:any[])=>any)|CallbackLike1<WordCloud2,Partial<data_ob_color_cb>,string>|null;
        fontFamily:string;
        weightFactor:number|((...a:any[])=>any)|CallbackLike1<WordCloud2,Partial<data_ob_weightFactor_cb>,number>|null;
        classes:string|((...a:any[])=>any)|CallbackLike1<WordCloud2,Partial<data_ob_color_cb>,string>;
        hover:CallbackLike1<WordCloud2,Partial<data_ob_color_cb>,null>|null;
        click:CallbackLike1<WordCloud2,Partial<data_ob_color_cb>,null>|null;
        // rotation
        rotateRatio:number,
        minRotation:number,
        maxRotation:number,
        rotationSteps:number,

        shape:string,
        gridSize:number,
    };
    private data: DataProvider;
    private DEFAULT_WEIGHT_FACTOR(size:number){
                return Math.pow(size, 2.3) *  this.model.height / 1024;
    }
    initialize() {
        this.DEFAULT_WEIGHT_FACTOR = this.DEFAULT_WEIGHT_FACTOR.bind(this);
        super.initialize();
        this.prepare()
    }
    prepare(){
        if(this.model.fontWeight && typeof (this.model.fontWeight as IAttr)['execute'] === "function"){
            const cb_func:CallbackLike1<WordCloud2,Partial<data_ob_color_cb>,number> = this.model.weightFactor as CallbackLike1<WordCloud2,Partial<data_ob_color_cb>,number>;
            this.model.fontWeight = (word:string,weight:number,font_size:number)=>{
                const data ={word:word,weight:weight,font_size:font_size};
                return cb_func.execute(this.model,data);
            }
        }
        if(this.model.weightFactor && typeof (this.model.weightFactor as IAttr)['execute'] === "function"){
            const cb_func:CallbackLike1<WordCloud2,Partial<data_ob_weightFactor_cb>,number> = this.model.weightFactor as CallbackLike1<WordCloud2,Partial<data_ob_weightFactor_cb>,number>;
            this.model.weightFactor = (size:number)=>{
                const data ={size:size};
                return cb_func?cb_func.execute(this.model,data):this.DEFAULT_WEIGHT_FACTOR
            }
        }
        if(this.model.classes && typeof (this.model.classes as IAttr)['execute'] === "function"){
            const cb_func:CallbackLike1<WordCloud2,Partial<data_ob_color_cb>,string> = this.model.classes as CallbackLike1<WordCloud2,Partial<data_ob_color_cb>,string>;
            this.model.classes = (word:string,weight:number,font_size:number)=>{
                const data ={word:word,weight:weight,font_size:font_size};
                return cb_func.execute(this.model,data);
            }
        }
        if(this.model.color && typeof (this.model.color as IAttr)['execute'] === "function"){
            // its a callback
            const cb_func:CallbackLike1<WordCloud2,Partial<data_ob_color_cb>,string> = this.model.color as CallbackLike1<WordCloud2,Partial<data_ob_color_cb>,string>;
            this.model.color = (word:string,weight:number,font_size:number,distance:number,theta:number)=>{
                const data ={word:word,weight:weight,font_size:font_size,distance:distance,theta:theta};
                return cb_func.execute(this.model,data);
            }
        }else if (typeof this.model.color==="object" && typeof (this.model.color as IAttr)['slice'] === "function"){
            // its a list??
            const original_list:string[] = this.model.color as string[];
            this.model.color = ()=>choose_str(original_list);
        }else if (typeof this.model.color==="string"){
            const col = this.model.source.get_column(this.model.color);
            if(col && col.length>0) {
                const data: { [key: string]: string } = {};
                const colors = this.model.source.get_column(this.model.color);
                const keys = this.model.source.get_column(this.model.wordCol)
                if (keys && keys.length && colors && colors.length) {
                    for (let i = 0; i < keys.length; i++) {
                        if (keys[i] && colors[i]) {
                            data[keys[i]] = colors[i]
                        }
                    }
                }
                this.model.color = (word: string): string => data[word] as string;
            }
        }

    }
    // private grid: SlickGrid

    // update_data() {
    //     this.model.view.compute_indices()
    //     this.data.constructor(this.model.source, this.model.view)
    //     this.render()
    // }
    connect_signals(): void {
        super.connect_signals()
        // this.connect(this.model.change, () => this.render())
        //
        // this.connect(this.model.source.streaming, () => this.updateGrid())
        // this.connect(this.model.source.patching, () => this.updateGrid())
        this.connect(this.model.source.change, () => {
            this.prepare();
            this.render();
        })
        // this.connect(this.model.source.properties.data.change, () => this.updateGrid())
        //
        // this.connect(this.model.source.selected.change, () => this.updateSelection())
        // this.connect(this.model.source.selected.properties.indices.change, () => this.updateSelection())
    }


    css_classes(): string[] {
        return super.css_classes().concat("bk-data-table")
    }

    get_sizes1() {
        if(!this.model.sizeCol){
            let words:string[] = []
            this.data.getRecords().map(record=>{
                const results = record[this.model.wordCol].toUpperCase().match(/([A-Z]+)/);
                words.push(...results)
            });
            return sortedCounter(words).slice(0,50)
            // console.log(sortedCounter(this.model.source.get_column(this.model.wordCol) as unknown as string[]));
        }
        const s: [string, number][] = [];
        this.data.getRecords().map((item) => {
            s.push([item[this.model.wordCol], item[this.model.sizeCol]]);
        });
        return s;
    }

    render(): void {
        super.render();
        this.data = new DataProvider(this.model.source, this.model.view);
        let sizes = this.get_sizes1()
        const canvas = document.createElement("canvas")
        canvas.width = this.model.width;
        canvas.height = this.model.height;

        // const colors: string[] = this.model.colors ? this.model.colors : [this.model.color,];
        const default_grid_size = Math.round(16 *  this.model.width / 1024)
        const opts = {
            list: sizes,
            fontFamily: this.model.fontFamily?this.model.fontFamily:'Times, serif',
            gridSize: this.model.gridSize?this.model.gridSize:default_grid_size,
            weightFactor: this.model.weightFactor?this.model.weightFactor:this.DEFAULT_WEIGHT_FACTOR ,
            color: this.model.color,
            rotateRatio: this.model.rotateRatio,
            minRotation: this.model.minRotation,
            maxRotation: this.model.maxRotation,
            rotationSteps: this.model.rotationSteps,
            shuffle: false,
            backgroundColor: this.model.background,
            drawOutOfBound: false,
            classes:this.model.classes,
            fontWeight:this.model.fontWeight,
            shape: this.model.shape,
            click: (target:[string,number,any],dimensions:[number,number,number,number],event:any)=>{
                let source:ColumnDataSource|undefined=undefined;
                if(this.model.sizeCol){
                    const len_recs = this.data.getLength();
                    for(let i=0;i<len_recs;i++){
                        const itm = this.data.getItem(i);
                        if(itm[this.model.wordCol] === target[0] && itm[this.model.sizeCol]===target[1]){
                            source = this.data.source
                            source.selected.indices = [i]
                            break;
                        }
                    }
                }
                if(source===undefined) {
                    source = new ColumnDataSource({
                        data: {
                            word: [target[0],] as unknown as Arrayable,
                            weight: [target[1],] as unknown as Arrayable
                        }
                    });
                    source.selected.indices = [0]; // update our "selected" indices ...
                }
                const data = {word:target[0],weight:target[1],extra:target[2],
                              dimensions:dimensions,event:event,source:source};
                // trigger event to python
                // this.model.trigger_event(new WordClickEvent(data.word,data.weight))
                // trigger user js click handler
                if(this.model.click)this.model.click.execute(this.model,data);
            },
            hover: (!this.model.hover)?null:(...args:any[])=>{
                if(this.model.hover) {
                    if (!args || !args[0])return;
                    const data = {word: args[0][0], weight: args[0][1], dimensions: args[1], event: args[2]};
                    this.model.hover.execute(this.model, data);
                }
            },
        };
        this.el.appendChild(canvas);
        WordCloud(canvas, opts);
    }


}

export namespace WordCloud2 {
    export type Attrs = p.AttrsOf<Props>
    // every property here should also be called out in the pyfile
    // as well as the define below
    export type Props = Widget.Props & {
        source: p.Property<ColumnDataSource>
        view: p.Property<CDSView>
        wordCol: p.Property<string>
        sizeCol: p.Property<string>
        color: p.Property<any>
        fontWeight:p.Property<string|((...a:any[])=>any)|CallbackLike1<WordCloud2,Partial<data_ob_color_cb>,string>|null>
        classes:p.Property<string|((...a:any[])=>any)|CallbackLike1<WordCloud2,Partial<data_ob_color_cb>,string>|null>
        hover:p.Property<CallbackLike1<WordCloud2,Partial<data_ob_color_cb>,null>|null>
        click:p.Property<CallbackLike1<WordCloud2,Partial<data_ob_color_cb>,null>|null>
        rotateRatio:p.Property<number>
        minRotation:p.Property<number>
        maxRotation:p.Property<number>
        rotationSteps:p.Property<number>
        gridSize:p.Property<number>
        fontFamily:p.Property<string>
        shape:p.Property<string>
        weightFactor:p.Property<number|((...args:any[])=>number)|null>
    }
}

export interface WordCloud2 extends Widget.Attrs {
}

export class WordCloud2 extends Widget {
    properties: Widget.Props;

    constructor(attrs?: Partial<WordCloud2.Attrs>) {
        super(attrs)
    }

    static initClass(): void {
        this.prototype.type = 'WordCloud2'
        this.prototype.default_view = WordCloud2View;

        this.define<WordCloud2.Props>({
            // every property here should be defined in the namespace above
            // and in the pyfile with exactly the same name
            source: [p.Instance],
            view: [p.Instance, () => new CDSView()],
            wordCol: [p.String],
            sizeCol: [p.String],
            color: [p.Any, "blue"],
            fontWeight:[p.Any, "normal"],
            classes:[p.Any, null],
            hover:[p.Instance, null],
            click:[p.Instance, null],
            rotateRatio:[p.Number, 1],
            minRotation:[p.Number,  0],
            maxRotation:[p.Number,  Math.PI/2],
            rotationSteps:[p.Number,  32],
            gridSize:[p.Number,  16],
            fontFamily:[p.String,  "Times, Serif"],
            shape: [p.String, "square"],
            weightFactor: [p.Any, null],

        });

        this.override({
          width: 600,
          height: 400,
          background: "#FFFFFF",
        })
    }


}

WordCloud2.initClass()
    """
    __implementation__ = JS_CODE
    __javascript__ = [
        "https://ajax.googleapis.com/ajax/libs/jquery/2.1.1/jquery.min.js",
        "https://cdnjs.cloudflare.com/ajax/libs/wordcloud2.js/1.0.6/wordcloud2.min.js",
        "https://cdn.jsdelivr.net/gh/timdream/wordcloud2.js@gh-pages/src/wordcloud2.js",
    ]


myEnum = (
    "circle",
    "cartoid",
    "diamond",
    "square",
    "triangle-forward",
    "triangle",
    "pentagon",
    "star",
)


class WordCloud2(_WordCloud2Meta):
    """
    Provides a Bokeh Interface to WordCloud  (https://wordcloud2-js.timdream.org)

    As Such it accepts Most of the same arguments.

    .. note::

       - any CustomJS callback will have two variables available `cb_obj` which is the model, and `cb_data` which is the data for the CustomJS Callback
       - depending on context `cb_data` will have different properties, but *usually* `cb_data.word` and `cb_data.weight` will be available
       - many CustomJS callbacks **MUST** return a value (see the docs for the various attributes)

    """

    source = Instance(
        DataSource,
        help="""
        **required** The source of data for the widget.
        
        .. code-block:: python
        
           data = ColumnDataSource(data=dict(words=list("ABCDE"),sizes=[1,4,2,5,7]))
           WordCloud(source=data, wordCol="words", sizeCol="sizes", color="blue")
        
        """,
    )

    view = Instance(
        CDSView,
        help="""
        A view into the data source to use when rendering table rows. A default view
        of the entire data source is created if a view is not passed in during
        initialization.
        
        .. code-block:: python
        
           view = CDSView(source=data,filter=GroupFilter(column_name="active",value="true"))        
           WordCloud(source=data, view=view, wordCol="words", sizeCol="sizes", color=["red","blue"])
                                         
        """,
    )

    sizeCol = String(
        help="the column of the weights, if unspecified it will count word occurences"
    )
    wordCol = String(help="**required** the column with the words in it")
    color = Either(
        String,
        List(String),
        Instance(CustomJS),
        help="""
     the color or colors to use when generating the wordcloud
     
     .. code-block:: python
     
         data = ColumnDataSource(data={
            words = ['apple','pie','tastes','delicious'],
            weights = [11,10,20,15],
            colors=['red','blue','blue','green']
         })
         
         # a single color, all words will be pink on a blue background
         wc1 = WordCloud(source=data,wordCol="words", sizeCol="weights", color="pink", background="blue")
         
         # 2 colors that will be selected at random, on a yellow background
         wc2 = WordCloud(source=data,wordCol="words", sizeCol="weights", background="yellow",color=["blue","red"])
         
         # specify a column to use for the colors
         wc3 = WordCloud(source=data,wordCol="words", sizeCol="weights", background="yellow",color="colors")
         
         # specify a javascript callback ,(default white background)
         callback = CustomJS(code='''
         if cb_data.word == 'apple':
            return 'red'
         return 'blue'
         ''')
         wc4 = WordCloud(source=data,wordCol="words", sizeCol="weights", color=callback)
         
    """,
    )
    fontWeight = Either(
        String,
        Instance(CustomJS),
        default="normal",
        help="the font weight to use, or a CustomJS that returns a Font weight(eg. 'bolder','600','normal') (see `cb_object`)",
    )
    classes = Either(
        String,
        Instance(CustomJS),
        help="a class name or function to use ... only works if using DOM elements, which are currently unsupported... so this does nothing for now",
    )
    weightFactor = Either(
        Instance(CustomJS),
        Float,
        help="""
    a multiplier to apply to the sizes or a CustomJS instance(see `cb_data`)
    
    .. code-block:: python
    
       # you can just specify a number (eg multiply all sizes by 12)
       wc = WordCloud(source=data,wordCol="words", sizeCol="weights", weightFactor=12)
       
       # or you can specify a callback (eg cube the given size)
       callback = CustomJS(code="return Math.pow(cb_data.size, 3))
       
    """,
    )

    rotateRatio = Float(
        help="the odds of a given word rotating between 0-1, if 1 then the word will ALWAYS rotate, if 0 it will NEVER rotate, at 0.2 it has a 20% chance of rotating",
        default=1,
    )
    minRotation = Float(help="the minimum amount(in radians) to rotate", default=0)
    maxRotation = Float(
        help="the maximum amount(in radians) to rotate", default=math.pi / 2.0
    )
    rotationSteps = Int(
        help="the number of slices to cut the rotation range into", default=32
    )
    gridSize = Float(
        help="the distance between words, the bigger the gridsize, the more distance between words.",
        default=16,
    )
    fontFamily = String(help="the fontFamily to use.", default="Times, serif")
    shape = Enum(*myEnum, help="the shape of the wordcloud", default="square")

    hover = Instance(
        CustomJS,
        help="""
    js callback to execute on word hover 1
    
    `cb_data` provides: `cb_data.word`, and `cb_data.weight`
    
    .. code-block:: python
    
       wordcloud.hover = CustomJS(code="console.log(`Hover On: ${cb_data.word} - x${cb_data.weight}`)")
    
  
    """,
    )
    click = Instance(
        CustomJS,
        help="""
    js callback to execute on word click
    
    .. note::
    
       this is **NOT** the same as :meth:`bokeh_wordcloud2.WordCloud2.on_click`, which runs inside the backend on a
       bokeh server, where as this attribute expects `CustomJS` that is run on the client.
    
    
    `cb_data` provides: `cb_data.word`, and `cb_data.weight`
    
    .. code-block:: python
    
       wordcloud.click = CustomJS(code='''
       console.log(`You Clicked!!!!: ${cb_data.word} - x${cb_data.weight}`)
       ''')
       
    """,
    )

    def __init__(self, **kw):
        super(WordCloud2, self).__init__(**kw)
        if "view" not in kw:
            self.view = CDSView(source=self.source)

    def on_click(self, python_callback):
        """
        bind a python callback to word clicks, this only works when running a bokeh server

        .. note::

           this is **NOT** the same as :attr:`bokeh_wordcloud2.WordCloud2.click`, which runs on the clients browser,
           where as this method expects a python function that is run on the bokeh-server.

        the function that recieves the call back will recieve  WordClick Event, that has a word and weight attribute

        .. code-block:: python

           def my_handler(event):
               print("Clicked Word: %r"%event.word)
               # update the view filters
               some_view.filters = [1,2,4,5,7,8]

           wordcloud.on_click(my_handler)

        :param python_callback: a python function to call when a word is clicked
        """
        self.on_event(WordClick, python_callback)
