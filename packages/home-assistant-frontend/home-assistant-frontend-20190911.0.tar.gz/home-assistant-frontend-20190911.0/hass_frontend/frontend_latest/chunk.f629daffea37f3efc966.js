(self.webpackJsonp=self.webpackJsonp||[]).push([[62],{231:function(e,t,i){"use strict";var l=i(3),a=i(14),s=i(74);i(238);const d=customElements.get("mwc-fab");let c=class extends d{render(){const e={"mdc-fab--mini":this.mini,"mdc-fab--exited":this.exited,"mdc-fab--extended":this.extended},t=""!==this.label&&this.extended;return a.g`
      <button
        .ripple="${Object(s.a)()}"
        class="mdc-fab ${Object(a.d)(e)}"
        ?disabled="${this.disabled}"
        aria-label="${this.label||this.icon}"
      >
        ${t&&this.showIconAtEnd?this.label:""}
        ${this.icon?a.g`
              <ha-icon .icon=${this.icon}></ha-icon>
            `:""}
        ${t&&!this.showIconAtEnd?this.label:""}
      </button>
    `}};c=l.b([Object(a.f)("ha-fab")],c)},720:function(e,t,i){"use strict";i.r(t);var l=i(3),a=i(0),s=i(73),d=(i(231),i(176)),c=i(121);i(657);const o=customElements.get("mwc-checkbox");let n=class extends o{firstUpdated(){super.firstUpdated(),this.style.setProperty("--mdc-theme-secondary","var(--primary-color)")}};n=l.b([Object(a.d)("ha-checkbox")],n);i(185),i(228),i(179);var r=i(18);let h=class extends a.a{constructor(){super(...arguments),this.selectable=!0}render(){if(!this.entity)return a.f``;const e=this.entity?this.hass.states[this.entity]:void 0;return e?a.f`
      <div class="flex-row" role="rowgroup">
        <div class="flex-cell" role="cell">
          ${this.selectable?a.f`
                <ha-checkbox @change=${this._handleSelect}></ha-checkbox>
              `:""}
          <state-badge .hass=${this.hass} .stateObj=${e}></state-badge>
          ${Object(d.a)(e)}
        </div>
        <div class="flex-cell" role="cell">${e.entity_id}</div>
        <div class="flex-cell" role="cell">
          ${Object(c.a)(e.entity_id)}
        </div>
        <div class="flex-cell" role="cell">
          <ha-relative-time
            .hass=${this.hass}
            .datetime=${e.last_changed}
          ></ha-relative-time>
        </div>
      </div>
    `:a.f``}_handleSelect(e){const t=e.currentTarget;Object(r.a)(this,"entity-selection-changed",{entity:this.entity,selected:t.checked})}static get styles(){return a.c`
      div {
        box-sizing: border-box;
      }

      .flex-row {
        display: flex;
        flex-flow: row wrap;
      }

      .flex-row:hover {
        background: var(--table-row-alternative-background-color, #eee);
      }

      .flex-cell {
        width: calc(100% / 4);
        padding: 12px 24px;
        border-bottom: 1px solid #e0e0e0;
        overflow: hidden;
        text-overflow: ellipsis;
        line-height: 40px;
      }

      @media all and (max-width: 767px) {
        .flex-cell {
          width: calc(100% / 3);
          padding-top: 0;
        }
        .flex-cell:first-child {
          width: 100%;
          padding-top: 12px;
          padding-bottom: 0;
          border-bottom: 0;
        }
      }

      @media all and (max-width: 430px) {
        .flex-cell {
          border-bottom: 0;
          padding: 0 24px;
        }

        .flex-cell:first-child {
          padding-top: 12px;
        }

        .flex-cell:last-child {
          padding-bottom: 12px;
          border-bottom: 1px solid #e0e0e0;
        }

        .flex-cell {
          width: 100%;
        }
      }
    `}};l.b([Object(a.g)()],h.prototype,"hass",void 0),l.b([Object(a.g)()],h.prototype,"entity",void 0),l.b([Object(a.g)()],h.prototype,"selectable",void 0),h=l.b([Object(a.d)("hui-select-row")],h);var b=i(96);const f=["zone"],p=(e,t)=>{if("call-service"!==t.action||!t.service_data||!t.service_data.entity_id)return;let i=t.service_data.entity_id;Array.isArray(i)||(i=[i]);for(const l of i)e.add(l)},v=(e,t)=>{"string"!=typeof t?(t.entity&&e.add(t.entity),t.camera_image&&e.add(t.camera_image),t.tap_action&&p(e,t.tap_action),t.hold_action&&p(e,t.hold_action)):e.add(t)},x=(e,t)=>{t.entity&&v(e,t.entity),t.entities&&t.entities.forEach(t=>v(e,t)),t.card&&x(e,t.card),t.cards&&t.cards.forEach(t=>x(e,t)),t.elements&&t.elements.forEach(t=>x(e,t)),t.badges&&t.badges.forEach(t=>v(e,t))},u=(e,t)=>{const i=(e=>{const t=new Set;return e.views.forEach(e=>x(t,e)),t})(t);return Object.keys(e.states).filter(e=>!i.has(e)&&!f.includes(e.split(".",1)[0])).sort()};var g=i(399);i.d(t,"HuiUnusedEntities",function(){return m});let m=class extends a.a{constructor(){super(...arguments),this._unusedEntities=[],this._selectedEntities=[]}get _config(){return this.lovelace.config}updated(e){super.updated(e),e.has("lovelace")&&this._getUnusedEntities()}render(){return this.hass&&this.lovelace?"storage"===this.lovelace.mode&&!1===this.lovelace.editMode?a.f``:a.f`
      <ha-card header="Unused entities">
        <div class="card-content">
          These are the entities that you have available, but are not in your
          Lovelace UI yet.
          ${"storage"===this.lovelace.mode?a.f`
                <br />Select the entities you want to add to a card and then
                click the add card button.
              `:""}
        </div>
        <div
          class="table-container"
          role="table"
          aria-label="Unused Entities"
          @entity-selection-changed=${this._handleSelectionChanged}
        >
          <div class="flex-row header" role="rowgroup">
            <div class="flex-cell" role="columnheader">Entity</div>
            <div class="flex-cell" role="columnheader">Entity id</div>
            <div class="flex-cell" role="columnheader">Domain</div>
            <div class="flex-cell" role="columnheader">Last Changed</div>
          </div>
          ${this._unusedEntities.map(e=>a.f`
              <hui-select-row
                .selectable=${"storage"===this.lovelace.mode}
                .hass=${this.hass}
                .entity=${e}
              ></hui-select-row>
            `)}
        </div>
      </ha-card>
      ${"storage"===this.lovelace.mode?a.f`
            <ha-fab
              class="${Object(s.a)({rtl:Object(b.a)(this.hass)})}"
              icon="hass:plus"
              label="${this.hass.localize("ui.panel.lovelace.editor.edit_card.add")}"
              @click="${this._selectView}"
            ></ha-fab>
          `:""}
    `:a.f``}_getUnusedEntities(){this.hass&&this.lovelace&&(this._selectedEntities=[],this._unusedEntities=u(this.hass,this._config))}_handleSelectionChanged(e){if(e.detail.selected)this._selectedEntities.push(e.detail.entity);else{const t=this._selectedEntities.indexOf(e.detail.entity);-1!==t&&this._selectedEntities.splice(t,1)}}_selectView(){var e,t;e=this,t={lovelace:this.lovelace,viewSelectedCallback:e=>this._addCard(e)},Object(r.a)(e,"show-dialog",{dialogTag:"hui-dialog-select-view",dialogImport:()=>i.e(46).then(i.bind(null,707)),dialogParams:t})}_addCard(e){Object(g.a)(this,{lovelace:this.lovelace,path:[e],entities:this._selectedEntities})}static get styles(){return a.c`
      :host {
        background: var(--lovelace-background);
        padding: 16px;
      }
      ha-fab {
        position: sticky;
        float: right;
        bottom: 16px;
        z-index: 1;
      }
      ha-fab.rtl {
        float: left;
      }

      div {
        box-sizing: border-box;
      }

      .table-container {
        display: block;
        margin: auto;
      }

      .flex-row {
        display: flex;
        flex-flow: row wrap;
      }
      .flex-row .flex-cell {
        font-weight: bold;
      }

      .flex-cell {
        width: calc(100% / 4);
        padding: 12px 24px;
        border-bottom: 1px solid #e0e0e0;
        vertical-align: middle;
      }

      @media all and (max-width: 767px) {
        .flex-cell {
          width: calc(100% / 3);
        }
        .flex-cell:first-child {
          width: 100%;
          border-bottom: 0;
        }
      }
      @media all and (max-width: 430px) {
        .flex-cell {
          border-bottom: 0;
        }

        .flex-cell:last-child {
          border-bottom: 1px solid #e0e0e0;
        }

        .flex-cell {
          width: 100%;
        }
      }
    `}};l.b([Object(a.g)()],m.prototype,"lovelace",void 0),l.b([Object(a.g)()],m.prototype,"hass",void 0),l.b([Object(a.g)()],m.prototype,"_unusedEntities",void 0),m=l.b([Object(a.d)("hui-unused-entities")],m)}}]);
//# sourceMappingURL=chunk.f629daffea37f3efc966.js.map