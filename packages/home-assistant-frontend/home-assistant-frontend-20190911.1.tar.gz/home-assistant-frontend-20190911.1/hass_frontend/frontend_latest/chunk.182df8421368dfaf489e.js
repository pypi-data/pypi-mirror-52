/*! For license information please see chunk.182df8421368dfaf489e.js.LICENSE */
(self.webpackJsonp=self.webpackJsonp||[]).push([[62],{231:function(e,t,a){"use strict";var s=a(3),i=a(14),o=a(74);a(238);const d=customElements.get("mwc-fab");let c=class extends d{render(){const e={"mdc-fab--mini":this.mini,"mdc-fab--exited":this.exited,"mdc-fab--extended":this.extended},t=""!==this.label&&this.extended;return i.g`
      <button
        .ripple="${Object(o.a)()}"
        class="mdc-fab ${Object(i.d)(e)}"
        ?disabled="${this.disabled}"
        aria-label="${this.label||this.icon}"
      >
        ${t&&this.showIconAtEnd?this.label:""}
        ${this.icon?i.g`
              <ha-icon .icon=${this.icon}></ha-icon>
            `:""}
        ${t&&!this.showIconAtEnd?this.label:""}
      </button>
    `}};c=s.b([Object(i.f)("ha-fab")],c)},412:function(e,t,a){"use strict";var s=a(3),i=a(11),o=a(0),d=a(18);a(109),a(93),a(108),a(85);let c=class extends o.a{render(){return i.g`
      <div class="search-container">
        <paper-input
          autofocus
          label="Search"
          .value=${this.filter}
          @value-changed=${this._filterInputChanged}
        >
          <iron-icon
            icon="hass:magnify"
            slot="prefix"
            class="prefix"
          ></iron-icon>
          ${this.filter&&i.g`
              <paper-icon-button
                slot="suffix"
                class="suffix"
                @click=${this._clearSearch}
                icon="hass:close"
                alt="Clear"
                title="Clear"
              ></paper-icon-button>
            `}
        </paper-input>
      </div>
    `}async _filterChanged(e){Object(d.a)(this,"value-changed",{value:String(e)})}async _filterInputChanged(e){this._filterChanged(e.target.value)}async _clearSearch(){this._filterChanged("")}static get styles(){return o.c`
      paper-input {
        flex: 1 1 auto;
        margin: 0 16px;
      }
      .search-container {
        display: inline-flex;
        width: 100%;
        align-items: center;
      }
      .prefix {
        margin: 8px;
      }
    `}};s.b([Object(o.g)()],c.prototype,"filter",void 0),c=s.b([Object(o.d)("search-input")],c)},721:function(e,t,a){"use strict";a.r(t);var s=a(3),i=a(0),o=a(73),d=(a(231),a(185),a(228),a(179),a(456)),c=a(77);const r={CELL:"mdc-data-table__cell",CELL_NUMERIC:"mdc-data-table__cell--numeric",CONTENT:"mdc-data-table__content",HEADER_ROW:"mdc-data-table__header-row",HEADER_ROW_CHECKBOX:"mdc-data-table__header-row-checkbox",ROOT:"mdc-data-table",ROW:"mdc-data-table__row",ROW_CHECKBOX:"mdc-data-table__row-checkbox",ROW_SELECTED:"mdc-data-table__row--selected"},l={ARIA_SELECTED:"aria-selected",DATA_ROW_ID_ATTR:"data-row-id",HEADER_ROW_CHECKBOX_SELECTOR:`.${r.HEADER_ROW_CHECKBOX}`,ROW_CHECKBOX_SELECTOR:`.${r.ROW_CHECKBOX}`,ROW_SELECTED_SELECTOR:`.${r.ROW_SELECTED}`,ROW_SELECTOR:`.${r.ROW}`};class n extends c.a{static get defaultAdapter(){return{addClassAtRowIndex:()=>void 0,getRowCount:()=>0,getRowElements:()=>[],getRowIdAtIndex:()=>"",getRowIndexByChildElement:()=>0,getSelectedRowCount:()=>0,isCheckboxAtRowIndexChecked:()=>!1,isHeaderRowCheckboxChecked:()=>!1,isRowsSelectable:()=>!1,notifyRowSelectionChanged:()=>void 0,notifySelectedAll:()=>void 0,notifyUnselectedAll:()=>void 0,registerHeaderRowCheckbox:()=>void 0,registerRowCheckboxes:()=>void 0,removeClassAtRowIndex:()=>void 0,setAttributeAtRowIndex:()=>void 0,setHeaderRowCheckboxChecked:()=>void 0,setHeaderRowCheckboxIndeterminate:()=>void 0,setRowCheckboxCheckedAtIndex:()=>void 0}}constructor(e){super(Object.assign({},n.defaultAdapter,e))}layout(){this.adapter_.isRowsSelectable()&&(this.adapter_.registerHeaderRowCheckbox(),this.adapter_.registerRowCheckboxes(),this.setHeaderRowCheckboxState_())}async layoutAsync(){this.adapter_.isRowsSelectable()&&(await this.adapter_.registerHeaderRowCheckbox(),await this.adapter_.registerRowCheckboxes(),this.setHeaderRowCheckboxState_())}getRows(){return this.adapter_.getRowElements()}setSelectedRowIds(e){for(let t=0;t<this.adapter_.getRowCount();t++){const a=this.adapter_.getRowIdAtIndex(t);let s=!1;a&&e.indexOf(a)>=0&&(s=!0),this.adapter_.setRowCheckboxCheckedAtIndex(t,s),this.selectRowAtIndex_(t,s)}this.setHeaderRowCheckboxState_()}getSelectedRowIds(){const e=[];for(let t=0;t<this.adapter_.getRowCount();t++)this.adapter_.isCheckboxAtRowIndexChecked(t)&&e.push(this.adapter_.getRowIdAtIndex(t));return e}handleHeaderRowCheckboxChange(){const e=this.adapter_.isHeaderRowCheckboxChecked();for(let t=0;t<this.adapter_.getRowCount();t++)this.adapter_.setRowCheckboxCheckedAtIndex(t,e),this.selectRowAtIndex_(t,e);e?this.adapter_.notifySelectedAll():this.adapter_.notifyUnselectedAll()}handleRowCheckboxChange(e){const t=this.adapter_.getRowIndexByChildElement(e.target);if(-1===t)return;const a=this.adapter_.isCheckboxAtRowIndexChecked(t);this.selectRowAtIndex_(t,a),this.setHeaderRowCheckboxState_();const s=this.adapter_.getRowIdAtIndex(t);this.adapter_.notifyRowSelectionChanged({rowId:s,rowIndex:t,selected:a})}setHeaderRowCheckboxState_(){this.adapter_.getSelectedRowCount()===this.adapter_.getRowCount()?(this.adapter_.setHeaderRowCheckboxChecked(!0),this.adapter_.setHeaderRowCheckboxIndeterminate(!1)):0===this.adapter_.getSelectedRowCount()?(this.adapter_.setHeaderRowCheckboxIndeterminate(!1),this.adapter_.setHeaderRowCheckboxChecked(!1)):(this.adapter_.setHeaderRowCheckboxIndeterminate(!0),this.adapter_.setHeaderRowCheckboxChecked(!1))}selectRowAtIndex_(e,t){t?(this.adapter_.addClassAtRowIndex(e,r.ROW_SELECTED),this.adapter_.setAttributeAtRowIndex(e,l.ARIA_SELECTED,"true")):(this.adapter_.removeClassAtRowIndex(e,r.ROW_SELECTED),this.adapter_.setAttributeAtRowIndex(e,l.ARIA_SELECTED,"false"))}}var h=a(14),_=a(650),b=a(124);a(412),a(660);const p=customElements.get("mwc-checkbox");let u=class extends p{firstUpdated(){super.firstUpdated(),this.style.setProperty("--mdc-theme-secondary","var(--primary-color)")}};u=s.b([Object(i.d)("ha-checkbox")],u);var m=a(18);let C=class extends h.a{constructor(){super(...arguments),this.columns={},this.data=[],this.selectable=!1,this.id="id",this.mdcFoundationClass=n,this._filterable=!1,this._headerChecked=!1,this._headerIndeterminate=!1,this._checkedRows=[],this._filter="",this._sortDirection=null,this._filterSortData=Object(b.a)((e,t,a,s,i)=>i?this._memSortData(this._memFilterData(e,t,a),t,s,i):this._memFilterData(e,t,a)),this._memFilterData=Object(b.a)((e,t,a)=>{if(!a)return e;const s=a.toUpperCase();return e.filter(e=>Object.entries(t).some(t=>{const[a,i]=t;return!(!i.filterable||!(i.filterKey?e[a][i.filterKey]:e[a]).toUpperCase().includes(s))}))}),this._memSortData=Object(b.a)((e,t,a,s)=>{const i=[...e],o=t[s];return i.sort((e,t)=>{let i=1;"desc"===a&&(i=-1);let d=o.filterKey?e[s][o.filterKey]:e[s],c=o.filterKey?t[s][o.filterKey]:t[s];return"string"==typeof d&&(d=d.toUpperCase()),"string"==typeof c&&(c=c.toUpperCase()),d<c?-1*i:d>c?1*i:0})})}updated(e){if(super.updated(e),e.has("columns")){this._filterable=Object.values(this.columns).some(e=>e.filterable);for(const e in this.columns)if(this.columns[e].direction){this._sortDirection=this.columns[e].direction,this._sortColumn=e;break}}}render(){return h.g`
      ${this._filterable?h.g`
            <search-input
              @value-changed=${this._handleSearchChange}
            ></search-input>
          `:""}
      <div class="mdc-data-table">
        <table class="mdc-data-table__table">
          <thead>
            <tr class="mdc-data-table__header-row">
              ${this.selectable?h.g`
                    <th
                      class="mdc-data-table__header-cell mdc-data-table__header-cell--checkbox"
                      role="columnheader"
                      scope="col"
                    >
                      <ha-checkbox
                        id="header-checkbox"
                        class="mdc-data-table__row-checkbox"
                        @change=${this._handleHeaderRowCheckboxChange}
                        .indeterminate=${this._headerIndeterminate}
                        .checked=${this._headerChecked}
                      >
                      </ha-checkbox>
                    </th>
                  `:""}
              ${Object.entries(this.columns).map(e=>{const[t,a]=e,s=t===this._sortColumn,i={"mdc-data-table__cell--numeric":Boolean(a.type&&"numeric"===a.type),sortable:Boolean(a.sortable),"not-sorted":Boolean(a.sortable&&!s)};return h.g`
                  <th
                    class="mdc-data-table__header-cell ${Object(h.d)(i)}"
                    role="columnheader"
                    scope="col"
                    @click=${this._handleHeaderClick}
                    data-column-id="${t}"
                  >
                    ${a.sortable?h.g`
                          <ha-icon
                            .icon=${s&&"desc"===this._sortDirection?"hass:arrow-down":"hass:arrow-up"}
                          ></ha-icon>
                        `:""}
                    <span>${a.title}</span>
                  </th>
                `})}
            </tr>
          </thead>
          <tbody class="mdc-data-table__content">
            ${Object(d.a)(this._filterSortData(this.data,this.columns,this._filter,this._sortDirection,this._sortColumn),e=>e[this.id],e=>h.g`
                <tr data-row-id="${e[this.id]}" class="mdc-data-table__row">
                  ${this.selectable?h.g`
                        <td
                          class="mdc-data-table__cell mdc-data-table__cell--checkbox"
                        >
                          <ha-checkbox
                            class="mdc-data-table__row-checkbox"
                            @change=${this._handleRowCheckboxChange}
                            .checked=${this._checkedRows.includes(e[this.id])}
                          >
                          </ha-checkbox>
                        </td>
                      `:""}
                  ${Object.entries(this.columns).map(t=>{const[a,s]=t;return h.g`
                      <td
                        class="mdc-data-table__cell ${Object(h.d)({"mdc-data-table__cell--numeric":Boolean(s.type&&"numeric"===s.type)})}"
                      >
                        ${s.template?s.template(e[a]):e[a]}
                      </td>
                    `})}
                </tr>
              `)}
          </tbody>
        </table>
      </div>
    `}createAdapter(){return{addClassAtRowIndex:(e,t)=>{this.rowElements[e].classList.add(t)},getRowCount:()=>this.data.length,getRowElements:()=>this.rowElements,getRowIdAtIndex:e=>this._getRowIdAtIndex(e),getRowIndexByChildElement:e=>Array.prototype.indexOf.call(this.rowElements,e.closest("tr")),getSelectedRowCount:()=>this._checkedRows.length,isCheckboxAtRowIndexChecked:e=>this._checkedRows.includes(this._getRowIdAtIndex(e)),isHeaderRowCheckboxChecked:()=>this._headerChecked,isRowsSelectable:()=>!0,notifyRowSelectionChanged:()=>void 0,notifySelectedAll:()=>void 0,notifyUnselectedAll:()=>void 0,registerHeaderRowCheckbox:()=>void 0,registerRowCheckboxes:()=>void 0,removeClassAtRowIndex:(e,t)=>{this.rowElements[e].classList.remove(t)},setAttributeAtRowIndex:(e,t,a)=>{this.rowElements[e].setAttribute(t,a)},setHeaderRowCheckboxChecked:e=>{this._headerChecked=e},setHeaderRowCheckboxIndeterminate:e=>{this._headerIndeterminate=e},setRowCheckboxCheckedAtIndex:(e,t)=>{this._setRowChecked(this._getRowIdAtIndex(e),t)}}}_getRowIdAtIndex(e){return this.rowElements[e].getAttribute("data-row-id")}_handleHeaderClick(e){const t=e.target.closest("th").getAttribute("data-column-id");this.columns[t].sortable&&(this._sortDirection&&this._sortColumn===t?"asc"===this._sortDirection?this._sortDirection="desc":this._sortDirection=null:this._sortDirection="asc",this._sortColumn=null===this._sortDirection?void 0:t,Object(m.a)(this,"sorting-changed",{column:t,direction:this._sortDirection}))}_handleHeaderRowCheckboxChange(){this._headerChecked=this._headerCheckbox.checked,this._headerIndeterminate=this._headerCheckbox.indeterminate,this.mdcFoundation.handleHeaderRowCheckboxChange()}_handleRowCheckboxChange(e){const t=e.target,a=t.parentElement.parentElement.getAttribute("data-row-id");this._setRowChecked(a,t.checked),this.mdcFoundation.handleRowCheckboxChange(e)}_setRowChecked(e,t){if(t&&!this._checkedRows.includes(e))this._checkedRows=[...this._checkedRows,e];else if(!t){const t=this._checkedRows.indexOf(e);-1!==t&&this._checkedRows.splice(t,1)}Object(m.a)(this,"selection-changed",{id:e,selected:t})}_handleSearchChange(e){this._filter=e.detail.value}static get styles(){return h.e`
      ${Object(h.l)(_.a)}
      .mdc-data-table {
        display: block;
      }
      .mdc-data-table__header-cell {
        overflow: hidden;
      }
      .mdc-data-table__header-cell.sortable {
        cursor: pointer;
      }
      .mdc-data-table__header-cell.not-sorted:not(.mdc-data-table__cell--numeric)
        span {
        position: relative;
        left: -24px;
      }
      .mdc-data-table__header-cell.not-sorted > * {
        transition: left 0.2s ease 0s;
      }
      .mdc-data-table__header-cell.not-sorted ha-icon {
        left: -36px;
      }
      .mdc-data-table__header-cell.not-sorted:not(.mdc-data-table__cell--numeric):hover
        span {
        left: 0px;
      }
      .mdc-data-table__header-cell:hover.not-sorted ha-icon {
        left: 0px;
      }
    `}};s.b([Object(h.i)({type:Object})],C.prototype,"columns",void 0),s.b([Object(h.i)({type:Array})],C.prototype,"data",void 0),s.b([Object(h.i)({type:Boolean})],C.prototype,"selectable",void 0),s.b([Object(h.i)({type:String})],C.prototype,"id",void 0),s.b([Object(h.j)(".mdc-data-table")],C.prototype,"mdcRoot",void 0),s.b([Object(h.k)(".mdc-data-table__row")],C.prototype,"rowElements",void 0),s.b([Object(h.j)("#header-checkbox")],C.prototype,"_headerCheckbox",void 0),s.b([Object(h.i)({type:Boolean})],C.prototype,"_filterable",void 0),s.b([Object(h.i)({type:Boolean})],C.prototype,"_headerChecked",void 0),s.b([Object(h.i)({type:Boolean})],C.prototype,"_headerIndeterminate",void 0),s.b([Object(h.i)({type:Array})],C.prototype,"_checkedRows",void 0),s.b([Object(h.i)({type:String})],C.prototype,"_filter",void 0),s.b([Object(h.i)({type:String})],C.prototype,"_sortColumn",void 0),s.b([Object(h.i)({type:String})],C.prototype,"_sortDirection",void 0),C=s.b([Object(h.f)("ha-data-table")],C);var w=a(176),g=a(121),R=a(96);const x=["zone"],f=(e,t)=>{if("call-service"!==t.action||!t.service_data||!t.service_data.entity_id)return;let a=t.service_data.entity_id;Array.isArray(a)||(a=[a]);for(const s of a)e.add(s)},k=(e,t)=>{"string"!=typeof t?(t.entity&&e.add(t.entity),t.camera_image&&e.add(t.camera_image),t.tap_action&&f(e,t.tap_action),t.hold_action&&f(e,t.hold_action)):e.add(t)},y=(e,t)=>{t.entity&&k(e,t.entity),t.entities&&t.entities.forEach(t=>k(e,t)),t.card&&y(e,t.card),t.cards&&t.cards.forEach(t=>y(e,t)),t.elements&&t.elements.forEach(t=>y(e,t)),t.badges&&t.badges.forEach(t=>k(e,t))},v=(e,t)=>{const a=(e=>{const t=new Set;return e.views.forEach(e=>y(t,e)),t})(t);return Object.keys(e.states).filter(e=>!a.has(e)&&!x.includes(e.split(".",1)[0])).sort()};var E=a(399);a.d(t,"HuiUnusedEntities",function(){return O});let O=class extends i.a{constructor(){super(...arguments),this._unusedEntities=[],this._selectedEntities=[],this._columns={entity:{title:"Entity",sortable:!0,filterable:!0,filterKey:"friendly_name",direction:"asc",template:e=>i.f`
        <state-badge .hass=${this.hass} .stateObj=${e}></state-badge>
        ${e.friendly_name}
      `},entity_id:{title:"Entity id",sortable:!0,filterable:!0},domain:{title:"Domain",sortable:!0,filterable:!0},last_changed:{title:"Last Changed",type:"numeric",sortable:!0,template:e=>i.f`
        <ha-relative-time
          .hass=${this.hass}
          .datetime=${e}
        ></ha-relative-time>
      `}}}get _config(){return this.lovelace.config}updated(e){super.updated(e),e.has("lovelace")&&this._getUnusedEntities()}render(){return this.hass&&this.lovelace?"storage"===this.lovelace.mode&&!1===this.lovelace.editMode?i.f``:i.f`
      <ha-card header="Unused entities">
        <div class="card-content">
          These are the entities that you have available, but are not in your
          Lovelace UI yet.
          ${"storage"===this.lovelace.mode?i.f`
                <br />Select the entities you want to add to a card and then
                click the add card button.
              `:""}
        </div>
      </ha-card>
      <ha-data-table
        .columns=${this._columns}
        .data=${this._unusedEntities.map(e=>{const t=this.hass.states[e];return{entity_id:e,entity:Object.assign({},t,{friendly_name:Object(w.a)(t)}),domain:Object(g.a)(e),last_changed:t.last_changed}})}
        .id=${"entity_id"}
        .selectable=${"storage"===this.lovelace.mode}
        @selection-changed=${this._handleSelectionChanged}
      ></ha-data-table>
      ${"storage"===this.lovelace.mode?i.f`
            <ha-fab
              class="${Object(o.a)({rtl:Object(R.a)(this.hass)})}"
              icon="hass:plus"
              label="${this.hass.localize("ui.panel.lovelace.editor.edit_card.add")}"
              @click="${this._selectView}"
            ></ha-fab>
          `:""}
    `:i.f``}_getUnusedEntities(){this.hass&&this.lovelace&&(this._selectedEntities=[],this._unusedEntities=v(this.hass,this._config))}_handleSelectionChanged(e){const t=e.detail,a=t.id;if(t.selected)this._selectedEntities.push(a);else{const e=this._selectedEntities.indexOf(a);-1!==e&&this._selectedEntities.splice(e,1)}}_selectView(){var e,t;e=this,t={lovelace:this.lovelace,viewSelectedCallback:e=>this._addCard(e)},Object(m.a)(e,"show-dialog",{dialogTag:"hui-dialog-select-view",dialogImport:()=>a.e(46).then(a.bind(null,711)),dialogParams:t})}_addCard(e){Object(E.a)(this,{lovelace:this.lovelace,path:[e],entities:this._selectedEntities})}static get styles(){return i.c`
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
      ha-card {
        margin-bottom: 16px;
      }
    `}};s.b([Object(i.g)()],O.prototype,"lovelace",void 0),s.b([Object(i.g)()],O.prototype,"hass",void 0),s.b([Object(i.g)()],O.prototype,"_unusedEntities",void 0),O=s.b([Object(i.d)("hui-unused-entities")],O)}}]);
//# sourceMappingURL=chunk.182df8421368dfaf489e.js.map