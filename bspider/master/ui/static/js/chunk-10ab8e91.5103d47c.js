(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-10ab8e91"],{"0f66":function(e,t,n){"use strict";n.d(t,"c",(function(){return i})),n.d(t,"b",(function(){return o})),n.d(t,"e",(function(){return r})),n.d(t,"d",(function(){return l})),n.d(t,"f",(function(){return s})),n.d(t,"a",(function(){return u}));n("386d");var a=n("b775");function i(e){return Object(a["a"])({url:"/node",method:"GET",params:{page:e.page,limit:e.limit,search:e.search}})}function o(e){return Object(a["a"])({url:"/node/"+e,method:"GET"})}function r(e,t){return Object(a["a"])({url:"/node/"+t,method:"PATCH",data:e})}function l(e){return Object(a["a"])({url:"/worker",method:"GET",params:{page:e.page,limit:e.limit,search:e.search}})}function s(e,t){return Object(a["a"])({url:"/worker/"+t,method:"PATCH",data:e})}function u(e){return Object(a["a"])({url:"/worker",method:"POST",data:e})}},"121a":function(e,t,n){"use strict";n.d(t,"e",(function(){return i})),n.d(t,"d",(function(){return o})),n.d(t,"h",(function(){return r})),n.d(t,"b",(function(){return l})),n.d(t,"a",(function(){return s})),n.d(t,"f",(function(){return u})),n.d(t,"g",(function(){return c})),n.d(t,"c",(function(){return d}));var a=n("b775");function i(){return Object(a["a"])({url:"/tools/node-list",method:"GET"})}function o(e){return Object(a["a"])({url:"/tools/code-list",method:"GET",params:e})}function r(e){return Object(a["a"])({url:"/tools/validate/crontab",method:"GET",params:e})}function l(e){return Object(a["a"])({url:"/tools/parser/exception/"+e,method:"GET"})}function s(e){return Object(a["a"])({url:"/tools/downloader/exception/"+e,method:"GET"})}function u(e){return Object(a["a"])({url:"/tools/crawl-detail",method:"GET",params:e})}function c(){return Object(a["a"])({url:"/tools/node-detail",method:"GET"})}function d(){return Object(a["a"])({url:"/tools/exception-project",method:"GET"})}},1962:function(e,t,n){"use strict";function a(e,t){for(var n=[],a=0,i=t.length;a<i;a++)void 0!==e[t[a]]&&null!==e[t[a]]&&n.push(t[a]+"="+e[t[a]]);return n.join(",")}n.d(t,"a",(function(){return a}))},"333d":function(e,t,n){"use strict";var a=function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("div",{staticClass:"pagination-container",class:{hidden:e.hidden}},[n("el-pagination",e._b({attrs:{background:e.background,"current-page":e.currentPage,"page-size":e.pageSize,layout:e.layout,"page-sizes":e.pageSizes,total:e.total},on:{"update:currentPage":function(t){e.currentPage=t},"update:current-page":function(t){e.currentPage=t},"update:pageSize":function(t){e.pageSize=t},"update:page-size":function(t){e.pageSize=t},"size-change":e.handleSizeChange,"current-change":e.handleCurrentChange}},"el-pagination",e.$attrs,!1))],1)},i=[];n("c5f6");Math.easeInOutQuad=function(e,t,n,a){return e/=a/2,e<1?n/2*e*e+t:(e--,-n/2*(e*(e-2)-1)+t)};var o=function(){return window.requestAnimationFrame||window.webkitRequestAnimationFrame||window.mozRequestAnimationFrame||function(e){window.setTimeout(e,1e3/60)}}();function r(e){document.documentElement.scrollTop=e,document.body.parentNode.scrollTop=e,document.body.scrollTop=e}function l(){return document.documentElement.scrollTop||document.body.parentNode.scrollTop||document.body.scrollTop}function s(e,t,n){var a=l(),i=e-a,s=20,u=0;t="undefined"===typeof t?500:t;var c=function e(){u+=s;var l=Math.easeInOutQuad(u,a,i,t);r(l),u<t?o(e):n&&"function"===typeof n&&n()};c()}var u={name:"Pagination",props:{total:{required:!0,type:Number},page:{type:Number,default:1},limit:{type:Number,default:20},pageSizes:{type:Array,default:function(){return[10,20,30,50]}},layout:{type:String,default:"total, sizes, prev, pager, next, jumper"},background:{type:Boolean,default:!0},autoScroll:{type:Boolean,default:!0},hidden:{type:Boolean,default:!1}},computed:{currentPage:{get:function(){return this.page},set:function(e){this.$emit("update:page",e)}},pageSize:{get:function(){return this.limit},set:function(e){this.$emit("update:limit",e)}}},methods:{handleSizeChange:function(e){this.$emit("pagination",{page:this.currentPage,limit:e}),this.autoScroll&&s(0,800)},handleCurrentChange:function(e){this.$emit("pagination",{page:e,limit:this.pageSize}),this.autoScroll&&s(0,800)}}},c=u,d=(n("e498"),n("2877")),p=Object(d["a"])(c,a,i,!1,null,"6af373ef",null);t["a"]=p.exports},6724:function(e,t,n){"use strict";n("8d41");var a="@@wavesContext";function i(e,t){function n(n){var a=Object.assign({},t.value),i=Object.assign({ele:e,type:"hit",color:"rgba(0, 0, 0, 0.15)"},a),o=i.ele;if(o){o.style.position="relative",o.style.overflow="hidden";var r=o.getBoundingClientRect(),l=o.querySelector(".waves-ripple");switch(l?l.className="waves-ripple":(l=document.createElement("span"),l.className="waves-ripple",l.style.height=l.style.width=Math.max(r.width,r.height)+"px",o.appendChild(l)),i.type){case"center":l.style.top=r.height/2-l.offsetHeight/2+"px",l.style.left=r.width/2-l.offsetWidth/2+"px";break;default:l.style.top=(n.pageY-r.top-l.offsetHeight/2-document.documentElement.scrollTop||document.body.scrollTop)+"px",l.style.left=(n.pageX-r.left-l.offsetWidth/2-document.documentElement.scrollLeft||document.body.scrollLeft)+"px"}return l.style.backgroundColor=i.color,l.className="waves-ripple z-active",!1}}return e[a]?e[a].removeHandle=n:e[a]={removeHandle:n},n}var o={bind:function(e,t){e.addEventListener("click",i(e,t),!1)},update:function(e,t){e.removeEventListener("click",e[a].removeHandle,!1),e.addEventListener("click",i(e,t),!1)},unbind:function(e){e.removeEventListener("click",e[a].removeHandle,!1),e[a]=null,delete e[a]}},r=function(e){e.directive("waves",o)};window.Vue&&(window.waves=o,Vue.use(r)),o.install=r;t["a"]=o},"6dc2":function(e,t,n){"use strict";n.r(t);var a=function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("div",{staticClass:"app-container"},[n("div",{staticClass:"filter-container"},[n("el-input",{staticClass:"filter-item",staticStyle:{width:"190px"},attrs:{placeholder:"worker name"},nativeOn:{keyup:function(t){return!t.type.indexOf("key")&&e._k(t.keyCode,"enter",13,t.key,"Enter")?null:e.handleFilter(t)}},model:{value:e.listQuery.name,callback:function(t){e.$set(e.listQuery,"name",t)},expression:"listQuery.name"}}),e._v(" "),n("el-select",{staticClass:"filter-item",staticStyle:{width:"160px"},attrs:{placeholder:"node ip",clearable:""},model:{value:e.listQuery.ip,callback:function(t){e.$set(e.listQuery,"ip",t)},expression:"listQuery.ip"}},e._l(e.nodeIpOptions,(function(e){return n("el-option",{key:e.ip,attrs:{label:e.ip,value:e.ip}})})),1),e._v(" "),n("el-select",{staticClass:"filter-item",staticStyle:{width:"150px"},attrs:{placeholder:"worker type",clearable:""},model:{value:e.listQuery.type,callback:function(t){e.$set(e.listQuery,"type",t)},expression:"listQuery.type"}},e._l(e.workerTypeOptions,(function(e){return n("el-option",{key:e.key,attrs:{label:e.display_name,value:e.key}})})),1),e._v(" "),n("el-button",{directives:[{name:"waves",rawName:"v-waves"}],staticClass:"filter-item",attrs:{type:"primary",icon:"el-icon-search"},on:{click:e.handleFilter}},[e._v("\n      Search\n    ")]),e._v(" "),n("el-button",{staticClass:"filter-item",staticStyle:{"margin-left":"10px"},attrs:{type:"primary",icon:"el-icon-edit"},on:{click:e.createWorkerHandler}},[e._v("\n      Add worker\n    ")]),e._v(" "),n("el-checkbox",{staticClass:"filter-item",staticStyle:{"margin-left":"15px"},on:{change:function(t){e.tableKey=e.tableKey+1}},model:{value:e.showTime,callback:function(t){e.showTime=t},expression:"showTime"}},[e._v("\n      create&update time\n    ")])],1),e._v(" "),n("el-table",{directives:[{name:"loading",rawName:"v-loading",value:e.listLoading,expression:"listLoading"}],key:e.tableKey,attrs:{data:e.list,border:"",fit:"","highlight-current-row":""}},[n("el-table-column",{attrs:{label:"Node IP",align:"center",width:"95px"},scopedSlots:e._u([{key:"default",fn:function(t){return[n("span",[e._v(e._s(t.row.ip))])]}}])}),e._v(" "),n("el-table-column",{attrs:{label:"Name",width:"120px",align:"center"},scopedSlots:e._u([{key:"default",fn:function(t){return[n("span",[e._v(e._s(t.row.name))])]}}])}),e._v(" "),n("el-table-column",{attrs:{label:"Worker PID",width:"100px",align:"center"},scopedSlots:e._u([{key:"default",fn:function(t){return[n("span",[e._v(e._s(t.row.pid))])]}}])}),e._v(" "),n("el-table-column",{attrs:{label:"Type",width:"110px",align:"center"},scopedSlots:e._u([{key:"default",fn:function(t){var a=t.row;return[n("el-tag",{attrs:{type:e._f("typeFilter")(a.type)}},[e._v("\n          "+e._s(a.type)+"\n        ")])]}}])}),e._v(" "),n("el-table-column",{attrs:{label:"Status","class-name":"status-col",width:"90px"},scopedSlots:e._u([{key:"default",fn:function(t){var a=t.row;return[n("el-tag",{attrs:{type:e._f("statusFilter")(a.status)}},[e._v("\n          "+e._s(e._f("statusName")(a.status))+"\n        ")])]}}])}),e._v(" "),n("el-table-column",{attrs:{label:"description",align:"center"},scopedSlots:e._u([{key:"default",fn:function(t){return[n("span",[e._v(e._s(t.row.description))])]}}])}),e._v(" "),e.showTime?n("el-table-column",{attrs:{label:"Create Time",width:"160px",align:"center"},scopedSlots:e._u([{key:"default",fn:function(t){return[n("span",[e._v(e._s(t.row.create_time))])]}}],null,!1,570062024)}):e._e(),e._v(" "),e.showTime?n("el-table-column",{attrs:{label:"Update Time",width:"160px",align:"center"},scopedSlots:e._u([{key:"default",fn:function(t){return[n("span",[e._v(e._s(t.row.update_time))])]}}],null,!1,3312930237)}):e._e(),e._v(" "),n("el-table-column",{attrs:{label:"Actions",align:"center",width:"180","class-name":"small-padding fixed-width"},scopedSlots:e._u([{key:"default",fn:function(t){var a=t.row;return[n("el-button",{attrs:{type:"primary",size:"mini"},on:{click:function(t){return e.updateWorkerHandler(a)}}},[e._v("\n          Edit\n        ")]),e._v(" "),1===a.status?n("el-button",{attrs:{size:"mini",type:"danger"},on:{click:function(t){return e.changeWorkerStatusHandler(a,0)}}},[e._v("\n          Stop\n        ")]):e._e(),e._v(" "),1!==a.status?n("el-button",{attrs:{size:"mini"},on:{click:function(t){return e.changeWorkerStatusHandler(a,1)}}},[e._v("\n          Start\n        ")]):e._e()]}}])})],1),e._v(" "),n("pagination",{directives:[{name:"show",rawName:"v-show",value:e.total>0,expression:"total>0"}],attrs:{total:e.total,page:e.listQuery.page,limit:e.listQuery.limit},on:{"update:page":function(t){return e.$set(e.listQuery,"page",t)},"update:limit":function(t){return e.$set(e.listQuery,"limit",t)},pagination:e.getList}}),e._v(" "),n("el-dialog",{attrs:{title:e.textMap[e.dialogStatus],visible:e.dialogFormVisible},on:{"update:visible":function(t){e.dialogFormVisible=t}}},[n("el-form",{ref:"dataPostForm",staticStyle:{width:"450px","margin-left":"50px"},attrs:{rules:e.rules,model:e.dialogPostForm,"label-position":"right","label-width":"110px"}},[n("el-form-item",{attrs:{label:"Name",prop:"name"}},[n("el-input",{model:{value:e.dialogPostForm.name,callback:function(t){e.$set(e.dialogPostForm,"name",t)},expression:"dialogPostForm.name"}})],1),e._v(" "),n("el-form-item",{attrs:{label:"Worker Type",prop:"type"}},[n("el-select",{staticClass:"filter-item",attrs:{placeholder:"Please select"},model:{value:e.dialogPostForm.type,callback:function(t){e.$set(e.dialogPostForm,"type",t)},expression:"dialogPostForm.type"}},e._l(e.workerTypeOptions,(function(e){return n("el-option",{key:e.key,attrs:{label:e.display_name,value:e.key}})})),1)],1),e._v(" "),n("el-form-item",{attrs:{label:"Node Ip",prop:"ip"}},[n("el-select",{staticClass:"filter-item",attrs:{placeholder:"Please select"},model:{value:e.dialogPostForm.ip,callback:function(t){e.$set(e.dialogPostForm,"ip",t)},expression:"dialogPostForm.ip"}},e._l(e.nodeIpOptions,(function(e){return n("el-option",{key:e.ip,attrs:{label:e.ip,value:e.ip}})})),1)],1),e._v(" "),n("el-form-item",{attrs:{label:"Desc",prop:"description"}},[n("el-input",{attrs:{autosize:{minRows:2,maxRows:4},type:"textarea",placeholder:"Please input desc"},model:{value:e.dialogPostForm.description,callback:function(t){e.$set(e.dialogPostForm,"description",t)},expression:"dialogPostForm.description"}})],1)],1),e._v(" "),n("div",{staticClass:"dialog-footer",attrs:{slot:"footer"},slot:"footer"},[n("el-button",{on:{click:function(t){e.dialogFormVisible=!1}}},[e._v("\n        Cancel\n      ")]),e._v(" "),n("el-button",{attrs:{type:"primary"},on:{click:function(t){"create"===e.dialogStatus?e.createData():e.updateData()}}},[e._v("\n        Confirm\n      ")])],1)],1)],1)},i=[],o=(n("6b54"),n("0f66")),r=n("121a"),l=n("6724"),s=n("333d"),u=n("1962"),c={name:"List",components:{Pagination:s["a"]},directives:{waves:l["a"]},filters:{statusFilter:function(e){var t={1:"success",0:"danger","-1":"warning"};return t[e.toString()]},statusName:function(e){var t={1:"running",0:"closed","-1":"fatal"};return t[e.toString()]},typeFilter:function(e){var t={downloader:"",parser:"info"};return t[e]}},props:{isDetail:{type:Boolean,default:!1}},data:function(){return{tableKey:0,list:null,total:0,listLoading:!0,listQuery:{page:1,limit:10,name:void 0,ip:void 0,type:void 0,search:void 0},workerTypeOptions:[{key:"parser",display_name:"parser"},{key:"downloader",display_name:"downloader"}],nodeIpOptions:[],statusMap:{1:"run",0:"close","-1":"fatal"},dialogFormVisible:!1,dialogStatus:"",textMap:{update:"Edit",create:"Create"},dialogPostForm:{},rules:{name:[{required:!0,message:"Please input worker's name",trigger:"blur"},{min:1,max:20,message:"1 to 20 characters in length",trigger:"blur"}],type:[{required:!0,message:"Please select this worker type",trigger:"blur"}],ip:[{required:!0,message:"Please select this node ip",trigger:"blur"}],description:[{required:!0,message:"Please input worker's description",trigger:"blur"},{min:1,max:70,message:"1 to 70 characters in length",trigger:"blur"}]},showTime:!1}},created:function(){this.getNodeIpOptions(),this.getList()},methods:{getList:function(){var e=this;this.listLoading=!0,this.listQuery.search=Object(u["a"])(this.listQuery,["name","ip","type"]),Object(o["d"])(this.listQuery).then((function(t){e.list=t.data.items,e.total=t.data.total,setTimeout((function(){e.listLoading=!1}),1500)}))},getNodeIpOptions:function(){var e=this;Object(r["e"])(this.listQuery).then((function(t){e.nodeIpOptions=t.data}))},handleFilter:function(){this.listQuery.page=1,this.getList()},createWorkerHandler:function(){var e=this;this.resetTemp(),this.dialogStatus="create",this.dialogFormVisible=!0,this.$nextTick((function(){e.$refs.dataPostForm.clearValidate()}))},updateWorkerHandler:function(e){var t=this;this.dialogPostForm=Object.assign({},e),this.dialogStatus="update",this.dialogFormVisible=!0,this.$nextTick((function(){t.$refs.dataPostForm.clearValidate()}))},resetTemp:function(){this.dialogPostForm={name:void 0,ip:this.listQuery.ip,type:void 0,description:void 0,status:void 0}},changeWorkerStatusHandler:function(e,t){var n=this;Object(o["f"])({status:t},e.id).then((function(a){0===a.errno&&(n.$message({message:n.statusMap[t.toString()]+" worker "+e.ip+" success",type:"success"}),1!==t?(e.status=t,e.pid=t):n.getList())})).catch((function(e){console.log(e)}))},updateData:function(){var e=this;this.$refs.dataPostForm.validate((function(t){t&&Object(o["f"])(e.dialogPostForm,e.dialogPostForm.id).then((function(t){0===t.errno&&(e.$message({message:t.msg,type:"success"}),e.dialogFormVisible=!1,e.getList())})).catch((function(e){console.log(e)}))}))},createData:function(){var e=this;this.$refs.dataPostForm.validate((function(t){t&&Object(o["a"])(e.dialogPostForm).then((function(t){0===t.errno&&(e.$message({message:t.msg,type:"success"}),e.dialogFormVisible=!1)})).catch((function(e){console.log(e)}))}))}}},d=c,p=n("2877"),m=Object(p["a"])(d,a,i,!1,null,null,null);t["default"]=m.exports},7456:function(e,t,n){},"8d41":function(e,t,n){},e498:function(e,t,n){"use strict";n("7456")}}]);