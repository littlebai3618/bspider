(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-0d31cc8e"],{"121a":function(t,e,a){"use strict";a.d(e,"e",(function(){return r})),a.d(e,"d",(function(){return s})),a.d(e,"h",(function(){return o})),a.d(e,"b",(function(){return i})),a.d(e,"a",(function(){return c})),a.d(e,"f",(function(){return l})),a.d(e,"g",(function(){return u})),a.d(e,"c",(function(){return d}));var n=a("b775");function r(){return Object(n["a"])({url:"/tools/node-list",method:"GET"})}function s(t){return Object(n["a"])({url:"/tools/code-list",method:"GET",params:t})}function o(t){return Object(n["a"])({url:"/tools/validate/crontab",method:"GET",params:t})}function i(t){return Object(n["a"])({url:"/tools/parser/exception/"+t,method:"GET"})}function c(t){return Object(n["a"])({url:"/tools/downloader/exception/"+t,method:"GET"})}function l(t){return Object(n["a"])({url:"/tools/crawl-detail",method:"GET",params:t})}function u(){return Object(n["a"])({url:"/tools/node-detail",method:"GET"})}function d(){return Object(n["a"])({url:"/tools/exception-project",method:"GET"})}},"1e0e":function(t,e,a){},"24d2":function(t,e,a){"use strict";a.d(e,"d",(function(){return r})),a.d(e,"c",(function(){return s})),a.d(e,"a",(function(){return o})),a.d(e,"e",(function(){return i})),a.d(e,"b",(function(){return c}));a("386d");var n=a("b775");function r(t){return Object(n["a"])({url:"/project",method:"GET",params:{page:t.page,limit:t.limit,search:t.search}})}function s(t){return Object(n["a"])({url:"/project/"+t,method:"GET"})}function o(t){return Object(n["a"])({url:"/project",method:"POST",data:t})}function i(t,e){return Object(n["a"])({url:"/project/"+e,method:"PATCH",data:t})}function c(t){return Object(n["a"])({url:"/project/"+t,method:"DELETE"})}},"357a":function(t,e,a){"use strict";var n=function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("div",{class:t.className,style:{height:t.height,width:"100%"}})},r=[],s=a("313e"),o=a.n(s),i=a("f42c");a("817d");var c={name:"TwoLineChart",mixins:[i["a"]],props:{className:{type:String,default:"chart"},width:{type:String,default:"100%"},height:{type:String,default:"350px"},autoResize:{type:Boolean,default:!0}},data:function(){return{chart:null}},mounted:function(){var t=this;this.$nextTick((function(){t.initChart()}))},beforeDestroy:function(){this.chart&&(this.chart.dispose(),this.chart=null)},methods:{initChart:function(){this.chart=o.a.init(this.$el,"macarons")},setOptions:function(){var t=arguments.length>0&&void 0!==arguments[0]?arguments[0]:{},e=t.xAxis,a=t.legend,n=t.series;this.chart.setOption({xAxis:{data:e,boundaryGap:!1,axisTick:{show:!1}},grid:{left:10,right:10,bottom:20,top:30,containLabel:!0},tooltip:{trigger:"axis",axisPointer:{type:"cross"},padding:[5,10]},yAxis:{axisTick:{show:!1}},legend:{data:a},series:n})}}},l=c,u=a("2877"),d=Object(u["a"])(l,n,r,!1,null,null,null);e["a"]=d.exports},"891b":function(t,e,a){"use strict";a("1e0e")},"918e":function(t,e,a){"use strict";a.r(e);var n=function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("div",{staticClass:"app-container"},[a("el-row",{attrs:{gutter:10}},[a("el-col",{attrs:{span:5}},[a("el-row",[a("el-card",{staticClass:"detail-wrapper"},[a("div",{staticClass:"clearfix",attrs:{slot:"header"},slot:"header"},[a("span",[t._v("Base Info")])]),t._v(" "),a("div",{staticClass:"text item"},[a("el-row",[a("el-col",{attrs:{span:10}},[a("div",{staticClass:"content-key"},[t._v("ID:")])]),t._v(" "),a("el-col",{attrs:{span:14}},[a("div",{staticClass:"content-value"},[t._v("\n                  "+t._s(t.projectBaseInfo.id)+"\n                  "),a("el-button",{staticStyle:{padding:"3px 0"},attrs:{type:"text"},on:{click:function(e){return t.updateProjectHandler(t.projectBaseInfo.id)}}},[t._v(" Edit ")])],1)])],1),t._v(" "),a("el-row",[a("el-col",{attrs:{span:10}},[a("div",{staticClass:"content-key"},[t._v("Name:")])]),t._v(" "),a("el-col",{attrs:{span:14}},[a("div",{staticClass:"content-value"},[t._v(t._s(t.projectBaseInfo.name))])])],1),t._v(" "),a("el-row",[a("el-col",{attrs:{span:10}},[a("div",{staticClass:"content-key"},[t._v("Editor:")])]),t._v(" "),a("el-col",{attrs:{span:14}},[a("div",{staticClass:"content-value"},[t._v(t._s(t.projectBaseInfo.editor))])])],1),t._v(" "),a("el-row",[a("el-col",{attrs:{span:10}},[a("div",{staticClass:"content-key"},[t._v("Group:")])]),t._v(" "),a("el-col",{attrs:{span:14}},[a("div",{staticClass:"content-value"},[t._v(t._s(t.projectBaseInfo.group))])])],1),t._v(" "),a("el-row",[a("el-col",{attrs:{span:10}},[a("div",{staticClass:"content-key"},[t._v("Status:")])]),t._v(" "),a("el-col",{attrs:{span:14}},[a("div",{staticClass:"content-value"},[a("el-tag",{attrs:{type:t._f("statusFilter")(t.projectBaseInfo.status),size:"mini"}},[t._v("\n                    "+t._s(t._f("statusName")(t.projectBaseInfo.status))+"\n                  ")])],1)])],1),t._v(" "),a("el-row",[a("el-col",{attrs:{span:10}},[a("div",{staticClass:"content-key"},[t._v("Rate:")])]),t._v(" "),a("el-col",{attrs:{span:14}},[a("el-tag",{attrs:{size:"mini"}},[t._v(t._s(t.projectBaseInfo.rate)+" R/min")])],1)],1),t._v(" "),a("el-row",[a("el-col",{attrs:{span:10}},[a("div",{staticClass:"content-key"},[t._v("Description:")])]),t._v(" "),a("el-col",{attrs:{span:14}},[a("div",{staticClass:"content-value"},[t._v(t._s(t.projectBaseInfo.description))])])],1),t._v(" "),a("el-row",[a("el-col",{attrs:{span:10}},[a("div",{staticClass:"content-key"},[t._v("Create:")])]),t._v(" "),a("el-col",{attrs:{span:14}},[a("div",{staticClass:"content-value"},[t._v(t._s(t.projectBaseInfo.create_time))])])],1),t._v(" "),a("el-row",[a("el-col",{attrs:{span:10}},[a("div",{staticClass:"content-key"},[t._v("Update:")])]),t._v(" "),a("el-col",{attrs:{span:14}},[a("div",{staticClass:"content-value"},[t._v(t._s(t.projectBaseInfo.update_time))])])],1)],1)])],1),t._v(" "),a("el-row",[a("el-card",{staticClass:"detail-wrapper"},[a("div",{staticClass:"clearfix",attrs:{slot:"header"},slot:"header"},[a("span",[t._v("Queue Info")])]),t._v(" "),a("div",{staticClass:"text item"},[a("el-row",[a("el-col",{attrs:{span:10}},[a("div",{staticClass:"content-key"},[t._v("Candidate:")])]),t._v(" "),a("el-col",{attrs:{span:14}},[a("div",{staticClass:"content-value"},[t._v("\n                  "+t._s(t.projectQueueInfo.candidate.total[0]+" - "+t.projectQueueInfo.candidate.total[1]+" R/s")+"\n                  "),a("el-button",{staticStyle:{padding:"3px 0"},attrs:{type:"text"},on:{click:t.purgeRequestHandler}},[t._v(" Purge ")])],1)])],1),t._v(" "),a("el-row",[a("el-col",{attrs:{span:10}},[a("div",{staticClass:"content-key"},[t._v("Download:")])]),t._v(" "),a("el-col",{attrs:{span:14}},[a("div",{staticClass:"content-value"},[t._v("\n                  "+t._s(t.projectQueueInfo.download.total[0]+" - "+t.projectQueueInfo.download.total[1]+" R/s")+"\n                ")])])],1),t._v(" "),a("el-row",[a("el-col",{attrs:{span:10}},[a("div",{staticClass:"content-key"},[t._v("Parse:")])]),t._v(" "),a("el-col",{attrs:{span:14}},[a("div",{staticClass:"content-value"},[t._v("\n                  "+t._s(t.projectQueueInfo.parse.total[0]+" - "+t.projectQueueInfo.parse.total[1]+" R/s")+"\n                ")])])],1)],1)])],1)],1),t._v(" "),a("el-col",{attrs:{span:19}},[a("el-tabs",{attrs:{type:"border-card"},model:{value:t.activeName,callback:function(e){t.activeName=e},expression:"activeName"}},[a("el-tab-pane",{attrs:{label:"Downloader Status",name:"Downloader Status",lazy:!0}},[a("keep-alive",[a("project-status-chart",{attrs:{"project-id":t.projectId,"status-type":"downloader"}})],1)],1),t._v(" "),a("el-tab-pane",{attrs:{label:"Downloader Exception",name:"Downloader Exception",lazy:!0}},[a("ProjectException",{attrs:{"project-id":t.projectId,"status-type":"downloader"}})],1),t._v(" "),a("el-tab-pane",{attrs:{label:"Parser Status",name:"Parser Status",lazy:!0}},[a("project-status-chart",{attrs:{"project-id":t.projectId,"status-type":"parser"}})],1),t._v(" "),a("el-tab-pane",{attrs:{label:"Parser Exception",name:"Parser Exception",lazy:!0}},[a("ProjectException",{attrs:{"project-id":t.projectId,"status-type":"parser"}})],1)],1)],1)],1)],1)},r=[],s=a("24d2"),o=a("b775");function i(t){return Object(o["a"])({url:"rabbitmq/project/"+t,method:"GET"})}function c(t){return Object(o["a"])({url:"rabbitmq/project/purge/"+t,method:"DELETE"})}var l=function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("two-line-chart",{ref:"lineChart",attrs:{width:"100%",height:t.height+"px"}})},u=[],d=a("c638"),p=a("357a"),f={name:"DownloadStatus",components:{TwoLineChart:p["a"]},props:{statusType:{type:String,default:"downloader"},projectId:{type:String,default:"0"}},data:function(){return{height:window.innerHeight-210}},created:function(){this.fetchProjectInfoChart()},methods:{fetchProjectInfoChart:function(){var t=this;"downloader"===this.statusType?Object(d["c"])(this.projectId).then((function(e){t.$refs.lineChart.setOptions(e.data)})).catch((function(t){console.log(t)})):Object(d["e"])(this.projectId).then((function(e){t.$refs.lineChart.setOptions(e.data)})).catch((function(t){console.log(t)}))}}},h=f,v=a("2877"),_=Object(v["a"])(h,l,u,!1,null,null,null),m=_.exports,j=function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("el-timeline",t._l(t.timeLineData,(function(e,n){return a("el-timeline-item",{key:n,attrs:{timestamp:e.crawl_time,placement:"top"}},[a("el-card",[a("el-table",{attrs:{data:[e],border:""}},[a("el-table-column",{attrs:{label:"Message"},scopedSlots:t._u([{key:"default",fn:function(n){var r=n.row;return[a("div",[a("span",{staticClass:"message-title",staticStyle:{"padding-right":"10px"}},[t._v("Method:")]),t._v(" "),a("el-tag",{attrs:{type:"success"}},[t._v("\n                "+t._s(r.method)+"\n              ")])],1),t._v(" "),a("br"),t._v(" "),a("div",[a("span",{staticClass:"message-title",staticStyle:{"padding-right":"10px"}},[t._v("Http Code: ")]),t._v(" "),a("el-tag",{attrs:{type:"danger"}},[t._v("\n                "+t._s(r.status)+"\n              ")])],1),t._v(" "),a("br"),t._v(" "),a("div",[a("span",{staticClass:"message-title",staticStyle:{"padding-right":"16px"}},[t._v("Url: ")]),t._v(" "),a("el-tag",{key:e.url_sign},[a("a",{attrs:{href:e.url}},[t._v("\n                  "+t._s(e.url)+"\n                ")])])],1),t._v(" "),a("br"),t._v(" "),a("div",[a("span",{staticClass:"message-title",staticStyle:{"padding-right":"16px"}},[t._v("Sign: ")]),t._v(" "),a("el-tag",{key:e.sign,attrs:{type:"info"},on:{click:function(a){return t.showCrawlDetailHandler(e.sign)}}},[a("a",[t._v(t._s(e.sign))])])],1)]}}],null,!0)}),t._v(" "),a("el-table-column",{attrs:{label:"Stack"},scopedSlots:t._u([{key:"default",fn:function(e){return[a("p",{domProps:{innerHTML:t._s(e.row.exception)}})]}}],null,!0)})],1)],1)],1)})),1)},b=[],g=a("121a"),w={name:"DownloadStatus",props:{statusType:{type:String,default:"downloader"},projectId:{type:String,default:"0"}},data:function(){return{timeLineData:{}}},created:function(){this.fetchProjectInfoChart()},methods:{fetchProjectInfoChart:function(){var t=this;"downloader"===this.statusType?Object(g["a"])(this.projectId).then((function(e){t.timeLineData=e.data})).catch((function(t){console.log(t)})):Object(g["b"])(this.projectId).then((function(e){t.timeLineData=e.data})).catch((function(t){console.log(t)}))},showCrawlDetailHandler:function(t){this.$router.push({path:"/tools/crawl-detail",query:{crawlQuery:{tag:"sign",data:t,source:this.statusType}}})}}},y=w,C=Object(v["a"])(y,j,b,!1,null,null,null),I=C.exports,E={name:"Detail",components:{ProjectStatusChart:m,ProjectException:I},filters:{statusFilter:function(t){var e={1:"success",0:"danger"};return e[t]},statusName:function(t){var e={1:"Open",0:"Closed"};return e[t]}},data:function(){return{timer:{getProjectQueueInfo:void 0},projectId:void 0,projectBaseInfo:{},loading:!1,tempRoute:{},projectQueueInfo:{candidate:{total:[0,0]},download:{total:[0,0]},parse:{total:[0,0]}},activeName:"Downloader Status"}},created:function(){this.projectId=this.$route.params&&this.$route.params.id,this.fetchProjectInfo(),this.getProjectQueueInfo()},mounted:function(){this.timer.getProjectQueueInfo=setInterval(this.getProjectQueueInfo,5e3)},beforeDestroy:function(){for(var t in this.timer)clearInterval(this.timer[t])},methods:{fetchProjectInfo:function(){var t=this;Object(s["c"])(this.projectId).then((function(e){t.projectBaseInfo=e.data})).catch((function(t){console.log(t)}))},updateProjectHandler:function(t){this.$router.push({path:"/project/edit/"+t})},purgeRequestHandler:function(){var t=this;this.$confirm("This action will permanently purge all candidate Request ","Alert",{confirmButtonText:"ok",cancelButtonText:"cancel",type:"warning"}).then((function(){c(t.projectId).then((function(e){0===e.errno&&t.$message({message:"purge all candidate Request success!",type:"success"})})).catch((function(t){console.log(t)}))})).catch((function(){t.$message({type:"info",message:"Cancel purge code"})}))},getProjectQueueInfo:function(){var t=this;i(this.projectId).then((function(e){t.projectQueueInfo=e.data})).catch((function(t){console.log(t)}))}}},x=E,O=(a("891b"),Object(v["a"])(x,n,r,!1,null,"45c65e78",null));e["default"]=O.exports},c638:function(t,e,a){"use strict";a.d(e,"c",(function(){return r})),a.d(e,"e",(function(){return s})),a.d(e,"b",(function(){return o})),a.d(e,"d",(function(){return i})),a.d(e,"a",(function(){return c}));var n=a("b775");function r(t){return Object(n["a"])({url:"chart/downloader/"+t,method:"GET"})}function s(t){return Object(n["a"])({url:"chart/parser/"+t,method:"GET"})}function o(){return Object(n["a"])({url:"chart/downloader",method:"GET"})}function i(t){return Object(n["a"])({url:"chart/node-detail/"+t,method:"GET"})}function c(){return Object(n["a"])({url:"chart/code-type-detail",method:"GET"})}},f42c:function(t,e,a){"use strict";var n=a("ed08");e["a"]={data:function(){return{$_sidebarElm:null}},mounted:function(){var t=this;this.__resizeHandler=Object(n["b"])((function(){t.chart&&t.chart.resize()}),100),window.addEventListener("resize",this.__resizeHandler),this.$_sidebarElm=document.getElementsByClassName("sidebar-container")[0],this.$_sidebarElm&&this.$_sidebarElm.addEventListener("transitionend",this.$_sidebarResizeHandler)},beforeDestroy:function(){window.removeEventListener("resize",this.__resizeHandler),this.$_sidebarElm&&this.$_sidebarElm.removeEventListener("transitionend",this.$_sidebarResizeHandler)},methods:{$_sidebarResizeHandler:function(t){"width"===t.propertyName&&this.__resizeHandler()}}}}}]);