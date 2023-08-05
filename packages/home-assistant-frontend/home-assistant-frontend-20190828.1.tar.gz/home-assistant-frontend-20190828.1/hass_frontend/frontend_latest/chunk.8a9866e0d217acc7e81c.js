/*! For license information please see chunk.8a9866e0d217acc7e81c.js.LICENSE */
(self.webpackJsonp=self.webpackJsonp||[]).push([[38],{127:function(e,t,r){var a=r(153),i=["renderMarkdown"];e.exports=function(){var e=new Worker(r.p+"fa012fa46b8f7a0b736e.worker.js",{name:"[hash].worker.js"});return a(e,i),e}},151:function(e,t,r){"use strict";var a=r(0),i=r(127),s=r.n(i),o=r(19);function n(e){var t,r=m(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var a={kind:"field"===e.kind?"field":"method",key:r,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(a.decorators=e.decorators),"field"===e.kind&&(a.initializer=e.value),a}function l(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function p(e){return e.decorators&&e.decorators.length}function c(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function d(e,t){var r=e[t];if(void 0!==r&&"function"!=typeof r)throw new TypeError("Expected '"+t+"' to be a function");return r}function m(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var a=r.call(e,t||"default");if("object"!=typeof a)return a;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function u(e,t,r){return(u="undefined"!=typeof Reflect&&Reflect.get?Reflect.get:function(e,t,r){var a=function(e,t){for(;!Object.prototype.hasOwnProperty.call(e,t)&&null!==(e=f(e)););return e}(e,t);if(a){var i=Object.getOwnPropertyDescriptor(a,t);return i.get?i.get.call(r):i.value}})(e,t,r||e)}function f(e){return(f=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)})(e)}let h;!function(e,t,r,a){var i=function(){var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach(function(r){t.forEach(function(t){t.kind===r&&"own"===t.placement&&this.defineClassElement(e,t)},this)},this)},initializeClassElements:function(e,t){var r=e.prototype;["method","field"].forEach(function(a){t.forEach(function(t){var i=t.placement;if(t.kind===a&&("static"===i||"prototype"===i)){var s="static"===i?e:r;this.defineClassElement(s,t)}},this)},this)},defineClassElement:function(e,t){var r=t.descriptor;if("field"===t.kind){var a=t.initializer;r={enumerable:r.enumerable,writable:r.writable,configurable:r.configurable,value:void 0===a?void 0:a.call(e)}}Object.defineProperty(e,t.key,r)},decorateClass:function(e,t){var r=[],a=[],i={static:[],prototype:[],own:[]};if(e.forEach(function(e){this.addElementPlacement(e,i)},this),e.forEach(function(e){if(!p(e))return r.push(e);var t=this.decorateElement(e,i);r.push(t.element),r.push.apply(r,t.extras),a.push.apply(a,t.finishers)},this),!t)return{elements:r,finishers:a};var s=this.decorateConstructor(r,t);return a.push.apply(a,s.finishers),s.finishers=a,s},addElementPlacement:function(e,t,r){var a=t[e.placement];if(!r&&-1!==a.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");a.push(e.key)},decorateElement:function(e,t){for(var r=[],a=[],i=e.decorators,s=i.length-1;s>=0;s--){var o=t[e.placement];o.splice(o.indexOf(e.key),1);var n=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,i[s])(n)||n);e=l.element,this.addElementPlacement(e,t),l.finisher&&a.push(l.finisher);var p=l.extras;if(p){for(var c=0;c<p.length;c++)this.addElementPlacement(p[c],t);r.push.apply(r,p)}}return{element:e,finishers:a,extras:r}},decorateConstructor:function(e,t){for(var r=[],a=t.length-1;a>=0;a--){var i=this.fromClassDescriptor(e),s=this.toClassDescriptor((0,t[a])(i)||i);if(void 0!==s.finisher&&r.push(s.finisher),void 0!==s.elements){e=s.elements;for(var o=0;o<e.length-1;o++)for(var n=o+1;n<e.length;n++)if(e[o].key===e[n].key&&e[o].placement===e[n].placement)throw new TypeError("Duplicated element ("+e[o].key+")")}}return{elements:e,finishers:r}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if(Symbol.iterator in Object(e)||"[object Arguments]"===Object.prototype.toString.call(e))return Array.from(e)}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance")}()).map(function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t},this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var r=m(e.key),a=String(e.placement);if("static"!==a&&"prototype"!==a&&"own"!==a)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+a+'"');var i=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var s={kind:t,key:r,placement:a,descriptor:Object.assign({},i)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(i,"get","The property descriptor of a field descriptor"),this.disallowProperty(i,"set","The property descriptor of a field descriptor"),this.disallowProperty(i,"value","The property descriptor of a field descriptor"),s.initializer=e.initializer),s},toElementFinisherExtras:function(e){var t=this.toElementDescriptor(e),r=d(e,"finisher"),a=this.toElementDescriptors(e.extras);return{element:t,finisher:r,extras:a}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var r=d(e,"finisher"),a=this.toElementDescriptors(e.elements);return{elements:a,finisher:r}},runClassFinishers:function(e,t){for(var r=0;r<t.length;r++){var a=(0,t[r])(e);if(void 0!==a){if("function"!=typeof a)throw new TypeError("Finishers must return a constructor.");e=a}}return e},disallowProperty:function(e,t,r){if(void 0!==e[t])throw new TypeError(r+" can't have a ."+t+" property.")}};return e}();if(a)for(var s=0;s<a.length;s++)i=a[s](i);var o=t(function(e){i.initializeInstanceElements(e,u.elements)},r),u=i.decorateClass(function(e){for(var t=[],r=function(e){return"method"===e.kind&&e.key===s.key&&e.placement===s.placement},a=0;a<e.length;a++){var i,s=e[a];if("method"===s.kind&&(i=t.find(r)))if(c(s.descriptor)||c(i.descriptor)){if(p(s)||p(i))throw new ReferenceError("Duplicated methods ("+s.key+") can't be decorated.");i.descriptor=s.descriptor}else{if(p(s)){if(p(i))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+s.key+").");i.decorators=s.decorators}l(s,i)}else t.push(s)}return t}(o.d.map(n)),e);i.initializeClassElements(o.F,u.elements),i.runClassFinishers(o.F,u.finishers)}([Object(a.d)("ha-markdown")],function(e,t){class r extends t{constructor(...t){super(...t),e(this)}}return{F:r,d:[{kind:"field",decorators:[Object(a.g)()],key:"content",value:()=>""},{kind:"field",decorators:[Object(a.g)({type:Boolean})],key:"allowSvg",value:()=>!1},{kind:"method",key:"update",value:function(e){u(f(r.prototype),"update",this).call(this,e),h||(h=s()()),this._render()}},{kind:"method",key:"_render",value:async function(){this.innerHTML=await h.renderMarkdown(this.content,{breaks:!0,gfm:!0,tables:!0},{allowSvg:this.allowSvg}),this._resize();const e=document.createTreeWalker(this,1,null,!1);for(;e.nextNode();){const t=e.currentNode;"A"===t.nodeName&&t.host!==document.location.host?t.target="_blank":"IMG"===t.nodeName&&t.addEventListener("load",this._resize)}}},{kind:"field",key:"_resize",value(){return()=>Object(o.a)(this,"iron-resize")}}]}},a.b)},155:function(e,t,r){"use strict";r(154);const a=customElements.get("paper-slider");customElements.define("ha-paper-slider",class extends a{static get template(){const e=document.createElement("template");e.innerHTML=a.template.innerHTML;const t=document.createElement("style");return t.innerHTML='\n      .pin > .slider-knob > .slider-knob-inner {\n        font-size:  var(--ha-paper-slider-pin-font-size, 10px);\n        line-height: normal;\n      }\n\n      .pin > .slider-knob > .slider-knob-inner::before {\n        top: unset;\n        margin-left: unset;\n\n        bottom: calc(15px + var(--calculated-paper-slider-height)/2);\n        left: 50%;\n        width: 2.2em;\n        height: 2.2em;\n\n        -webkit-transform-origin: left bottom;\n        transform-origin: left bottom;\n        -webkit-transform: rotate(-45deg) scale(0) translate(0);\n        transform: rotate(-45deg) scale(0) translate(0);\n      }\n\n      .pin.expand > .slider-knob > .slider-knob-inner::before {\n        -webkit-transform: rotate(-45deg) scale(1) translate(7px, -7px);\n        transform: rotate(-45deg) scale(1) translate(7px, -7px);\n      }\n\n      .pin > .slider-knob > .slider-knob-inner::after {\n        top: unset;\n        font-size: unset;\n\n        bottom: calc(15px + var(--calculated-paper-slider-height)/2);\n        left: 50%;\n        margin-left: -1.1em;\n        width: 2.2em;\n        height: 2.1em;\n\n        -webkit-transform-origin: center bottom;\n        transform-origin: center bottom;\n        -webkit-transform: scale(0) translate(0);\n        transform: scale(0) translate(0);\n      }\n\n      .pin.expand > .slider-knob > .slider-knob-inner::after {\n        -webkit-transform: scale(1) translate(0, -10px);\n        transform: scale(1) translate(0, -10px);\n      }\n\n      :host([dir="rtl"]) .pin.expand > .slider-knob > .slider-knob-inner::after {\n        -webkit-transform: scale(1) translate(0, -17px) scaleX(-1) !important;\n        transform: scale(1) translate(0, -17px) scaleX(-1) !important;\n        }\n    ',e.content.appendChild(t),e}})},157:function(e,t,r){"use strict";r(150),r(143),r(105),r(90),r(140),r(142);var a=r(3),i=r(29),s=(r(155),r(115));customElements.define("ha-form",class extends(Object(s.a)(i.a)){static get template(){return a.a`
      <style>
        .error {
          color: red;
        }
        paper-checkbox {
          display: inline-block;
          padding: 22px 0;
        }
      </style>
      <template is="dom-if" if="[[_isArray(schema)]]" restamp="">
        <template is="dom-if" if="[[error.base]]">
          <div class="error">[[computeError(error.base, schema)]]</div>
        </template>

        <template is="dom-repeat" items="[[schema]]">
          <ha-form
            data="[[_getValue(data, item)]]"
            schema="[[item]]"
            error="[[_getValue(error, item)]]"
            on-data-changed="_valueChanged"
            compute-label="[[computeLabel]]"
            compute-error="[[computeError]]"
          ></ha-form>
        </template>
      </template>
      <template is="dom-if" if="[[!_isArray(schema)]]" restamp="">
        <template is="dom-if" if="[[error]]">
          <div class="error">[[computeError(error, schema)]]</div>
        </template>

        <template
          is="dom-if"
          if='[[_equals(schema.type, "string")]]'
          restamp=""
        >
          <template
            is="dom-if"
            if='[[_includes(schema.name, "password")]]'
            restamp=""
          >
            <paper-input
              type="[[_passwordFieldType(unmaskedPassword)]]"
              label="[[computeLabel(schema)]]"
              value="{{data}}"
              required="[[schema.required]]"
              auto-validate="[[schema.required]]"
              error-message="Required"
            >
              <paper-icon-button
                toggles
                active="{{unmaskedPassword}}"
                slot="suffix"
                icon="[[_passwordFieldIcon(unmaskedPassword)]]"
                id="iconButton"
                title="Click to toggle between masked and clear password"
              >
              </paper-icon-button>
            </paper-input>
          </template>
          <template
            is="dom-if"
            if='[[!_includes(schema.name, "password")]]'
            restamp=""
          >
            <paper-input
              label="[[computeLabel(schema)]]"
              value="{{data}}"
              required="[[schema.required]]"
              auto-validate="[[schema.required]]"
              error-message="Required"
            ></paper-input>
          </template>
        </template>

        <template
          is="dom-if"
          if='[[_equals(schema.type, "integer")]]'
          restamp=""
        >
          <template is="dom-if" if="[[_isRange(schema)]]" restamp="">
            <div>
              [[computeLabel(schema)]]
              <ha-paper-slider
                pin=""
                value="{{data}}"
                min="[[schema.valueMin]]"
                max="[[schema.valueMax]]"
              ></ha-paper-slider>
            </div>
          </template>
          <template is="dom-if" if="[[!_isRange(schema)]]" restamp="">
            <paper-input
              label="[[computeLabel(schema)]]"
              value="{{data}}"
              type="number"
              required="[[schema.required]]"
              auto-validate="[[schema.required]]"
              error-message="Required"
            ></paper-input>
          </template>
        </template>

        <template is="dom-if" if='[[_equals(schema.type, "float")]]' restamp="">
          <!-- TODO -->
          <paper-input
            label="[[computeLabel(schema)]]"
            value="{{data}}"
            required="[[schema.required]]"
            auto-validate="[[schema.required]]"
            error-message="Required"
          ></paper-input>
        </template>

        <template
          is="dom-if"
          if='[[_equals(schema.type, "boolean")]]'
          restamp=""
        >
          <div>
            <paper-checkbox checked="{{data}}"
              >[[computeLabel(schema)]]</paper-checkbox
            >
          </div>
        </template>

        <template
          is="dom-if"
          if='[[_equals(schema.type, "select")]]'
          restamp=""
        >
          <paper-dropdown-menu label="[[computeLabel(schema)]]">
            <paper-listbox
              slot="dropdown-content"
              attr-for-selected="item-name"
              selected="{{data}}"
            >
              <template is="dom-repeat" items="[[schema.options]]">
                <paper-item item-name$="[[_optionValue(item)]]"
                  >[[_optionLabel(item)]]</paper-item
                >
              </template>
            </paper-listbox>
          </paper-dropdown-menu>
        </template>
      </template>
    `}static get properties(){return{data:{type:Object,notify:!0},schema:Object,error:Object,computeLabel:{type:Function,value:()=>e=>e&&e.name},computeError:{type:Function,value:()=>(e,t)=>e}}}focus(){const e=this.shadowRoot.querySelector("ha-form, paper-input, ha-paper-slider, paper-checkbox, paper-dropdown-menu");e&&e.focus()}_isArray(e){return Array.isArray(e)}_isRange(e){return"valueMin"in e&&"valueMax"in e}_equals(e,t){return e===t}_includes(e,t){return e.indexOf(t)>=0}_getValue(e,t){return e?e[t.name]:null}_valueChanged(e){let t=e.detail.value;"integer"===e.model.item.type&&(t=Number(e.detail.value)),this.set(["data",e.model.item.name],t)}_passwordFieldType(e){return e?"text":"password"}_passwordFieldIcon(e){return e?"hass:eye-off":"hass:eye"}_optionValue(e){return Array.isArray(e)?e[0]:e}_optionLabel(e){return Array.isArray(e)?e[1]:e}})},191:function(e,t,r){"use strict";r(189);var a=r(70),i=r(1),s=r(123);const o={getTabbableNodes:function(e){var t=[];return this._collectTabbableNodes(e,t)?s.a._sortByTabIndex(t):t},_collectTabbableNodes:function(e,t){if(e.nodeType!==Node.ELEMENT_NODE||!s.a._isVisible(e))return!1;var r,a=e,o=s.a._normalizedTabIndex(a),n=o>0;o>=0&&t.push(a),r="content"===a.localName||"slot"===a.localName?Object(i.a)(a).getDistributedNodes():Object(i.a)(a.shadowRoot||a.root||a).children;for(var l=0;l<r.length;l++)n=this._collectTabbableNodes(r[l],t)||n;return n}},n=customElements.get("paper-dialog"),l={get _focusableNodes(){return o.getTabbableNodes(this)}};customElements.define("ha-paper-dialog",class extends(Object(a.b)([l],n)){})},206:function(e,t,r){"use strict";r(4),r(44),r(41);var a=r(181),i=r(5),s=r(3);Object(i.a)({_template:s.a`
    <style>

      :host {
        display: block;
        @apply --layout-relative;
      }

      :host(.is-scrolled:not(:first-child))::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 1px;
        background: var(--divider-color);
      }

      :host(.can-scroll:not(.scrolled-to-bottom):not(:last-child))::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        height: 1px;
        background: var(--divider-color);
      }

      .scrollable {
        padding: 0 24px;

        @apply --layout-scroll;
        @apply --paper-dialog-scrollable;
      }

      .fit {
        @apply --layout-fit;
      }
    </style>

    <div id="scrollable" class="scrollable" on-scroll="updateScrollState">
      <slot></slot>
    </div>
`,is:"paper-dialog-scrollable",properties:{dialogElement:{type:Object}},get scrollTarget(){return this.$.scrollable},ready:function(){this._ensureTarget(),this.classList.add("no-padding")},attached:function(){this._ensureTarget(),requestAnimationFrame(this.updateScrollState.bind(this))},updateScrollState:function(){this.toggleClass("is-scrolled",this.scrollTarget.scrollTop>0),this.toggleClass("can-scroll",this.scrollTarget.offsetHeight<this.scrollTarget.scrollHeight),this.toggleClass("scrolled-to-bottom",this.scrollTarget.scrollTop+this.scrollTarget.offsetHeight>=this.scrollTarget.scrollHeight)},_ensureTarget:function(){this.dialogElement=this.dialogElement||this.parentElement,this.dialogElement&&this.dialogElement.behaviors&&this.dialogElement.behaviors.indexOf(a.b)>=0?(this.dialogElement.sizingTarget=this.scrollTarget,this.scrollTarget.classList.remove("fit")):this.dialogElement&&this.scrollTarget.classList.add("fit")}})},688:function(e,t,r){"use strict";r.r(t);r(82),r(206),r(182);var a=r(3),i=r(29),s=(r(191),r(157),r(151),r(92),r(115)),o=r(172);let n=0;customElements.define("ha-mfa-module-setup-flow",class extends(Object(o.a)(Object(s.a)(i.a))){static get template(){return a.a`
      <style include="ha-style-dialog">
        .error {
          color: red;
        }
        ha-paper-dialog {
          max-width: 500px;
        }
        ha-markdown img:first-child:last-child,
        ha-markdown svg:first-child:last-child {
          display: block;
          margin: 0 auto;
        }
        ha-markdown a {
          color: var(--primary-color);
        }
        .init-spinner {
          padding: 10px 100px 34px;
          text-align: center;
        }
        .submit-spinner {
          margin-right: 16px;
        }
      </style>
      <ha-paper-dialog
        id="dialog"
        with-backdrop=""
        opened="{{_opened}}"
        on-opened-changed="_openedChanged"
      >
        <h2>
          <template is="dom-if" if="[[_equals(_step.type, 'abort')]]">
            [[localize('ui.panel.profile.mfa_setup.title_aborted')]]
          </template>
          <template is="dom-if" if="[[_equals(_step.type, 'create_entry')]]">
            [[localize('ui.panel.profile.mfa_setup.title_success')]]
          </template>
          <template is="dom-if" if="[[_equals(_step.type, 'form')]]">
            [[_computeStepTitle(localize, _step)]]
          </template>
        </h2>
        <paper-dialog-scrollable>
          <template is="dom-if" if="[[_errorMsg]]">
            <div class="error">[[_errorMsg]]</div>
          </template>
          <template is="dom-if" if="[[!_step]]">
            <div class="init-spinner">
              <paper-spinner active></paper-spinner>
            </div>
          </template>
          <template is="dom-if" if="[[_step]]">
            <template is="dom-if" if="[[_equals(_step.type, 'abort')]]">
              <ha-markdown
                allowsvg
                content="[[_computeStepAbortedReason(localize, _step)]]"
              ></ha-markdown>
            </template>

            <template is="dom-if" if="[[_equals(_step.type, 'create_entry')]]">
              <p>
                [[localize('ui.panel.profile.mfa_setup.step_done', 'step',
                _step.title)]]
              </p>
            </template>

            <template is="dom-if" if="[[_equals(_step.type, 'form')]]">
              <template
                is="dom-if"
                if="[[_computeStepDescription(localize, _step)]]"
              >
                <ha-markdown
                  allowsvg
                  content="[[_computeStepDescription(localize, _step)]]"
                ></ha-markdown>
              </template>

              <ha-form
                data="{{_stepData}}"
                schema="[[_step.data_schema]]"
                error="[[_step.errors]]"
                compute-label="[[_computeLabelCallback(localize, _step)]]"
                compute-error="[[_computeErrorCallback(localize, _step)]]"
              ></ha-form>
            </template>
          </template>
        </paper-dialog-scrollable>
        <div class="buttons">
          <template is="dom-if" if="[[_equals(_step.type, 'abort')]]">
            <mwc-button on-click="_flowDone"
              >[[localize('ui.panel.profile.mfa_setup.close')]]</mwc-button
            >
          </template>
          <template is="dom-if" if="[[_equals(_step.type, 'create_entry')]]">
            <mwc-button on-click="_flowDone"
              >[[localize('ui.panel.profile.mfa_setup.close')]]</mwc-button
            >
          </template>
          <template is="dom-if" if="[[_equals(_step.type, 'form')]]">
            <template is="dom-if" if="[[_loading]]">
              <div class="submit-spinner">
                <paper-spinner active></paper-spinner>
              </div>
            </template>
            <template is="dom-if" if="[[!_loading]]">
              <mwc-button on-click="_submitStep"
                >[[localize('ui.panel.profile.mfa_setup.submit')]]</mwc-button
              >
            </template>
          </template>
        </div>
      </ha-paper-dialog>
    `}static get properties(){return{_hass:Object,_dialogClosedCallback:Function,_instance:Number,_loading:{type:Boolean,value:!1},_errorMsg:String,_opened:{type:Boolean,value:!1},_step:{type:Object,value:null},_stepData:Object}}ready(){super.ready(),this.addEventListener("keypress",e=>{13===e.keyCode&&this._submitStep()})}showDialog({hass:e,continueFlowId:t,mfaModuleId:r,dialogClosedCallback:a}){this.hass=e,this._instance=n++,this._dialogClosedCallback=a,this._createdFromHandler=!!r,this._loading=!0,this._opened=!0;const i=t?this.hass.callWS({type:"auth/setup_mfa",flow_id:t}):this.hass.callWS({type:"auth/setup_mfa",mfa_module_id:r}),s=this._instance;i.then(e=>{s===this._instance&&(this._processStep(e),this._loading=!1,setTimeout(()=>this.$.dialog.center(),0))})}_submitStep(){this._loading=!0,this._errorMsg=null;const e=this._instance;this.hass.callWS({type:"auth/setup_mfa",flow_id:this._step.flow_id,user_input:this._stepData}).then(t=>{e===this._instance&&(this._processStep(t),this._loading=!1)},e=>{this._errorMsg=e&&e.body&&e.body.message||"Unknown error occurred",this._loading=!1})}_processStep(e){e.errors||(e.errors={}),this._step=e,0===Object.keys(e.errors).length&&(this._stepData={})}_flowDone(){this._opened=!1;const e=this._step&&["create_entry","abort"].includes(this._step.type);this._step&&!e&&this._createdFromHandler,this._dialogClosedCallback({flowFinished:e}),this._errorMsg=null,this._step=null,this._stepData={},this._dialogClosedCallback=null}_equals(e,t){return e===t}_openedChanged(e){this._step&&!e.detail.value&&this._flowDone()}_computeStepAbortedReason(e,t){return e(`component.auth.mfa_setup.${t.handler}.abort.${t.reason}`)}_computeStepTitle(e,t){return e(`component.auth.mfa_setup.${t.handler}.step.${t.step_id}.title`)||"Setup Multi-factor Authentication"}_computeStepDescription(e,t){const r=[`component.auth.mfa_setup.${t.handler}.step.${t.step_id}.description`],a=t.description_placeholders||{};return Object.keys(a).forEach(e=>{r.push(e),r.push(a[e])}),e(...r)}_computeLabelCallback(e,t){return r=>e(`component.auth.mfa_setup.${t.handler}.step.${t.step_id}.data.${r.name}`)||r.name}_computeErrorCallback(e,t){return r=>e(`component.auth.mfa_setup.${t.handler}.error.${r}`)||r}})}}]);
//# sourceMappingURL=chunk.8a9866e0d217acc7e81c.js.map