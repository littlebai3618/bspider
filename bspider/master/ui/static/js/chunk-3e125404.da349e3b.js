(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-3e125404"],{"121a":function(t,e,o){"use strict";o.d(e,"e",function(){return r}),o.d(e,"d",function(){return i}),o.d(e,"h",function(){return a}),o.d(e,"b",function(){return s}),o.d(e,"a",function(){return c}),o.d(e,"f",function(){return u}),o.d(e,"g",function(){return l}),o.d(e,"c",function(){return d});var n=o("b775");function r(){return Object(n["a"])({url:"/tools/node-list",method:"GET"})}function i(t){return Object(n["a"])({url:"/tools/code-list",method:"GET",params:t})}function a(t){return Object(n["a"])({url:"/tools/validate/crontab",method:"GET",params:t})}function s(t){return Object(n["a"])({url:"/tools/parser/exception/"+t,method:"GET"})}function c(t){return Object(n["a"])({url:"/tools/downloader/exception/"+t,method:"GET"})}function u(t){return Object(n["a"])({url:"/tools/crawl-detail",method:"GET",params:t})}function l(){return Object(n["a"])({url:"/tools/node-detail",method:"GET"})}function d(){return Object(n["a"])({url:"/tools/exception-project",method:"GET"})}},"1bbd":function(t,e,o){},"3c1b":function(t,e,o){"use strict";var n=function(){var t=this,e=t.$createElement,o=t._self._c||e;return o("div",{staticClass:"createPost-container"},[o("el-form",{ref:"postForm",staticClass:"form-container",attrs:{model:t.postForm,rules:t.rules}},[o("sticky",{attrs:{"z-index":10,"class-name":"sub-navbar "+t.stickyStatus}},[o("el-button",{directives:[{name:"loading",rawName:"v-loading",value:t.loading,expression:"loading"}],staticStyle:{"margin-left":"10px"},attrs:{type:"success"},on:{click:t.submitForm}},[t._v("\n        submit\n      ")])],1),t._v(" "),o("div",{staticClass:"createPost-main-container"},[o("el-row",[o("el-col",{attrs:{span:24}},[o("div",{staticClass:"postInfo-container"},[o("el-row",[o("el-col",{attrs:{span:8}},[o("el-form-item",{staticClass:"postInfo-container-item",attrs:{"label-width":"75px",label:"Project:"}},[o("el-input",{attrs:{readonly:""},model:{value:t.projectName,callback:function(e){t.projectName=e},expression:"projectName"}})],1)],1),t._v(" "),o("el-col",{attrs:{span:8}},[o("el-form-item",{staticClass:"postInfo-container-item",attrs:{"label-width":"75px",label:"Crontab:",prop:"trigger"}},[o("el-input",{model:{value:t.postForm.trigger,callback:function(e){t.$set(t.postForm,"trigger",e)},expression:"postForm.trigger"}})],1)],1),t._v(" "),o("el-col",{attrs:{span:8}},[o("el-form-item",{staticClass:"postInfo-container-item",attrs:{"label-width":"120px",label:"Script Name:",prop:"code_id"}},[o("el-select",{staticClass:"filter-item",attrs:{placeholder:"Please select",filterable:""},on:{change:t.getCodeContent},model:{value:t.postForm.code_id,callback:function(e){t.$set(t.postForm,"code_id",e)},expression:"postForm.code_id"}},t._l(t.codeOptions,function(t){return o("el-option",{key:t.name,attrs:{label:t.name,value:t.id}})}),1)],1)],1)],1)],1)])],1),t._v(" "),o("el-form-item",{staticStyle:{"margin-bottom":"40px"},attrs:{prop:"description","label-width":"90px",label:"Description:"}},[o("el-input",{staticClass:"article-textarea",attrs:{rows:1,type:"textarea",autosize:"",placeholder:"Please enter the description"},model:{value:t.postForm.description,callback:function(e){t.$set(t.postForm,"description",e)},expression:"postForm.description"}}),t._v(" "),o("span",{directives:[{name:"show",rawName:"v-show",value:t.contentShortLength,expression:"contentShortLength"}],staticClass:"word-counter"},[t._v(t._s(t.contentShortLength)+"words")])],1),t._v(" "),o("el-alert",{attrs:{center:!0,title:t.alertText,type:"info","show-icon":""},nativeOn:{click:function(e){return t.jumpToCodeEditorHandler()}}}),t._v(" "),o("el-form-item",{staticStyle:{"margin-bottom":"30px"}},[o("python-editor",{ref:"editor",attrs:{readonly:!0,height:t.pythonEditorHigh,width:"100%"}})],1)],1)],1)],1)},r=[],i=o("73ae"),a=o("121a"),s=o("47d5"),c=o("7dc9"),u=o("b804"),l={project_id:0,code_id:void 0,type:"crawl",trigger:void 0,description:""},d={name:"ProjectCronForm",components:{Sticky:u["a"],PythonEditor:c["a"]},props:{isEdit:{type:Boolean,default:!1}},data:function(){var t=function(t,e,o){Object(a["h"])({data:e}).then(function(t){t.data.valid?o():o(new Error("Invalid crontab"))})};return{cronId:void 0,stickyStatus:"draft",codeOptions:[],postForm:Object.assign({},l),loading:!1,rules:{trigger:[{required:!0,message:"Please select this worker type",trigger:"blur"},{validator:t,trigger:"blur"}],code_id:[{required:!0,message:"Please select script",trigger:"change"}],description:[{required:!0,message:"Please input operation's description",trigger:"blur"},{min:1,max:70,message:"1 to 70 characters in length",trigger:"blur"}]},alertText:"Select script to Preview it",tempRoute:{},projectName:void 0,pythonEditorHigh:"600px"}},computed:{contentShortLength:function(){return this.postForm.description.length}},created:function(){if(this.pythonEditorHigh=window.innerHeight-360+"px",this.projectName=this.$route.query&&this.$route.query.project_name,console.log(this.$route.query.project_id),this.isEdit){var t=this.$route.params&&this.$route.params.id;this.fetchData(t)}else this.postForm.project_id=this.$route.query&&this.$route.query.project_id;this.getCodeOptions(),this.tempRoute=Object.assign({},this.$route)},methods:{fetchData:function(t){var e=this;Object(i["c"])(t).then(function(o){e.cronId=t,e.postForm=o.data,e.isEdit&&e.getCodeContent(e.postForm.code_id),e.setTagsViewTitle(),e.setPageTitle()}).catch(function(t){console.log(t)})},getCodeOptions:function(){var t=this;Object(a["d"])({type:"task"}).then(function(e){t.codeOptions=e.data})},setTagsViewTitle:function(){var t="Edit Project Cron",e=Object.assign({},this.tempRoute,{title:"".concat(t," ").concat(this.postForm.project_id,"-").concat(this.postForm.code_id)});this.$store.dispatch("tagsView/updateVisitedView",e)},setPageTitle:function(){var t="Edit Project Cron";document.title="".concat(t," ").concat(this.postForm.project_id,"-").concat(this.postForm.code_id)},getCodeContent:function(t){var e=this;Object(s["c"])(t).then(function(t){e.$refs.editor.setContent(t.data.content),e.alertText="Executable Code Preview Click to edit this code"}).catch(function(t){console.log(t)})},jumpToCodeEditorHandler:function(){if(this.postForm.class_name){var t=this.getCodeIdByCodeOptions(this.postForm.class_name);this.$router.push({path:"/code/edit/"+t})}else this.$notify({title:"warning",message:"Please select script name",type:"warning",duration:2e3})},submitForm:function(){this.isEdit?this.update():this.create()},update:function(){var t=this;this.$refs.postForm.validate(function(e){e&&Object(i["e"])(t.postForm,t.cronId).then(function(e){t.loading=!0,0===e.errno&&(t.stickyStatus="published",t.$message({message:e.msg,type:"success"})),t.loading=!1}).catch(function(t){console.log(t)})})},create:function(){var t=this;this.$refs.postForm.validate(function(e){e&&Object(i["a"])(t.postForm).then(function(e){t.loading=!0,0===e.errno&&(t.stickyStatus="published",t.$message({message:e.msg,type:"success"})),t.loading=!1}).catch(function(t){console.log(t)})})}}},p=d,m=(o("946f"),o("2877")),h=Object(m["a"])(p,n,r,!1,null,"68b74280",null);e["a"]=h.exports},"47d5":function(t,e,o){"use strict";o.d(e,"d",function(){return r}),o.d(e,"c",function(){return i}),o.d(e,"a",function(){return a}),o.d(e,"e",function(){return s}),o.d(e,"b",function(){return c});o("386d");var n=o("b775");function r(t){return Object(n["a"])({url:"/code",method:"GET",params:{page:t.page,limit:t.limit,search:t.search}})}function i(t){return Object(n["a"])({url:"/code/"+t,method:"GET"})}function a(t){return Object(n["a"])({url:"/code",method:"POST",data:t})}function s(t,e){return Object(n["a"])({url:"/code/"+e,method:"PATCH",data:t})}function c(t){return Object(n["a"])({url:"/code/"+t,method:"DELETE"})}},"73ae":function(t,e,o){"use strict";o.d(e,"d",function(){return r}),o.d(e,"c",function(){return i}),o.d(e,"a",function(){return a}),o.d(e,"e",function(){return s}),o.d(e,"b",function(){return c});o("386d");var n=o("b775");function r(t){return Object(n["a"])({url:"/cron",method:"GET",params:{page:t.page,limit:t.limit,search:t.search}})}function i(t){return Object(n["a"])({url:"/cron/"+t,method:"GET"})}function a(t){return Object(n["a"])({url:"/cron",method:"POST",data:t})}function s(t,e){return Object(n["a"])({url:"/cron/"+e,method:"PATCH",data:t})}function c(t){return Object(n["a"])({url:"/cron/"+t,method:"DELETE"})}},"946f":function(t,e,o){"use strict";var n=o("1bbd"),r=o.n(n);r.a},a026:function(t,e,o){"use strict";o.r(e);var n=function(){var t=this,e=t.$createElement,o=t._self._c||e;return o("project-cron-form",{attrs:{"is-edit":!0}})},r=[],i=o("3c1b"),a={name:"Edit",components:{ProjectCronForm:i["a"]}},s=a,c=o("2877"),u=Object(c["a"])(s,n,r,!1,null,null,null);e["default"]=u.exports}}]);