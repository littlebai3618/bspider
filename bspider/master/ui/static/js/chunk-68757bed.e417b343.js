(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-68757bed"],{"0f66":function(t,e,a){"use strict";a.d(e,"c",function(){return s}),a.d(e,"b",function(){return r}),a.d(e,"e",function(){return i}),a.d(e,"d",function(){return o}),a.d(e,"f",function(){return c}),a.d(e,"a",function(){return l});a("386d");var n=a("b775");function s(t){return Object(n["a"])({url:"/node",method:"GET",params:{page:t.page,limit:t.limit,search:t.search}})}function r(t){return Object(n["a"])({url:"/node/"+t,method:"GET"})}function i(t,e){return Object(n["a"])({url:"/node/"+e,method:"PATCH",data:t})}function o(t){return Object(n["a"])({url:"/worker",method:"GET",params:{page:t.page,limit:t.limit,search:t.search}})}function c(t,e){return Object(n["a"])({url:"/worker/"+e,method:"PATCH",data:t})}function l(t){return Object(n["a"])({url:"/worker",method:"POST",data:t})}},1349:function(t,e,a){"use strict";a.r(e);var n=function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("div",{staticClass:"app-container"},[a("el-row",{attrs:{gutter:10}},[a("el-col",{attrs:{span:5}},[a("el-row",[a("el-card",{staticClass:"detail-wrapper"},[a("div",{staticClass:"clearfix",attrs:{slot:"header"},slot:"header"},[a("span",[t._v("Base Info")])]),t._v(" "),a("div",{staticClass:"text item"},[a("el-row",[a("el-col",{attrs:{span:10}},[a("div",{staticClass:"content-key"},[t._v("ID:")])]),t._v(" "),a("el-col",{attrs:{span:14}},[a("div",{staticClass:"content-value"},[t._v("\n                  "+t._s(t.nodeBaseInfo.id)+"\n                ")])])],1),t._v(" "),a("el-row",[a("el-col",{attrs:{span:10}},[a("div",{staticClass:"content-key"},[t._v("Name:")])]),t._v(" "),a("el-col",{attrs:{span:14}},[a("div",{staticClass:"content-value"},[t._v(t._s(t.nodeBaseInfo.name))])])],1),t._v(" "),a("el-row",[a("el-col",{attrs:{span:10}},[a("div",{staticClass:"content-key"},[t._v("CPU:")])]),t._v(" "),a("el-col",{attrs:{span:14}},[a("div",{staticClass:"content-value"},[t._v(t._s(t.nodeBaseInfo.cpu_num)+" core")])])],1),t._v(" "),a("el-row",[a("el-col",{attrs:{span:10}},[a("div",{staticClass:"content-key"},[t._v("Memory:")])]),t._v(" "),a("el-col",{attrs:{span:14}},[a("div",{staticClass:"content-value"},[t._v(t._s(t.nodeBaseInfo.mem_size)+" G")])])],1),t._v(" "),a("el-row",[a("el-col",{attrs:{span:10}},[a("div",{staticClass:"content-key"},[t._v("Disk:")])]),t._v(" "),a("el-col",{attrs:{span:14}},[a("div",{staticClass:"content-value"},[t._v(t._s(t.nodeBaseInfo.disk_size)+" G")])])],1)],1)])],1),t._v(" "),a("el-row",[a("el-card",{staticClass:"detail-wrapper"},[a("div",{staticClass:"clearfix",attrs:{slot:"header"},slot:"header"},[a("span",[t._v("Agent Info")])]),t._v(" "),a("div",{staticClass:"text item"},[a("el-row",[a("el-col",{attrs:{span:10}},[a("div",{staticClass:"content-key"},[t._v("Pid:")])]),t._v(" "),a("el-col",{attrs:{span:14}},[a("div",{staticClass:"content-value"},[t._v(t._s(t.nodeBaseInfo.pid))])])],1),t._v(" "),a("el-row",[a("el-col",{attrs:{span:10}},[a("div",{staticClass:"content-key"},[t._v("Status:")])]),t._v(" "),a("el-col",{attrs:{span:14}},[a("div",{staticClass:"content-value"},[a("el-tag",{attrs:{type:t._f("statusFilter")(t.nodeBaseInfo.status),size:"mini"}},[t._v("\n                    "+t._s(t._f("statusName")(t.nodeBaseInfo.status))+"\n                  ")])],1)])],1),t._v(" "),a("el-row",[a("el-col",{attrs:{span:10}},[a("div",{staticClass:"content-key"},[t._v("Server:")])]),t._v(" "),a("el-col",{attrs:{span:14}},[a("div",{staticClass:"content-value"},[t._v(t._s(t.nodeBaseInfo.ip+":"+t.nodeBaseInfo.port))])])],1),t._v(" "),a("el-row",[a("el-col",{attrs:{span:10}},[a("div",{staticClass:"content-key"},[t._v("Description:")])]),t._v(" "),a("el-col",{attrs:{span:14}},[a("div",{staticClass:"content-value"},[t._v(t._s(t.nodeBaseInfo.description))])])],1),t._v(" "),a("el-row",[a("el-col",{attrs:{span:10}},[a("div",{staticClass:"content-key"},[t._v("Create:")])]),t._v(" "),a("el-col",{attrs:{span:14}},[a("div",{staticClass:"content-value"},[t._v(t._s(t.nodeBaseInfo.create_time))])])],1),t._v(" "),a("el-row",[a("el-col",{attrs:{span:10}},[a("div",{staticClass:"content-key"},[t._v("Update:")])]),t._v(" "),a("el-col",{attrs:{span:14}},[a("div",{staticClass:"content-value"},[t._v(t._s(t.nodeBaseInfo.update_time))])])],1)],1)])],1)],1),t._v(" "),a("el-col",{attrs:{span:19}},[a("el-tabs",{attrs:{type:"border-card"},model:{value:t.activeName,callback:function(e){t.activeName=e},expression:"activeName"}},[a("el-tab-pane",{attrs:{label:"Node Status(7 days)",name:"Node Status",lazy:!0}},[a("keep-alive",[a("node-status-chart",{attrs:{"node-ip":t.nodeIp}})],1)],1)],1)],1)],1)],1)},s=[],r=a("0f66"),i=function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("two-line-chart",{ref:"lineChart",attrs:{width:"100%",height:"750px"}})},o=[],c=a("c638"),l=a("357a"),d={name:"NodeStatusChart",components:{TwoLineChart:l["a"]},props:{nodeIp:{type:String,default:"0"}},created:function(){this.fetchProjectInfoChart()},methods:{fetchProjectInfoChart:function(){var t=this;Object(c["d"])(this.nodeIp).then(function(e){t.$refs.lineChart.setOptions(e.data)}).catch(function(t){console.log(t)})}}},u=d,v=a("2877"),h=Object(v["a"])(u,i,o,!1,null,"78d8d3b0",null),f=h.exports,p={name:"Detail",components:{NodeStatusChart:f},filters:{statusFilter:function(t){var e={1:"success",0:"danger"};return e[t]},statusName:function(t){var e={1:"Open",0:"Closed"};return e[t]}},data:function(){return{timer:{getProjectQueueInfo:void 0},nodeIp:void 0,nodeId:void 0,nodeBaseInfo:{},loading:!1,tempRoute:{},activeName:"Node Status"}},created:function(){this.nodeId=this.$route.params&&this.$route.params.id,this.nodeIp=this.$route.query&&this.$route.query.ip,this.fetchNodeInfo()},beforeDestroy:function(){for(var t in this.timer)clearInterval(this.timer[t])},methods:{fetchNodeInfo:function(){var t=this;Object(r["b"])(this.nodeId).then(function(e){t.nodeBaseInfo=e.data}).catch(function(t){console.log(t)})}}},_=p,m=(a("7742"),Object(v["a"])(_,n,s,!1,null,"fe390362",null));e["default"]=m.exports},"357a":function(t,e,a){"use strict";var n=function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("div",{class:t.className,style:{height:t.height,width:"100%"}})},s=[],r=a("313e"),i=a.n(r),o=a("f42c");a("817d");var c={name:"TwoLineChart",mixins:[o["a"]],props:{className:{type:String,default:"chart"},width:{type:String,default:"100%"},height:{type:String,default:"350px"},autoResize:{type:Boolean,default:!0}},data:function(){return{chart:null}},mounted:function(){var t=this;this.$nextTick(function(){t.initChart()})},beforeDestroy:function(){this.chart&&(this.chart.dispose(),this.chart=null)},methods:{initChart:function(){this.chart=i.a.init(this.$el,"macarons")},setOptions:function(){var t=arguments.length>0&&void 0!==arguments[0]?arguments[0]:{},e=t.xAxis,a=t.legend,n=t.series;this.chart.setOption({xAxis:{data:e,boundaryGap:!1,axisTick:{show:!1}},grid:{left:10,right:10,bottom:20,top:30,containLabel:!0},tooltip:{trigger:"axis",axisPointer:{type:"cross"},padding:[5,10]},yAxis:{axisTick:{show:!1}},legend:{data:a},series:n})}}},l=c,d=a("2877"),u=Object(d["a"])(l,n,s,!1,null,null,null);e["a"]=u.exports},7742:function(t,e,a){"use strict";var n=a("a8b3"),s=a.n(n);s.a},a8b3:function(t,e,a){},c638:function(t,e,a){"use strict";a.d(e,"c",function(){return s}),a.d(e,"e",function(){return r}),a.d(e,"b",function(){return i}),a.d(e,"d",function(){return o}),a.d(e,"a",function(){return c});var n=a("b775");function s(t){return Object(n["a"])({url:"chart/downloader/"+t,method:"GET"})}function r(t){return Object(n["a"])({url:"chart/parser/"+t,method:"GET"})}function i(){return Object(n["a"])({url:"chart/downloader",method:"GET"})}function o(t){return Object(n["a"])({url:"chart/node-detail/"+t,method:"GET"})}function c(){return Object(n["a"])({url:"chart/code-type-detail",method:"GET"})}},f42c:function(t,e,a){"use strict";var n=a("ed08");e["a"]={data:function(){return{$_sidebarElm:null}},mounted:function(){var t=this;this.__resizeHandler=Object(n["b"])(function(){t.chart&&t.chart.resize()},100),window.addEventListener("resize",this.__resizeHandler),this.$_sidebarElm=document.getElementsByClassName("sidebar-container")[0],this.$_sidebarElm&&this.$_sidebarElm.addEventListener("transitionend",this.$_sidebarResizeHandler)},beforeDestroy:function(){window.removeEventListener("resize",this.__resizeHandler),this.$_sidebarElm&&this.$_sidebarElm.removeEventListener("transitionend",this.$_sidebarResizeHandler)},methods:{$_sidebarResizeHandler:function(t){"width"===t.propertyName&&this.__resizeHandler()}}}}}]);