(self.webpackJsonp=self.webpackJsonp||[]).push([[55],{197:function(t,e,n){"use strict";var i=n(203);n.d(e,"a",function(){return a});const a=Object(i.a)({types:{"entity-id":function(t){return"string"!=typeof t?"entity id should be a string":!!t.includes(".")||"entity id should be in the format 'domain.entity'"},icon:function(t){return"string"!=typeof t?"icon should be a string":!!t.includes(":")||"icon should be in the format 'mdi:icon'"}}})},205:function(t,e,n){"use strict";n.d(e,"a",function(){return i});const i=n(0).f`
  <style>
    paper-toggle-button {
      padding-top: 16px;
    }
    .side-by-side {
      display: flex;
    }
    .side-by-side > * {
      flex: 1;
      padding-right: 4px;
    }
    .suffix {
      margin: 0 8px;
    }
  </style>
`},682:function(t,e,n){"use strict";n.r(e),n.d(e,"HuiMarkdownCardEditor",function(){return u});var i=n(3),a=n(0),o=(n(93),n(215),n(197)),s=n(18),c=n(205);const r=Object(o.a)({type:"string",title:"string?",content:"string"});let u=class extends a.a{setConfig(t){t=r(t),this._config=t}get _title(){return this._config.title||""}get _content(){return this._config.content||""}render(){return this.hass?a.f`
      ${c.a}
      <div class="card-config">
        <paper-input
          label="Title"
          .value="${this._title}"
          .configValue="${"title"}"
          @value-changed="${this._valueChanged}"
        ></paper-input>
        <paper-textarea
          label="Content"
          .value="${this._content}"
          .configValue="${"content"}"
          @value-changed="${this._valueChanged}"
          autocapitalize="none"
          autocomplete="off"
          spellcheck="false"
        ></paper-textarea>
      </div>
    `:a.f``}_valueChanged(t){if(!this._config||!this.hass)return;const e=t.target;this[`_${e.configValue}`]!==e.value&&(e.configValue&&(""===e.value?delete this._config[e.configValue]:this._config=Object.assign({},this._config,{[e.configValue]:e.value})),Object(s.a)(this,"config-changed",{config:this._config}))}};i.b([Object(a.g)()],u.prototype,"hass",void 0),i.b([Object(a.g)()],u.prototype,"_config",void 0),u=i.b([Object(a.d)("hui-markdown-card-editor")],u)}}]);
//# sourceMappingURL=chunk.d09e156ed8575ee810eb.js.map