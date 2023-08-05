(window.webpackJsonp=window.webpackJsonp||[]).push([[8],{1157:function(e,t,o){"use strict";(function(e){var r=o(93),n=o(500),i=o(506),l=o(52),s=o(0),c=o(604),a=o(1210),d=o.n(a),p=o(76),u=o(1221),m=o(1222),h=o(1673),b=o(1240),f=o(1241),g=o(1242),C=o(1250),x=o(1690),v=o(1265),k=o(44);const y=l.List(),w=l.Set(),E=Object(k.c)(i.a).attrs(e=>({className:e.isSelected?"selected":""}))`
  /*
   * Show the cell-toolbar-mask if hovering on cell,
   * cell was the last clicked
   */
  &:hover ${x.a}, &.selected ${x.a} {
    display: block;
  }
`;E.displayName="Cell";const M=k.c.div`
  background-color: darkblue;
  color: ghostwhite;
  padding: 9px 16px;

  font-size: 12px;
  line-height: 20px;
`;M.displayName="CellBanner";const O=Object(p.b)((e,{id:t,contentRef:o})=>{return e=>{const n=r.r.model(e,{contentRef:o});if(!n||"notebook"!==n.type)throw new Error("Cell components should not be used with non-notebook models");const i=n.kernelRef,l=r.r.notebook.cellById(n,{id:t});if(!l)throw new Error("cell not found inside cell map");const s=l.cell_type,c=l.get("outputs",y),a=r.r.notebook.cellPromptById(n,{id:t}),d="code"===s&&(l.getIn(["metadata","inputHidden"])||l.getIn(["metadata","hide_input"]))||!1,p="code"===s&&(0===c.size||l.getIn(["metadata","outputHidden"])),u="code"===s&&l.getIn(["metadata","outputExpanded"]),m=l.getIn(["metadata","tags"])||w,h=n.getIn(["cellPagers",t])||y;let b;if(i){const t=r.r.kernel(e,{kernelRef:i});t&&(b=t.channels)}return{cellFocused:n.cellFocused===t,cellStatus:n.transient.getIn(["cellMap",t,"status"]),cellType:s,channels:b,contentRef:o,editorFocused:n.editorFocused===t,executionCount:l.get("execution_count",null),outputExpanded:u,outputHidden:p,outputs:c,pager:h,prompt:a,source:l.get("source",""),sourceHidden:d,tags:m,theme:r.r.userTheme(e)}}},(e,{id:t,contentRef:o})=>{return e=>({focusAboveCell:()=>{e(r.a.focusPreviousCell({id:t,contentRef:o})),e(r.a.focusPreviousCellEditor({id:t,contentRef:o}))},focusBelowCell:()=>{e(r.a.focusNextCell({id:t,createCellIfUndefined:!0,contentRef:o})),e(r.a.focusNextCellEditor({id:t,contentRef:o}))},focusEditor:()=>e(r.a.focusCellEditor({id:t,contentRef:o})),selectCell:()=>e(r.a.focusCell({id:t,contentRef:o})),unfocusEditor:()=>e(r.a.focusCellEditor({id:void 0,contentRef:o})),changeCellType:n=>e(r.a.changeCellType({contentRef:o,id:t,to:n})),clearOutputs:()=>e(r.a.clearOutputs({id:t,contentRef:o})),deleteCell:()=>e(r.a.deleteCell({id:t,contentRef:o})),executeCell:()=>e(r.a.executeCell({id:t,contentRef:o})),toggleCellInputVisibility:()=>e(r.a.toggleCellInputVisibility({id:t,contentRef:o})),toggleCellOutputVisibility:()=>e(r.a.toggleCellOutputVisibility({id:t,contentRef:o})),toggleOutputExpansion:()=>e(r.a.toggleOutputExpansion({id:t,contentRef:o})),toggleParameterCell:()=>e(r.a.toggleParameterCell({id:t,contentRef:o})),sendInputReply:t=>e(r.a.sendInputReply({value:t})),updateOutputMetadata:(n,i,l)=>{e(r.a.updateOutputMetadata({id:t,contentRef:o,metadata:i,index:n,mediaType:l}))}})})(class extends s.PureComponent{constructor(){super(...arguments),this.toggleCellType=(()=>{this.props.changeCellType("markdown"===this.props.cellType?"code":"markdown")})}render(){const{executeCell:e,deleteCell:t,clearOutputs:o,toggleParameterCell:r,toggleCellInputVisibility:l,toggleCellOutputVisibility:c,toggleOutputExpansion:a,changeCellType:d,cellFocused:p,cellStatus:u,cellType:m,editorFocused:g,focusAboveCell:C,focusBelowCell:k,focusEditor:y,id:w,prompt:O,tags:R,theme:S,selectCell:T,unfocusEditor:N,contentRef:I,sourceHidden:D,sendInputReply:j}=this.props,F="busy"===u,A="queued"===u;let P=null;switch(m){case"code":P=s.createElement(s.Fragment,null,s.createElement(i.c,{hidden:this.props.sourceHidden},s.createElement(i.g,{counter:this.props.executionCount,running:F,queued:A}),s.createElement(i.i,null,s.createElement(h.a,{id:w,contentRef:I,focusAbove:C,focusBelow:k}))),s.createElement(i.f,null,this.props.pager.map((e,t)=>s.createElement(n.e,{data:e.data,metadata:e.metadata},s.createElement(n.b.Json,null),s.createElement(n.b.JavaScript,null),s.createElement(n.b.HTML,null),s.createElement(n.b.Markdown,null),s.createElement(n.b.LaTeX,null),s.createElement(n.b.SVG,null),s.createElement(n.b.Image,null),s.createElement(n.b.Plain,null)))),s.createElement(i.e,{hidden:this.props.outputHidden,expanded:this.props.outputExpanded},this.props.outputs.map((e,t)=>s.createElement(n.c,{output:e,key:t},s.createElement(v.a,{output_type:"display_data",cellId:w,contentRef:I,index:t}),s.createElement(v.a,{output_type:"execute_result",cellId:w,contentRef:I,index:t}),s.createElement(n.a,null),s.createElement(n.f,null)))),O&&s.createElement(n.d,Object.assign({},O,{submitPromptReply:j})));break;case"markdown":P=s.createElement(f.a,{focusAbove:C,focusBelow:k,focusEditor:y,cellFocused:p,editorFocused:g,unfocusEditor:N,source:this.props.source},s.createElement(i.i,null,s.createElement(h.a,{id:w,contentRef:I,focusAbove:C,focusBelow:k})));break;case"raw":P=s.createElement(i.i,null,s.createElement(h.a,{id:w,contentRef:I,focusAbove:C,focusBelow:k}));break;default:P=s.createElement("pre",null,this.props.source)}return s.createElement(b.a,{focused:p,onClick:T},s.createElement(E,{isSelected:p},R.has("parameters")?s.createElement(M,null,"Papermill - Parametrized"):null,R.has("default parameters")?s.createElement(M,null,"Papermill - Default Parameters"):null,s.createElement(x.b,{type:m,cellFocused:p,executeCell:e,deleteCell:t,clearOutputs:o,toggleParameterCell:r,toggleCellInputVisibility:l,toggleCellOutputVisibility:c,toggleOutputExpansion:a,changeCellType:this.toggleCellType,sourceHidden:D}),P))}}),R=k.c.div`
  padding-top: var(--nt-spacing-m, 10px);
  padding-left: var(--nt-spacing-m, 10px);
  padding-right: var(--nt-spacing-m, 10px);
`;class S extends s.PureComponent{constructor(e){super(e),this.keyDown=this.keyDown.bind(this)}componentDidMount(){document.addEventListener("keydown",this.keyDown)}componentWillUnmount(){document.removeEventListener("keydown",this.keyDown)}keyDown(t){if(13!==t.keyCode)return;const{executeFocusedCell:o,focusNextCell:r,focusNextCellEditor:n,contentRef:i,cellOrder:l,focusedCell:s,cellMap:c}=this.props;let a=t.ctrlKey;if("darwin"===e.platform&&(a=(t.metaKey||t.ctrlKey)&&!(t.metaKey&&t.ctrlKey)),(t.shiftKey||a)&&!(t.shiftKey&&a)&&(t.preventDefault(),o({contentRef:i}),t.shiftKey)){const e=l.indexOf(s),t=l.get(e+1),o=c.get(t);r({id:void 0,createCellIfUndefined:!0,contentRef:i}),(void 0===o||o&&"code"===o.get("cell_type"))&&n({id:s||void 0,contentRef:i})}}render(){return s.createElement(s.Fragment,null,s.createElement(g.a,{contentRef:this.props.contentRef}),s.createElement(R,null,s.createElement(u.a,{id:this.props.cellOrder.get(0),above:!0,contentRef:this.props.contentRef}),this.props.cellOrder.map(e=>s.createElement("div",{className:"cell-container",key:`cell-container-${e}`},s.createElement(m.a,{moveCell:this.props.moveCell,id:e,focusCell:this.props.focusCell,contentRef:this.props.contentRef},s.createElement(O,{id:e,contentRef:this.props.contentRef})),s.createElement(u.a,{key:`creator-${e}`,id:e,above:!1,contentRef:this.props.contentRef})))),s.createElement(C.a,{contentRef:this.props.contentRef}),function(e){switch(e){case"dark":return s.createElement(i.b,null);case"light":default:return s.createElement(i.d,null)}}(this.props.theme))}}S.defaultProps={theme:"light"};const T=Object(c.DragDropContext)(d.a)(S);t.a=Object(p.b)((e,t)=>{const{contentRef:o}=t;if(!o)throw new Error("<Notebook /> has to have a contentRef");return e=>{const t=r.r.content(e,{contentRef:o}),n=r.r.model(e,{contentRef:o});if(!n||!t)throw new Error("<Notebook /> has to have content & model that are notebook types");const i=r.r.userTheme(e);if("notebook"!==n.type)return{cellOrder:l.List(),contentRef:o,theme:i,focusedCell:null,cellMap:l.Map()};if("notebook"!==n.type)throw new Error("<Notebook /> has to have content & model that are notebook types");const s=r.r.notebook.cellFocused(n),c=r.r.notebook.cellMap(n);return{cellOrder:n.notebook.cellOrder,contentRef:o,theme:i,focusedCell:s,cellMap:c}}},e=>({executeFocusedCell:t=>e(r.a.executeFocusedCell(t)),focusCell:t=>e(r.a.focusCell(t)),focusNextCell:t=>e(r.a.focusNextCell(t)),focusNextCellEditor:t=>e(r.a.focusNextCellEditor(t)),moveCell:t=>e(r.a.moveCell(t)),updateOutputMetadata:t=>e(r.a.updateOutputMetadata(t))}))(T)}).call(this,o(81))},1221:function(e,t,o){"use strict";var r=o(62),n=o(211),i=o(0),l=o(76),s=o(44);const c=s.c.div`
  display: none;
  background: var(--theme-cell-creator-bg);
  box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.5);
  pointer-events: all;
  position: relative;
  top: -5px;

  button {
    display: inline-block;

    width: 22px;
    height: 20px;
    padding: 0px 4px;

    text-align: center;

    border: none;
    outline: none;
    background: none;
  }

  button span {
    font-size: 15px;
    line-height: 1;

    color: var(--theme-cell-creator-fg);
  }

  button span:hover {
    color: var(--theme-cell-creator-fg-hover);
  }

  .octicon {
    transition: color 0.5s;
  }
`,a=s.c.div`
  display: block;
  position: relative;
  overflow: visible;
  height: 0px;

  @media print{
    display: none;
  }
`,d=s.c.div`
  position: relative;
  overflow: visible;
  top: -10px;
  height: 60px;
  text-align: center;

  &:hover ${c} {
    display: inline-block;
  }
`;class p extends i.PureComponent{constructor(){super(...arguments),this.createMarkdownCell=(()=>{this.props.createCell("markdown")}),this.createCodeCell=(()=>{this.props.createCell("code")})}render(){return i.createElement(a,null,i.createElement(d,null,i.createElement(c,null,i.createElement("button",{onClick:this.createMarkdownCell,title:"create text cell",className:"add-text-cell"},i.createElement("span",{className:"octicon"},i.createElement(n.g,null))),i.createElement("button",{onClick:this.createCodeCell,title:"create code cell",className:"add-code-cell"},i.createElement("span",{className:"octicon"},i.createElement(n.c,null))))))}}t.a=Object(l.b)(null,e=>({createCellAbove:t=>e(r.createCellAbove(t)),createCellAppend:t=>e(r.createCellAppend(t)),createCellBelow:t=>e(r.createCellBelow(t))}))(class extends i.PureComponent{constructor(){super(...arguments),this.createCell=(e=>{const{above:t,createCellBelow:o,createCellAppend:r,createCellAbove:n,id:i,contentRef:l}=this.props;void 0!==i&&"string"==typeof i?t?n({cellType:e,id:i,contentRef:l}):o({cellType:e,id:i,source:"",contentRef:l}):r({cellType:e,contentRef:l})})}render(){return i.createElement(p,{above:this.props.above,createCell:this.createCell})}})},1222:function(e,t,o){"use strict";var r=o(0),n=o(604),i=o(44);const l=["data:image/png;base64,","iVBORw0KGgoAAAANSUhEUgAAADsAAAAzCAYAAAApdnDeAAAAAXNSR0IArs4c6QAA","AwNJREFUaAXtmlFL3EAUhe9MZptuoha3rLWgYC0W+lj/T3+26INvXbrI2oBdE9km","O9Nzxu1S0LI70AQScyFmDDfkfvdMZpNwlCCccwq7f21MaVM4FPtkU0o59RdoJBMx","WZINBg+DQWGKCAk+2kIKFh9JlSzLYVmOilEpR1Kh/iUbQFiNQTSbzWJrbYJximOJ","cSaulpVRoqh4K8JhjprIVJWqFlCpQNG51roYj8cLjJcGf5RMZWC1TYw1o2LxcEmy","0jeEo3ZFWVHIx0ji4eeKHFOx8l4sVVVZnBE6tWLHq7xO7FY86YpPeVjeo5y61tlR","JyhXEOQhF/lw6BGWixHvUWXVTpdgyUMu8q1h/ZJbqQhdiLsESx4FLvL9gcV6q3Cs","0liq2IHuBHjItYIV3rMvJnrYrkrdK9sr24EO9NO4AyI+i/CilOXbTi1xeXXFTyAS","GSOfzs42XmM+v5fJ5JvP29/fl8PDw43nhCbUpuzFxYXs7OxKmqZb1WQGkc/P80K+","T6dbnROaVJuyfPY+Pj7aup7h66HP/1Uu5O7u59bnhSTWpmxIEU3l9rBNdbrp6/TK","Nt3xpq7XK9tUp5u+Tm2/s/jYJdfX12LwBHVycrKRK89zmeJhYnZ7K3Fcz3e/2mDP","z7/waZEf8zaC+gSkKa3l4OBA3uztbXdOYFZtsKcfToNKSZNUPp6GnRN0AST3C1Ro","x9qS3yvbFqVC6+yVDe1YW/J7ZduiVGidvbKhHWtLfq9sW5QKrdMri9cxB6OFhQmO","TrDuBHjIRT5CEZZj0i7xOkYnWGeCPOQiHqC8lc/R60cLnNPuvjOkns7dk4t8/Jfv","s46mRlWqQiudxebVV3gAj7C9hXsmgZeztnfe/91YODEr3IoF/JY/sE2gbGaVLci3","hh0tRtWNvsm16JmNcOs6N9dW72LP7yOtWbEhjAUkZ+icoJ5HbE6+NSxMjKWe6cKb","GkUWgMwiFbXSlRpFkXelUlF4F70rVd7Bd4oZ/LL8xiDmtPV2Nwyf2zOlTfHERY7i","Haa1+w2+iFqx0aIgvgAAAABJRU5ErkJggg=="].join(""),s={beginDrag:e=>({id:e.id})},c=i.c.div.attrs({role:"presentation"})`
  position: absolute;
  z-index: 200;
  width: var(--prompt-width, 50px);
  height: 100%;
  cursor: move;
`,a=i.c.div.attrs(e=>({style:{opacity:e.isDragging?.25:1,borderTop:e.isOver&&e.hoverUpperHalf?"3px lightgray solid":"3px transparent solid",borderBottom:e.isOver&&!e.hoverUpperHalf?"3px lightgray solid":"3px transparent solid"}}))`
  position: relative;
  padding: 10px;
`;function d(e,t,o){const r=o.getBoundingClientRect(),n=(r.bottom-r.top)/2;return t.getClientOffset().y-r.top<n}const p={drop(e,t,o){if(t){const r=d(0,t,o.el);e.moveCell({id:t.getItem().id,destinationId:e.id,above:r,contentRef:e.contentRef})}},hover(e,t,o){t&&o.setState({hoverUpperHalf:d(0,t,o.el)})}};const u=Object(n.DragSource)("CELL",s,function(e,t){return{connectDragSource:e.dragSource(),isDragging:t.isDragging(),connectDragPreview:e.dragPreview()}}),m=Object(n.DropTarget)("CELL",p,function(e,t){return{connectDropTarget:e.dropTarget(),isOver:t.isOver()}});t.a=u(m(class extends r.Component{constructor(){super(...arguments),this.state={hoverUpperHalf:!0},this.selectCell=(()=>{const{focusCell:e,id:t,contentRef:o}=this.props;e({id:t,contentRef:o})})}componentDidMount(){const e=this.props.connectDragPreview,t=new window.Image;t.src=l,t.onload=(()=>{e(t)})}render(){return this.props.connectDropTarget(r.createElement("div",null,r.createElement(a,{isDragging:this.props.isDragging,hoverUpperHalf:this.state.hoverUpperHalf,isOver:this.props.isOver,ref:e=>{this.el=e}},this.props.connectDragSource(r.createElement("div",null,r.createElement(c,{onClick:this.selectCell}))),this.props.children)))}}))},1239:function(e,t,o){"use strict";o.r(t);var r=o(65),n=o.n(r);o(621),o(619);n.a.defineMode("ipython",(e,t)=>{const o=Object.assign({},t,{name:"python",singleOperators:new RegExp("^[\\+\\-\\*/%&|@\\^~<>!\\?]"),identifiers:new RegExp("^[_A-Za-z¡-￿][_A-Za-z0-9¡-￿]*")});return n.a.getMode(e,o)},"python"),n.a.defineMIME("text/x-ipython","ipython")},1240:function(e,t,o){"use strict";o.d(t,"a",function(){return n});var r=o(0);class n extends r.Component{constructor(){super(...arguments),this.el=null}scrollIntoViewIfNeeded(e){const t=this.el&&this.el.parentElement&&this.el.parentElement.querySelector(":hover")===this.el;this.props.focused&&e!==this.props.focused&&!t&&(this.el&&"scrollIntoViewIfNeeded"in this.el?this.el.scrollIntoViewIfNeeded():this.el&&this.el.scrollIntoView())}componentDidUpdate(e){this.scrollIntoViewIfNeeded(e.focused)}componentDidMount(){this.scrollIntoViewIfNeeded()}render(){return r.createElement("div",{onClick:this.props.onClick,role:"presentation",ref:e=>{this.el=e}},this.props.children)}}},1241:function(e,t,o){"use strict";o.d(t,"a",function(){return c});var r=o(712),n=o(506),i=o(0),l=o.n(i);const s=()=>{};class c extends l.a.Component{constructor(e){super(e),this.state={view:!0},this.openEditor=this.openEditor.bind(this),this.editorKeyDown=this.editorKeyDown.bind(this),this.renderedKeyDown=this.renderedKeyDown.bind(this),this.closeEditor=this.closeEditor.bind(this)}componentDidMount(){this.updateFocus()}componentWillReceiveProps(e){this.setState({view:!e.editorFocused})}componentDidUpdate(){this.updateFocus()}updateFocus(){this.rendered&&this.state&&this.state.view&&this.props.cellFocused&&(this.rendered.focus(),this.props.editorFocused&&this.openEditor())}editorKeyDown(e){const t=e.shiftKey,o=e.ctrlKey;(t||o)&&"Enter"===e.key&&this.closeEditor()}closeEditor(){this.setState({view:!0}),this.props.unfocusEditor()}openEditor(){this.setState({view:!1}),this.props.focusEditor()}renderedKeyDown(e){const t=e.shiftKey,o=e.ctrlKey;if(!t&&!o||"Enter"!==e.key)switch(e.key){case"Enter":return this.openEditor(),void e.preventDefault();case"ArrowUp":this.props.focusAbove();break;case"ArrowDown":this.props.focusBelow()}else{if(this.state.view)return;this.closeEditor()}}render(){const e=this.props.source;return this.state&&this.state.view?l.a.createElement("div",{onDoubleClick:this.openEditor,onKeyDown:this.renderedKeyDown,ref:e=>{this.rendered=e},tabIndex:this.props.cellFocused?0:void 0,style:{outline:"none"}},l.a.createElement(n.e,null,l.a.createElement(r.a,{source:e||"*Empty markdown cell, double click me to add content.*"}))):l.a.createElement("div",{onKeyDown:this.editorKeyDown},l.a.createElement(n.c,null,l.a.createElement(n.h,null),this.props.children),l.a.createElement(n.e,{hidden:""===e},l.a.createElement(r.a,{source:e||"*Empty markdown cell, double click me to add content.*"})))}}c.defaultProps={cellFocused:!1,editorFocused:!1,focusAbove:s,focusBelow:s,focusEditor:s,unfocusEditor:s,source:""}},1242:function(e,t,o){"use strict";var r=o(107),n=o(0),i=o.n(n),l=o(1243),s=o(76);t.a=Object(s.b)((e,t)=>{const{contentRef:o}=t;return e=>({filePath:r.filepath(e,{contentRef:o})})})(class extends i.a.PureComponent{render(){return i.a.createElement(i.a.Fragment,null,i.a.createElement(l.Helmet,null,i.a.createElement("base",{href:this.props.filePath||"."})))}})},1250:function(e,t,o){"use strict";var r=o(107),n=o(1251),i=o.n(n),l=o(0),s=o.n(l),c=o(76),a=o(44);const d=a.c.div`
  float: left;
  display: block;
  padding-left: 10px;
`,p=a.c.div`
  float: right;
  padding-right: 10px;
  display: block;
`,u=a.c.div`
  padding-top: 8px;
  position: fixed;
  bottom: 0;
  left: 0;
  width: 100%;
  font-size: 12px;
  line-height: 0.5em;
  background: var(--status-bar);
  z-index: 99;
  @media print {
    display: none;
  }
`;t.a=Object(c.b)((e,t)=>{const{contentRef:o}=t;return e=>{const t=r.content(e,{contentRef:o});if(!t||"notebook"!==t.type)return{kernelStatus:"not connected",kernelSpecDisplayName:"no kernel",lastSaved:null};const n=t.model.kernelRef;let i=null;n&&(i=r.kernel(e,{kernelRef:n}));const l=t&&t.lastSaved?t.lastSaved:null,s=null!=i&&null!=i.status?i.status:"not connected";let c=" ";return"not connected"===s?c="no kernel":null!=i&&null!=i.kernelSpecName?c=i.kernelSpecName:t&&"notebook"===t.type&&(c=r.notebook.displayName(t.model)||" "),{kernelSpecDisplayName:c,kernelStatus:s,lastSaved:l}}})(class extends s.a.Component{shouldComponentUpdate(e){return this.props.lastSaved!==e.lastSaved||this.props.kernelStatus!==e.kernelStatus}render(){const e=this.props.kernelSpecDisplayName||"Loading...";return s.a.createElement(u,null,s.a.createElement(p,null,this.props.lastSaved?s.a.createElement("p",null," Last saved ",i()(this.props.lastSaved)," "):s.a.createElement("p",null," Not saved yet ")),s.a.createElement(d,null,s.a.createElement("p",null,e," | ",this.props.kernelStatus)))}})},1265:function(e,t,o){"use strict";var r=o(0),n=o.n(r),i=o(76),l=o(93),s=o(369);const c=Object(i.b)((e,t)=>{const{contentRef:o,index:r,cellId:n}=t,i=Object(s.default)(e=>e?e.toJS():{});return e=>{const t=e.core.entities.contents.byRef.getIn([o,"model","notebook","cellMap",n,"outputs",r],null);if(!t||"display_data"!==t.output_type&&"execute_result"!==t.output_type)return console.warn("connected transform media managed to get a non media bundle output"),{Media:()=>null};const s=l.r.transformsById(e),c=l.r.displayOrder(e),a=l.r.userTheme(e),d=((e,t,o)=>{const r=e.data;return t.find(e=>r.hasOwnProperty(e)&&(o.hasOwnProperty(e)||o.get(e,!1)))})(t,c,s);if(d){const o=i(t.metadata.get(d)),r=t.data[d];return{Media:l.r.transform(e,{id:d}),mediaType:d,data:r,metadata:o,theme:a}}return{Media:()=>null,mediaType:d,output:t,theme:a}}},(e,t)=>{const{cellId:o,contentRef:r,index:n}=t;return e=>({mediaActions:{onMetadataChange:(t,i)=>{e(l.a.updateOutputMetadata({id:o,contentRef:r,metadata:t,index:n,mediaType:i}))}}})})(e=>{const{Media:t,mediaActions:o,mediaType:r,data:i,metadata:l,theme:s}=e;return r&&i?n.a.createElement(t,Object.assign({},o,{data:i,metadata:l,theme:s})):null});t.a=c},1673:function(e,t,o){"use strict";var r=o(62),n=o(65),i=o.n(n);const l={value:!1,mode:!0,theme:!1,indentUnit:!0,smartIndent:!0,tabSize:!0,indentWithTabs:!0,electricChars:!0,rtlMoveVisually:!0,keyMap:!0,extraKeys:!1,lineWrapping:!0,lineNumbers:!0,firstLineNumber:!0,lineNumberFormatter:!0,gutters:!0,fixedGutter:!0,readOnly:!0,showCursorWhenSelecting:!0,undoDepth:!0,historyEventDelay:!0,tabindex:!0,autofocus:!0,dragDrop:!0,onDragEvent:!0,onKeyEvent:!0,cursorBlinkRate:!0,cursorHeight:!0,workTime:!0,workDelay:!0,pollInterval:!0,flattenSpans:!0,maxHighlightLength:!0,viewportMargin:!0,lint:!0,placeholder:!0,showHint:!0,hintOptions:!1};function s(e){return!!l[e]}var c=o(168),a=o(0),d=o(3),p=o.n(d),u=o(1710),m=o(1687),h=o(169),b=o(1695),f=o(202),g=o(1693),C=o(1735),x=o(1711),v=o(1694),k=o(1712),y=o(167),w=o(1698);const E={8:"backspace",9:"tab",13:"enter",16:"shift",17:"ctrl",18:"alt",19:"pause",20:"capslock",27:"escape",32:"space",33:"pageup",34:"pagedown",35:"end",36:"home",37:"left",38:"up",39:"right",40:"down",45:"insert",46:"delete",91:"left window key",92:"right window key",93:"select",107:"add",109:"subtract",110:"decimal point",111:"divide",112:"f1",113:"f2",114:"f3",115:"f4",116:"f5",117:"f6",118:"f7",119:"f8",120:"f9",121:"f10",122:"f11",123:"f12",144:"numlock",145:"scrolllock",186:"semicolon",187:"equalsign",188:"comma",189:"dash",192:"graveaccent",220:"backslash",222:"quote"};var M=o(165),O=o(74),R=o(1728),S=o(1730),T=o(44);function N(e){return a.createElement(a.Fragment,null,e.type?a.createElement(I,{type:e.type}):null,e.displayText||e.text)}const I=T.c.span.attrs(e=>({className:`completion-type-${e.type}`,title:e.type}))`
  & {
    background: transparent;
    border: transparent 1px solid;
    width: 17px;
    height: 17px;
    margin: 0;
    padding: 0;
    display: inline-block;
    margin-right: 5px;
    top: 18px;
  }

  &:before {
    /* When experimental type completion isn't available render the left side as "nothing" */
    content: " ";
    bottom: 1px;
    left: 4px;
    position: relative;
    color: white;
  }
  /* color and content for each type of completion */
  &.completion-type-keyword:before {
    content: "K";
  }
  &.completion-type-keyword {
    background-color: darkred;
  }
  &.completion-type-class:before {
    content: "C";
  }
  &.completion-type-class {
    background-color: blueviolet;
  }
  &.completion-type-module:before {
    content: "M";
  }
  &.completion-type-module {
    background-color: chocolate;
  }
  &.completion-type-statement:before {
    content: "S";
  }
  &.completion-type-statement {
    background-color: forestgreen;
  }
  &.completion-type-function:before {
    content: "ƒ";
  }
  &.completion-type-function {
    background-color: yellowgreen;
  }
  &.completion-type-instance:before {
    content: "I";
  }
  &.completion-type-instance {
    background-color: teal;
  }
  &.completion-type-null:before {
    content: "ø";
  }
  &.completion-type-null {
    background-color: black;
  }
`;let D=(e,t)=>{let o=e;for(let r=0;r+1<t.length&&r<e;r++){const e=t.charCodeAt(r);if(e>=55296&&e<=56319){const e=t.charCodeAt(r+1);e>=56320&&e<=57343&&(o--,r++)}}return o},j=(e,t)=>{let o=e;for(let e=0;e+1<t.length&&e<o;e++){const r=t.charCodeAt(e);if(r>=55296&&r<=56319){const r=t.charCodeAt(e+1);r>=56320&&r<=57343&&(o++,e++)}}return o};function F(e,t){t.pick()}1==="𝐚".length&&(j=D=((e,t)=>e));const A=e=>t=>{let o=t.cursor_start,r=t.cursor_end;if(null===r)r=e.indexFromPos(e.getCursor()),null===o?o=r:o<0&&(o=r+o);else{const t=e.getValue();r=j(r,t),o=j(o,t)}const n=e.posFromIndex(o),i=e.posFromIndex(r);let l=t.matches;function s(e,t,o){p.a.render(a.createElement(N,Object.assign({},o)),e)}return t.metadata&&t.metadata._jupyter_types_experimental&&(l=t.metadata._jupyter_types_experimental),{list:l.map(e=>"string"==typeof e?{to:i,from:n,text:e,render:s}:Object.assign({to:i,from:n,render:s},e)),from:n,to:i}};const P=(e,t)=>Object(M.createMessage)("complete_request",{content:{code:e,cursor_pos:t}});function z(e,t){const o=t.getCursor();let r=t.indexFromPos(o);const n=t.getValue();return r=D(r,n),function(e,t,o){const r=e.pipe(Object(M.childOf)(o),Object(M.ofMessageType)("complete_reply"),Object(y.a)(e=>e.content),Object(R.a)(),Object(y.a)(A(t)),Object(S.a)(15e3));return O.a.create(t=>{const n=r.subscribe(t);return e.next(o),n})}(e,t,P(n,r))}function V(e,t){const o=t.getCursor(),r=D(t.indexFromPos(o),t.getValue());return function(e,t,o){const r=e.pipe(Object(M.childOf)(o),Object(M.ofMessageType)("inspect_reply"),Object(y.a)(e=>e.content),Object(R.a)(),Object(y.a)(e=>({dict:e.data})));return O.a.create(t=>{const n=r.subscribe(t);return e.next(o),n})}(e,0,function(e,t){return Object(M.createMessage)("inspect_request",{content:{code:e,cursor_pos:t,detail_level:0}})}(t.getValue(),r))}const B=T.c.textarea.attrs({autoComplete:"off"})`
  font-family: "Dank Mono", dm, "Source Code Pro", "Monaco", monospace;
  font-size: 14px;
  line-height: 20px;

  height: inherit;

  background: none;

  border: none;
  overflow: hidden;

  -webkit-scrollbar: none;
  -webkit-box-shadow: none;
  -moz-box-shadow: none;
  box-shadow: none;
  width: 100%;
  resize: none;
  padding: 10px 0 5px 10px;
  letter-spacing: 0.3px;
  word-spacing: 0px;

  &:focus {
    outline: none;
    border: none;
  }
`;var K=o(500);const H=T.c.button`
  float: right;
  font-size: 11.5px;
  position: absolute;
  right: 0px;
  top: 0px;
`,U=T.c.div`
  background-color: var(--theme-app-bg, #2b2b2b);
  box-shadow: 2px 2px 50px rgba(0, 0, 0, 0.2);
  float: right;
  height: auto;
  left: ${e=>e.cursorCoords.left}px;
  margin: 30px 20px 50px 20px;
  padding: 20px 20px 50px 20px;
  position: absolute;
  top: ${e=>e.cursorCoords.top}px;
  white-space: pre-wrap;
  width: auto;
  z-index: 9999999;
`;function L({bundle:e,cursorCoords:t,deleteTip:o}){return e&&t?a.createElement(U,{className:"CodeMirror-hint",tabIndex:0,onKeyDown:e=>{"Escape"===e.key&&o()},cursorCoords:t},a.createElement(K.e,{data:e,metadata:{expanded:!0}},a.createElement(K.b.Markdown,null),a.createElement(K.b.Plain,null)),a.createElement(H,{onClick:o},"✕")):null}T.a`
  /* BASICS */

  .CodeMirror {
    /* Set height, width, borders, and global font properties here */
    font-family: monospace;
    height: 300px;
    color: black;
    direction: ltr;
  }

  /* PADDING */

  .CodeMirror-lines {
    padding: 4px 0; /* Vertical padding around content */
  }
  .CodeMirror pre {
    padding: 0 4px; /* Horizontal padding of content */
  }

  .CodeMirror-scrollbar-filler,
  .CodeMirror-gutter-filler {
    background-color: white; /* The little square between H and V scrollbars */
  }

  /* GUTTER */

  .CodeMirror-gutters {
    border-right: 1px solid #ddd;
    background-color: #f7f7f7;
    white-space: nowrap;
  }
  .CodeMirror-linenumbers {
  }
  .CodeMirror-linenumber {
    padding: 0 3px 0 5px;
    min-width: 20px;
    text-align: right;
    color: #999;
    white-space: nowrap;
  }

  .CodeMirror-guttermarker {
    color: black;
  }
  .CodeMirror-guttermarker-subtle {
    color: #999;
  }

  /* CURSOR */

  .CodeMirror-cursor {
    border-left: 1px solid black;
    border-right: none;
    width: 0;
  }
  /* Shown when moving in bi-directional text */
  .CodeMirror div.CodeMirror-secondarycursor {
    border-left: 1px solid silver;
  }
  .cm-fat-cursor .CodeMirror-cursor {
    width: auto;
    border: 0 !important;
    background: #7e7;
  }
  .cm-fat-cursor div.CodeMirror-cursors {
    z-index: 1;
  }
  .cm-fat-cursor-mark {
    background-color: rgba(20, 255, 20, 0.5);
    -webkit-animation: blink 1.06s steps(1) infinite;
    -moz-animation: blink 1.06s steps(1) infinite;
    animation: blink 1.06s steps(1) infinite;
  }
  .cm-animate-fat-cursor {
    width: auto;
    border: 0;
    -webkit-animation: blink 1.06s steps(1) infinite;
    -moz-animation: blink 1.06s steps(1) infinite;
    animation: blink 1.06s steps(1) infinite;
    background-color: #7e7;
  }
  @-moz-keyframes blink {
    0% {
    }
    50% {
      background-color: transparent;
    }
    100% {
    }
  }
  @-webkit-keyframes blink {
    0% {
    }
    50% {
      background-color: transparent;
    }
    100% {
    }
  }
  @keyframes blink {
    0% {
    }
    50% {
      background-color: transparent;
    }
    100% {
    }
  }

  /* Can style cursor different in overwrite (non-insert) mode */
  .CodeMirror-overwrite .CodeMirror-cursor {
  }

  .cm-tab {
    display: inline-block;
    text-decoration: inherit;
  }

  .CodeMirror-rulers {
    position: absolute;
    left: 0;
    right: 0;
    top: -50px;
    bottom: -20px;
    overflow: hidden;
  }
  .CodeMirror-ruler {
    border-left: 1px solid #ccc;
    top: 0;
    bottom: 0;
    position: absolute;
  }

  /* DEFAULT THEME */

  .cm-s-default .cm-header {
    color: blue;
  }
  .cm-s-default .cm-quote {
    color: #090;
  }
  .cm-negative {
    color: #d44;
  }
  .cm-positive {
    color: #292;
  }
  .cm-header,
  .cm-strong {
    font-weight: bold;
  }
  .cm-em {
    font-style: italic;
  }
  .cm-link {
    text-decoration: underline;
  }
  .cm-strikethrough {
    text-decoration: line-through;
  }

  .cm-s-default .cm-keyword {
    color: #708;
  }
  .cm-s-default .cm-atom {
    color: #219;
  }
  .cm-s-default .cm-number {
    color: #164;
  }
  .cm-s-default .cm-def {
    color: #00f;
  }
  .cm-s-default .cm-variable,
  .cm-s-default .cm-punctuation,
  .cm-s-default .cm-property,
  .cm-s-default .cm-operator {
  }
  .cm-s-default .cm-variable-2 {
    color: #05a;
  }
  .cm-s-default .cm-variable-3,
  .cm-s-default .cm-type {
    color: #085;
  }
  .cm-s-default .cm-comment {
    color: #a50;
  }
  .cm-s-default .cm-string {
    color: #a11;
  }
  .cm-s-default .cm-string-2 {
    color: #f50;
  }
  .cm-s-default .cm-meta {
    color: #555;
  }
  .cm-s-default .cm-qualifier {
    color: #555;
  }
  .cm-s-default .cm-builtin {
    color: #30a;
  }
  .cm-s-default .cm-bracket {
    color: #997;
  }
  .cm-s-default .cm-tag {
    color: #170;
  }
  .cm-s-default .cm-attribute {
    color: #00c;
  }
  .cm-s-default .cm-hr {
    color: #999;
  }
  .cm-s-default .cm-link {
    color: #00c;
  }

  .cm-s-default .cm-error {
    color: #f00;
  }
  .cm-invalidchar {
    color: #f00;
  }

  .CodeMirror-composing {
    border-bottom: 2px solid;
  }

  /* Default styles for common addons */

  div.CodeMirror span.CodeMirror-matchingbracket {
    color: #0b0;
  }
  div.CodeMirror span.CodeMirror-nonmatchingbracket {
    color: #a22;
  }
  .CodeMirror-matchingtag {
    background: rgba(255, 150, 0, 0.3);
  }
  .CodeMirror-activeline-background {
    background: #e8f2ff;
  }

  /* STOP */

  /* The rest of this file contains styles related to the mechanics of
   the editor. You probably shouldn't touch them. */

  .CodeMirror {
    position: relative;
    overflow: hidden;
    background: white;
  }

  .CodeMirror-scroll {
    overflow: scroll !important; /* Things will break if this is overridden */
    /* 30px is the magic margin used to hide the element's real scrollbars */
    /* See overflow: hidden in .CodeMirror */
    margin-bottom: -30px;
    margin-right: -30px;
    padding-bottom: 30px;
    height: 100%;
    outline: none; /* Prevent dragging from highlighting the element */
    position: relative;
  }
  .CodeMirror-sizer {
    position: relative;
    border-right: 30px solid transparent;
  }

  /* The fake, visible scrollbars. Used to force redraw during scrolling
   before actual scrolling happens, thus preventing shaking and
   flickering artifacts. */
  .CodeMirror-vscrollbar,
  .CodeMirror-hscrollbar,
  .CodeMirror-scrollbar-filler,
  .CodeMirror-gutter-filler {
    position: absolute;
    z-index: 6;
    display: none;
  }
  .CodeMirror-vscrollbar {
    right: 0;
    top: 0;
    overflow-x: hidden;
    overflow-y: scroll;
  }
  .CodeMirror-hscrollbar {
    bottom: 0;
    left: 0;
    overflow-y: hidden;
    overflow-x: scroll;
  }
  .CodeMirror-scrollbar-filler {
    right: 0;
    bottom: 0;
  }
  .CodeMirror-gutter-filler {
    left: 0;
    bottom: 0;
  }

  .CodeMirror-gutters {
    position: absolute;
    left: 0;
    top: 0;
    min-height: 100%;
    z-index: 3;
  }
  .CodeMirror-gutter {
    white-space: normal;
    height: 100%;
    display: inline-block;
    vertical-align: top;
    margin-bottom: -30px;
  }
  .CodeMirror-gutter-wrapper {
    position: absolute;
    z-index: 4;
    background: none !important;
    border: none !important;
  }
  .CodeMirror-gutter-background {
    position: absolute;
    top: 0;
    bottom: 0;
    z-index: 4;
  }
  .CodeMirror-gutter-elt {
    position: absolute;
    cursor: default;
    z-index: 4;
  }
  .CodeMirror-gutter-wrapper ::selection {
    background-color: transparent;
  }
  .CodeMirror-gutter-wrapper ::-moz-selection {
    background-color: transparent;
  }

  .CodeMirror-lines {
    cursor: text;
    min-height: 1px; /* prevents collapsing before first draw */
  }
  .CodeMirror pre {
    /* Reset some styles that the rest of the page might have set */
    -moz-border-radius: 0;
    -webkit-border-radius: 0;
    border-radius: 0;
    border-width: 0;
    background: transparent;
    font-family: inherit;
    font-size: inherit;
    margin: 0;
    white-space: pre;
    word-wrap: normal;
    line-height: inherit;
    color: inherit;
    z-index: 2;
    position: relative;
    overflow: visible;
    -webkit-tap-highlight-color: transparent;
    -webkit-font-variant-ligatures: contextual;
    font-variant-ligatures: contextual;
  }
  .CodeMirror-wrap pre {
    word-wrap: break-word;
    white-space: pre-wrap;
    word-break: normal;
  }

  .CodeMirror-linebackground {
    position: absolute;
    left: 0;
    right: 0;
    top: 0;
    bottom: 0;
    z-index: 0;
  }

  .CodeMirror-linewidget {
    position: relative;
    z-index: 2;
    padding: 0.1px; /* Force widget margins to stay inside of the container */
  }

  .CodeMirror-widget {
  }

  .CodeMirror-rtl pre {
    direction: rtl;
  }

  .CodeMirror-code {
    outline: none;
  }

  /* Force content-box sizing for the elements where we expect it */
  .CodeMirror-scroll,
  .CodeMirror-sizer,
  .CodeMirror-gutter,
  .CodeMirror-gutters,
  .CodeMirror-linenumber {
    -moz-box-sizing: content-box;
    box-sizing: content-box;
  }

  .CodeMirror-measure {
    position: absolute;
    width: 100%;
    height: 0;
    overflow: hidden;
    visibility: hidden;
  }

  .CodeMirror-cursor {
    position: absolute;
    pointer-events: none;
  }
  .CodeMirror-measure pre {
    position: static;
  }

  div.CodeMirror-cursors {
    visibility: hidden;
    position: relative;
    z-index: 3;
  }
  div.CodeMirror-dragcursors {
    visibility: visible;
  }

  .CodeMirror-focused div.CodeMirror-cursors {
    visibility: visible;
  }

  .CodeMirror-selected {
    background: #d9d9d9;
  }
  .CodeMirror-focused .CodeMirror-selected {
    background: #d7d4f0;
  }
  .CodeMirror-crosshair {
    cursor: crosshair;
  }
  .CodeMirror-line::selection,
  .CodeMirror-line > span::selection,
  .CodeMirror-line > span > span::selection {
    background: #d7d4f0;
  }
  .CodeMirror-line::-moz-selection,
  .CodeMirror-line > span::-moz-selection,
  .CodeMirror-line > span > span::-moz-selection {
    background: #d7d4f0;
  }

  .cm-searching {
    background-color: #ffa;
    background-color: rgba(255, 255, 0, 0.4);
  }

  /* Used to force a border model for a node */
  .cm-force-border {
    padding-right: 0.1px;
  }

  @media print {
    /* Hide the cursor when printing */
    .CodeMirror div.CodeMirror-cursors {
      visibility: hidden;
    }
  }

  /* See issue #2901 */
  .cm-tab-wrap-hack:after {
    content: "";
  }

  /* Help users use markselection to safely style text background */
  span.CodeMirror-selectedtext {
    background: none;
  }

/*************************** OVERRIDES ***************************/
/* These styles override CodeMirror styling, to ease our theming */

.CodeMirror {
    height: "100%";
    font-family: "Dank Mono", dm, "Source Code Pro", "Monaco", monospace;
    font-size: 14px;
    line-height: 20px;

    height: auto;

    background: none;
  }

  .CodeMirror-cursor {
    border-left-width: 1px;
    border-left-style: solid;
    border-left-color: var(--cm-color, black);
  }

  .CodeMirror-scroll {
    overflow-x: auto !important;
    overflow-y: hidden !important;
    width: 100%;
  }

  .CodeMirror-lines {
    padding: 0.4em;
  }

  .CodeMirror-linenumber {
    padding: 0 8px 0 4px;
  }

  .CodeMirror-gutters {
    border-top-left-radius: 2px;
    border-bottom-left-radius: 2px;
  }

  /** Override particular styles to allow for theming via CSS Variables */
  .cm-s-composition.CodeMirror {
    font-family: "Source Code Pro", monospace;
    letter-spacing: 0.3px;
    word-spacing: 0px;
    background: var(--cm-background, #fafafa);
    color: var(--cm-color, black);
  }
  .cm-s-composition .CodeMirror-lines {
    padding: 10px;
  }
  .cm-s-composition .CodeMirror-gutters {
    background-color: var(--cm-gutter-bg, white);
    padding-right: 10px;
    z-index: 3;
    border: none;
  }

  .cm-s-composition span.cm-comment {
    color: var(--cm-comment, #a86);
  }
  .cm-s-composition span.cm-keyword {
    line-height: 1em;
    font-weight: bold;
    color: var(--cm-keyword, blue);
  }
  .cm-s-composition span.cm-string {
    color: var(--cm-string, #a22);
  }
  .cm-s-composition span.cm-builtin {
    line-height: 1em;
    font-weight: bold;
    color: var(--cm-builtin, #077);
  }
  .cm-s-composition span.cm-special {
    line-height: 1em;
    font-weight: bold;
    color: var(--cm-special, #0aa);
  }
  .cm-s-composition span.cm-variable {
    color: var(--cm-variable, black);
  }
  .cm-s-composition span.cm-number,
  .cm-s-composition span.cm-atom {
    color: var(--cm-number, #3a3);
  }
  .cm-s-composition span.cm-meta {
    color: var(--cm-meta, #555);
  }
  .cm-s-composition span.cm-link {
    color: var(--cm-link, #3a3);
  }
  .cm-s-composition span.cm-operator {
    color: var(--cm-operator, black);
  }
  .cm-s-composition span.cm-def {
    color: var(--cm-def, black);
  }
  .cm-s-composition .CodeMirror-activeline-background {
    background: var(--cm-activeline-bg, #e8f2ff);
  }
  .cm-s-composition .CodeMirror-matchingbracket {
    border-bottom: 1px solid var(--cm-matchingbracket-outline, grey);
    color: var(--cm-matchingbracket-color, black) !important;
  }


`,T.a`
/* From codemirror/addon/hint/show-hint.css */
/* There are overrides at the bottom of this stylesheet to cooperate with nteract */

.CodeMirror-hints {
  position: absolute;
  z-index: 10;
  overflow: hidden;
  list-style: none;

  margin: 0;
  padding: 2px;

  -webkit-box-shadow: 2px 3px 5px rgba(0,0,0,.2);
  -moz-box-shadow: 2px 3px 5px rgba(0,0,0,.2);
  box-shadow: 2px 3px 5px rgba(0,0,0,.2);
  border-radius: 3px;
  border: 1px solid silver;

  background: white;
  font-size: 90%;
  font-family: monospace;

  max-height: 20em;
  overflow-y: auto;
}

.CodeMirror-hint {
  margin: 0;
  padding: 0 4px;
  border-radius: 2px;
  white-space: pre;
  color: black;
  cursor: pointer;
}

li.CodeMirror-hint-active {
  background: #08f;
  color: white;
}

/*************************** OVERRIDES ***************************/
/* These styles override hint styling, used for code completion */

.CodeMirror-hints {
    -webkit-box-shadow: 2px 3px 5px rgba(0, 0, 0, 0.2);
    -moz-box-shadow: 2px 3px 5px rgba(0, 0, 0, 0.2);
    box-shadow: 2px 3px 5px rgba(0, 0, 0, 0.2);
    border-radius: 0px;
    border: none;
    padding: 0;

    background: var(--cm-hint-bg, white);
    font-size: 90%;
    font-family: "Source Code Pro", monospace;

    /*_________*/
    z-index: 9001;  /* known as wow just bring it to the front, ignore the rest of the UI */

    overflow-y: auto;
  }

  .CodeMirror-hint {
    border-radius: 0px;
    white-space: pre;
    cursor: pointer;
    color: var(--cm-hint-color, black);
  }

  li.CodeMirror-hint-active {
    background: var(--cm-hint-bg-active, #abd1ff);
    color: var(--cm-hint-color-active, black);
  }

  /** Handle the type hint segment */
  .CodeMirror-hint {
    padding-left: 0;
    border-bottom: none;
  }
`;function _(e){return e?e.replace(/\r\n|\r/g,"\n"):e}class W extends a.PureComponent{constructor(e){super(e),this.textareaRef=a.createRef(),this.tooltipNode=null,this.handleCursorChange=(e=>{const t=e.cursorCoords();this.setState({cursorCoords:t})}),this.hint=this.hint.bind(this),this.hint.async=!0,this.tips=this.tips.bind(this),this.deleteTip=this.deleteTip.bind(this),this.debounceNextCompletionRequest=!0,this.state={bundle:null,cursorCoords:null},this.fullOptions=this.fullOptions.bind(this),this.cleanMode=this.cleanMode.bind(this);const t={"Cmd-.":this.tips,"Cmd-/":"toggleComment","Ctrl-.":this.tips,"Ctrl-/":"toggleComment","Ctrl-Space":e=>(this.debounceNextCompletionRequest=!1,e.execCommand("autocomplete")),Down:this.goLineDownOrEmit,"Shift-Tab":e=>e.execCommand("indentLess"),Tab:this.executeTab,Up:this.goLineUpOrEmit,Esc:this.deleteTip},o={completeSingle:!1,extraKeys:{Right:F},hint:this.hint};this.defaultOptions=Object.assign({extraKeys:t,hintOptions:o,theme:"composition",lineWrapping:!0})}fullOptions(e={}){return Object.keys(this.props).filter(s).reduce((e,t)=>(e[t]=this.props[t],e),e)}cleanMode(){return this.props.mode?"string"==typeof this.props.mode?this.props.mode:"object"==typeof this.props.mode&&"toJS"in this.props.mode?this.props.mode.toJS():this.props.mode:"text/plain"}componentWillMount(){this.componentWillReceiveProps=Object(c.debounce)(this.componentWillReceiveProps,0)}componentDidMount(){o(1223),o(1224),o(1225),o(1226),o(1227),o(619),o(1228),o(1229),o(1230),o(1231),o(1232),o(1233),o(1234),o(1235),o(620),o(1237),o(1239);const{completion:e,editorFocused:t,focusAbove:r,focusBelow:n}=this.props,l=document.getElementsByClassName("tip-holder")[0];l?this.tooltipNode=l:(this.tooltipNode=document.createElement("div"),this.tooltipNode.classList.add("tip-holder"),document.body.appendChild(this.tooltipNode));const s=Object.assign({},this.fullOptions(),this.defaultOptions,{mode:this.cleanMode()});this.cm=i.a.fromTextArea(this.textareaRef.current,s),this.cm.setValue(this.props.value||""),t&&this.cm.focus(),this.cm.on("topBoundary",e=>{this.deleteTip(),r&&r(e)}),this.cm.on("bottomBoundary",e=>{this.deleteTip(),n&&n(e)}),this.cm.on("cursorActivity",this.handleCursorChange),this.cm.on("focus",this.focusChanged.bind(this,!0)),this.cm.on("blur",this.focusChanged.bind(this,!1)),this.cm.on("change",this.codemirrorValueChanged.bind(this));const c=Object(u.a)(this.cm,"keyup",(e,t)=>({editor:e,ev:t}));this.keyupEventsSubscriber=c.pipe(Object(g.a)(e=>Object(m.a)(e))).subscribe(({editor:t,ev:o})=>{if(e&&!t.state.completionActive&&!E[(o.keyCode||o.which).toString()]){const e=t.getDoc().getCursor(),o=t.getTokenAt(e);"tag"!==o.type&&"variable"!==o.type&&" "!==o.string&&"<"!==o.string&&"/"!==o.string&&"."!==o.string||t.execCommand("autocomplete")}}),this.completionSubject=new h.b;const[a,d]=Object(C.a)(e=>!0===e.debounce)(this.completionSubject),p=Object(b.a)(d,a.pipe(Object(x.a)(150),Object(v.a)(d),Object(k.a)())).pipe(Object(g.a)(e=>{const{channels:t}=this.props;if(!t)throw new Error("Unexpectedly received a completion event when channels were unset");return z(t,e.editor).pipe(Object(y.a)(t=>()=>e.callback(t)),Object(v.a)(this.completionSubject),Object(w.a)(e=>(console.log(`Code completion error: ${e.message}`),Object(f.b)())))}));this.completionEventsSubscriber=p.subscribe(e=>e())}componentDidUpdate(e){if(!this.cm)return;const{editorFocused:t,theme:o}=this.props;e.theme!==o&&this.cm.refresh(),e.editorFocused!==t&&(t?this.cm.focus():this.cm.getInputField().blur()),e.cursorBlinkRate!==this.props.cursorBlinkRate&&(this.cm.setOption("cursorBlinkRate",this.props.cursorBlinkRate),t&&(this.cm.getInputField().blur(),this.cm.focus())),e.mode!==this.props.mode&&this.cm.setOption("mode",this.cleanMode())}componentWillReceiveProps(e){if(this.cm&&void 0!==e.value&&_(this.cm.getValue())!==_(e.value))if(this.props.preserveScrollPosition){const t=this.cm.getScrollInfo();this.cm.setValue(e.value),this.cm.scrollTo(t.left,t.top)}else this.cm.setValue(e.value);for(const t in e)s(t)&&e[t]!==this.props[t]&&this.cm.setOption(t,e[t])}componentWillUnmount(){this.cm&&this.cm.toTextArea(),this.keyupEventsSubscriber.unsubscribe(),this.completionEventsSubscriber.unsubscribe()}focusChanged(e){this.props.onFocusChange&&this.props.onFocusChange(e)}hint(e,t){const{completion:o,channels:r}=this.props,n=this.debounceNextCompletionRequest;if(this.debounceNextCompletionRequest=!0,o&&r){const o={editor:e,callback:t,debounce:n};this.completionSubject.next(o)}}deleteTip(){this.setState({bundle:null})}tips(e){const{tip:t,channels:o}=this.props;if(this.state.bundle)return this.deleteTip();t&&V(o,e).subscribe(e=>{const t=Object.keys(e.dict).length>0?e.dict:null;this.setState({bundle:t})})}goLineDownOrEmit(e){const t=e.getCursor(),o=e.lastLine(),r=e.getLine(o);t.line!==o||t.ch!==r.length||e.somethingSelected()?e.execCommand("goLineDown"):i.a.signal(e,"bottomBoundary")}goLineUpOrEmit(e){const t=e.getCursor();0!==t.line||0!==t.ch||e.somethingSelected()?e.execCommand("goLineUp"):i.a.signal(e,"topBoundary")}executeTab(e){e.somethingSelected()?e.execCommand("indentMore"):e.execCommand("insertSoftTab")}codemirrorValueChanged(e,t){this.props.onChange&&"setValue"!==t.origin&&this.props.onChange(e.getValue(),t)}render(){const{bundle:e,cursorCoords:t}=this.state,o=this.tooltipNode;return a.createElement(a.Fragment,null,a.createElement(B,{ref:this.textareaRef,defaultValue:this.props.value}),o?p.a.createPortal(a.createElement(L,{bundle:e,cursorCoords:t,deleteTip:this.deleteTip}),o):null)}}W.defaultProps={value:"",channels:null,completion:!1,editorFocused:!1,kernelStatus:"not connected",theme:"light",tip:!1,autofocus:!1,matchBrackets:!0,indentUnit:4,lineNumbers:!1,cursorBlinkRate:530};var q=o(107),J=o(76);const Y={name:"gfm",tokenTypeOverrides:{emoji:"emoji"}},Z={name:"text/plain",tokenTypeOverrides:{emoji:"emoji"}};t.a=Object(J.b)((e,t)=>{const{id:o,contentRef:r,focusAbove:n,focusBelow:i}=t;return function(e){const t=q.model(e,{contentRef:r});if(!t||"notebook"!==t.type)throw new Error("Connected Editor components should not be used with non-notebook models");const l=q.notebook.cellById(t,{id:o});if(!l)throw new Error("cell not found inside cell map");t.cellFocused;const s=t.editorFocused===o,c=q.userTheme(e);let a=null,d="not connected",p=Z,u=!1;switch(l.cell_type){case"markdown":u=!0,p=Y;break;case"raw":u=!0,p=Z;break;case"code":{const o=t.kernelRef,r=o?e.core.entities.kernels.byRef.get(o):null;a=r?r.channels:null,r&&(d=r.status||"not connected"),p=r&&r.info?r.info.codemirrorMode:q.notebook.codeMirrorMode(t)}}return{tip:!0,completion:!0,editorFocused:s,focusAbove:n,focusBelow:i,theme:c,value:l.source,channels:a,kernelStatus:d,cursorBlinkRate:e.config.get("cursorBlinkRate",530),mode:p,lineWrapping:u}}},(e,t)=>{const{id:o,contentRef:n}=t;return e=>({onChange:t=>{e(r.updateCellSource({id:o,value:t,contentRef:n}))},onFocusChange(t){t&&(e(r.focusCellEditor({id:o,contentRef:n})),e(r.focusCell({id:o,contentRef:n})))}})})(W)},1690:function(e,t,o){"use strict";var r=o(0),n=o(603),i=o(44);const l=i.c.div`
  z-index: 10000;
  display: inline-block;
`;l.displayName="DropdownDiv";class s extends r.PureComponent{constructor(e){super(e),this.state={menuHidden:!0}}render(){return r.createElement(l,null,r.Children.map(this.props.children,e=>{const t=e;return Object(n.areComponentsEqual)(t.type,a)?r.cloneElement(t,{onClick:()=>{this.setState({menuHidden:!this.state.menuHidden})}}):Object(n.areComponentsEqual)(t.type,p)?this.state.menuHidden?null:r.cloneElement(t,{onItemClick:()=>{this.setState({menuHidden:!0})}}):e}))}}const c=i.c.div`
  user-select: none;
  margin: 0px;
  padding: 0px;
`;c.displayName="DropdownTriggerDiv";class a extends r.PureComponent{render(){return r.createElement(c,{onClick:this.props.onClick},this.props.children)}}const d=i.c.div`
  user-select: none;
  margin: 0px;
  padding: 0px;

  width: 200px;

  opacity: 1;
  position: absolute;
  top: 0.2em;
  right: 0;
  border-style: none;
  padding: 0;
  font-family: var(--nt-font-family-normal);
  font-size: var(--nt-font-size-m);
  line-height: 1.5;
  margin: 20px 0;
  background-color: var(--theme-cell-menu-bg);

  ul {
    list-style: none;
    text-align: left;
    padding: 0;
    margin: 0;
    opacity: 1;
  }

  ul li {
    padding: 0.5rem;
  }

  ul li:hover {
    background-color: var(--theme-cell-menu-bg-hover, #e2dfe3);
    cursor: pointer;
  }
`;d.displayName="DropdownContentDiv";class p extends r.PureComponent{render(){return r.createElement(d,null,r.createElement("ul",null,r.Children.map(this.props.children,e=>{const t=e;return r.cloneElement(t,{onClick:e=>{t.props.onClick(e),this.props.onItemClick(e)}})})))}}p.defaultProps={onItemClick:()=>{}};var u=o(211);o.d(t,"a",function(){return h});const m=i.c.div`
  background-color: var(--theme-cell-toolbar-bg);
  opacity: 0.4;
  transition: opacity 0.4s;

  & > div {
    display: inline-block;
  }

  :hover {
    opacity: 1;
  }

  @media print {
    display: none ;
  }

  button {
    display: inline-block;

    width: 22px;
    height: 20px;
    padding: 0px 4px;

    text-align: center;

    border: none;
    outline: none;
    background: none;
  }

  span {
    font-size: 15px;
    line-height: 1;
    color: var(--theme-cell-toolbar-fg);
  }

  button span:hover {
    color: var(--theme-cell-toolbar-fg-hover);
  }

  .octicon {
    transition: color 0.5s;
  }

  span.spacer {
    display: inline-block;
    vertical-align: middle;
    margin: 1px 5px 3px 5px;
    height: 11px;
  }
`,h=i.c.div.attrs(e=>({style:{display:e.cellFocused?"block":e.sourceHidden?"block":"none"}}))`
  z-index: 9;
  position: sticky; /* keep visible with large code cells that need scrolling */
  float: right;
  top: 0;
  right: 0;
  height: 34px;
  margin: 0 0 0 -100%; /* allow code cell to completely overlap (underlap?) */
  padding: 0 0 0 50px; /* give users extra room to move their mouse to the
                          toolbar without causing the cell to go out of
                          focus/hide the toolbar before they get there */
`;class b extends r.PureComponent{render(){const{executeCell:e,deleteCell:t,sourceHidden:o}=this.props;return r.createElement(h,{sourceHidden:o,cellFocused:this.props.cellFocused},r.createElement(m,null,"markdown"!==this.props.type&&r.createElement("button",{onClick:e,title:"execute cell",className:"executeButton"},r.createElement("span",{className:"octicon"},r.createElement(u.j,null))),r.createElement(s,null,r.createElement(a,null,r.createElement("button",{title:"show additional actions"},r.createElement("span",{className:"octicon toggle-menu"},r.createElement(u.b,null)))),"code"===this.props.type?r.createElement(p,null,r.createElement("li",{onClick:this.props.clearOutputs,className:"clearOutput",role:"option","aria-selected":"false",tabIndex:0},r.createElement("a",null,"Clear Cell Output")),r.createElement("li",{onClick:this.props.toggleCellInputVisibility,className:"inputVisibility",role:"option","aria-selected":"false",tabIndex:0},r.createElement("a",null,"Toggle Input Visibility")),r.createElement("li",{onClick:this.props.toggleCellOutputVisibility,className:"outputVisibility",role:"option","aria-selected":"false",tabIndex:0},r.createElement("a",null,"Toggle Output Visibility")),r.createElement("li",{onClick:this.props.toggleOutputExpansion,className:"outputExpanded",role:"option","aria-selected":"false",tabIndex:0},r.createElement("a",null,"Toggle Expanded Output")),r.createElement("li",{onClick:this.props.toggleParameterCell,role:"option","aria-selected":"false",tabIndex:0},r.createElement("a",null,"Toggle Parameter Cell")),r.createElement("li",{onClick:this.props.changeCellType,className:"changeType",role:"option","aria-selected":"false",tabIndex:0},r.createElement("a",null,"Convert to Markdown Cell"))):r.createElement(p,null,r.createElement("li",{onClick:this.props.changeCellType,className:"changeType",role:"option","aria-selected":"false",tabIndex:0},r.createElement("a",null,"Convert to Code Cell")))),r.createElement("span",{className:"spacer"}),r.createElement("button",{onClick:t,title:"delete cell",className:"deleteButton"},r.createElement("span",{className:"octicon"},r.createElement(u.i,null)))))}}b.defaultProps={type:"code"};t.b=b},1709:function(e,t,o){"use strict";o.r(t);var r=o(1157);t.default=r.a}}]);