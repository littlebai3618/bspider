(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-7f0e1e08"],{"121a":function(t,e,i){"use strict";i.d(e,"e",function(){return o}),i.d(e,"d",function(){return r}),i.d(e,"h",function(){return s}),i.d(e,"b",function(){return a}),i.d(e,"a",function(){return c}),i.d(e,"f",function(){return d}),i.d(e,"g",function(){return l}),i.d(e,"c",function(){return u});var n=i("b775");function o(){return Object(n["a"])({url:"/tools/node-list",method:"GET"})}function r(t){return Object(n["a"])({url:"/tools/code-list",method:"GET",params:t})}function s(t){return Object(n["a"])({url:"/tools/validate/crontab",method:"GET",params:t})}function a(t){return Object(n["a"])({url:"/tools/parser/exception/"+t,method:"GET"})}function c(t){return Object(n["a"])({url:"/tools/downloader/exception/"+t,method:"GET"})}function d(t){return Object(n["a"])({url:"/tools/crawl-detail",method:"GET",params:t})}function l(){return Object(n["a"])({url:"/tools/node-detail",method:"GET"})}function u(){return Object(n["a"])({url:"/tools/exception-project",method:"GET"})}},"1bbd":function(t,e,i){},"3c1b":function(t,e,i){"use strict";var n=function(){var t=this,e=t.$createElement,i=t._self._c||e;return i("div",{staticClass:"createPost-container"},[i("el-form",{ref:"postForm",staticClass:"form-container",attrs:{model:t.postForm,rules:t.rules}},[i("sticky",{attrs:{"z-index":10,"class-name":"sub-navbar "+t.stickyStatus}},[i("el-button",{directives:[{name:"loading",rawName:"v-loading",value:t.loading,expression:"loading"}],staticStyle:{"margin-left":"10px"},attrs:{type:"success"},on:{click:t.submitForm}},[t._v("\n        submit\n      ")])],1),t._v(" "),i("div",{staticClass:"createPost-main-container"},[i("el-row",[i("el-col",{attrs:{span:24}},[i("div",{staticClass:"postInfo-container"},[i("el-row",[i("el-col",{attrs:{span:8}},[i("el-form-item",{staticClass:"postInfo-container-item",attrs:{"label-width":"75px",label:"Project:"}},[i("el-input",{attrs:{readonly:""},model:{value:t.projectName,callback:function(e){t.projectName=e},expression:"projectName"}})],1)],1),t._v(" "),i("el-col",{attrs:{span:8}},[i("el-form-item",{staticClass:"postInfo-container-item",attrs:{"label-width":"75px",label:"Crontab:",prop:"trigger"}},[i("el-input",{model:{value:t.postForm.trigger,callback:function(e){t.$set(t.postForm,"trigger",e)},expression:"postForm.trigger"}})],1)],1),t._v(" "),i("el-col",{attrs:{span:8}},[i("el-form-item",{staticClass:"postInfo-container-item",attrs:{"label-width":"120px",label:"Script Name:",prop:"code_id"}},[i("el-select",{staticClass:"filter-item",attrs:{placeholder:"Please select",filterable:""},on:{change:t.getCodeContent},model:{value:t.postForm.code_id,callback:function(e){t.$set(t.postForm,"code_id",e)},expression:"postForm.code_id"}},t._l(t.codeOptions,function(t){return i("el-option",{key:t.name,attrs:{label:t.name,value:t.id}})}),1)],1)],1)],1)],1)])],1),t._v(" "),i("el-form-item",{staticStyle:{"margin-bottom":"40px"},attrs:{prop:"description","label-width":"90px",label:"Description:"}},[i("el-input",{staticClass:"article-textarea",attrs:{rows:1,type:"textarea",autosize:"",placeholder:"Please enter the description"},model:{value:t.postForm.description,callback:function(e){t.$set(t.postForm,"description",e)},expression:"postForm.description"}}),t._v(" "),i("span",{directives:[{name:"show",rawName:"v-show",value:t.contentShortLength,expression:"contentShortLength"}],staticClass:"word-counter"},[t._v(t._s(t.contentShortLength)+"words")])],1),t._v(" "),i("el-alert",{attrs:{center:!0,title:t.alertText,type:"info","show-icon":""},nativeOn:{click:function(e){return t.jumpToCodeEditorHandler()}}}),t._v(" "),i("el-form-item",{staticStyle:{"margin-bottom":"30px"}},[i("python-editor",{ref:"editor",attrs:{readonly:!0,height:t.pythonEditorHigh,width:"100%"}})],1)],1)],1)],1)},o=[],r=i("73ae"),s=i("121a"),a=i("47d5"),c=i("7dc9"),d=i("b804"),l={project_id:0,code_id:void 0,type:"crawl",trigger:void 0,description:""},u={name:"ProjectCronForm",components:{Sticky:d["a"],PythonEditor:c["a"]},props:{isEdit:{type:Boolean,default:!1}},data:function(){var t=function(t,e,i){Object(s["h"])({data:e}).then(function(t){t.data.valid?i():i(new Error("Invalid crontab"))})};return{cronId:void 0,stickyStatus:"draft",codeOptions:[],postForm:Object.assign({},l),loading:!1,rules:{trigger:[{required:!0,message:"Please select this worker type",trigger:"blur"},{validator:t,trigger:"blur"}],code_id:[{required:!0,message:"Please select script",trigger:"change"}],description:[{required:!0,message:"Please input operation's description",trigger:"blur"},{min:1,max:70,message:"1 to 70 characters in length",trigger:"blur"}]},alertText:"Select script to Preview it",tempRoute:{},projectName:void 0,pythonEditorHigh:"600px"}},computed:{contentShortLength:function(){return this.postForm.description.length}},created:function(){if(this.pythonEditorHigh=window.innerHeight-360+"px",this.projectName=this.$route.query&&this.$route.query.project_name,console.log(this.$route.query.project_id),this.isEdit){var t=this.$route.params&&this.$route.params.id;this.fetchData(t)}else this.postForm.project_id=this.$route.query&&this.$route.query.project_id;this.getCodeOptions(),this.tempRoute=Object.assign({},this.$route)},methods:{fetchData:function(t){var e=this;Object(r["c"])(t).then(function(i){e.cronId=t,e.postForm=i.data,e.isEdit&&e.getCodeContent(e.postForm.code_id),e.setTagsViewTitle(),e.setPageTitle()}).catch(function(t){console.log(t)})},getCodeOptions:function(){var t=this;Object(s["d"])({type:"task"}).then(function(e){t.codeOptions=e.data})},setTagsViewTitle:function(){var t="Edit Project Cron",e=Object.assign({},this.tempRoute,{title:"".concat(t," ").concat(this.postForm.project_id,"-").concat(this.postForm.code_id)});this.$store.dispatch("tagsView/updateVisitedView",e)},setPageTitle:function(){var t="Edit Project Cron";document.title="".concat(t," ").concat(this.postForm.project_id,"-").concat(this.postForm.code_id)},getCodeContent:function(t){var e=this;Object(a["c"])(t).then(function(t){e.$refs.editor.setContent(t.data.content),e.alertText="Executable Code Preview Click to edit this code"}).catch(function(t){console.log(t)})},jumpToCodeEditorHandler:function(){if(this.postForm.class_name){var t=this.getCodeIdByCodeOptions(this.postForm.class_name);this.$router.push({path:"/code/edit/"+t})}else this.$notify({title:"warning",message:"Please select script name",type:"warning",duration:2e3})},submitForm:function(){this.isEdit?this.update():this.create()},update:function(){var t=this;this.$refs.postForm.validate(function(e){e&&Object(r["e"])(t.postForm,t.cronId).then(function(e){t.loading=!0,0===e.errno&&(t.stickyStatus="published",t.$message({message:e.msg,type:"success"})),t.loading=!1}).catch(function(t){console.log(t)})})},create:function(){var t=this;this.$refs.postForm.validate(function(e){e&&Object(r["a"])(t.postForm).then(function(e){t.loading=!0,0===e.errno&&(t.stickyStatus="published",t.$message({message:e.msg,type:"success"})),t.loading=!1}).catch(function(t){console.log(t)})})}}},h=u,p=(i("946f"),i("2877")),m=Object(p["a"])(h,n,o,!1,null,"68b74280",null);e["a"]=m.exports},"47d5":function(t,e,i){"use strict";i.d(e,"d",function(){return o}),i.d(e,"c",function(){return r}),i.d(e,"a",function(){return s}),i.d(e,"e",function(){return a}),i.d(e,"b",function(){return c});i("386d");var n=i("b775");function o(t){return Object(n["a"])({url:"/code",method:"GET",params:{page:t.page,limit:t.limit,search:t.search}})}function r(t){return Object(n["a"])({url:"/code/"+t,method:"GET"})}function s(t){return Object(n["a"])({url:"/code",method:"POST",data:t})}function a(t,e){return Object(n["a"])({url:"/code/"+e,method:"PATCH",data:t})}function c(t){return Object(n["a"])({url:"/code/"+t,method:"DELETE"})}},"48b1":function(t,e,i){"use strict";i.r(e);var n=function(){var t=this,e=t.$createElement,i=t._self._c||e;return i("project-cron-form",{attrs:{"is-edit":!1}})},o=[],r=i("3c1b"),s={name:"Create",components:{ProjectCronForm:r["a"]}},a=s,c=i("2877"),d=Object(c["a"])(a,n,o,!1,null,null,null);e["default"]=d.exports},"73ae":function(t,e,i){"use strict";i.d(e,"d",function(){return o}),i.d(e,"c",function(){return r}),i.d(e,"a",function(){return s}),i.d(e,"e",function(){return a}),i.d(e,"b",function(){return c});i("386d");var n=i("b775");function o(t){return Object(n["a"])({url:"/cron",method:"GET",params:{page:t.page,limit:t.limit,search:t.search}})}function r(t){return Object(n["a"])({url:"/cron/"+t,method:"GET"})}function s(t){return Object(n["a"])({url:"/cron",method:"POST",data:t})}function a(t,e){return Object(n["a"])({url:"/cron/"+e,method:"PATCH",data:t})}function c(t){return Object(n["a"])({url:"/cron/"+t,method:"DELETE"})}},"7dc9":function(t,e,i){"use strict";var n=function(){var t=this,e=t.$createElement,i=t._self._c||e;return i("div",{staticClass:"python-editor"},[i("textarea",{ref:"textarea"})])},o=[],r=i("56b3"),s=i.n(r);i("a7be"),i("7a7a"),i("697eb"),i("f6b6");i("db91"),i("31c5"),i("cbc8"),i("4895"),i("8c33"),i("9b74"),i("10b2");var a={name:"PythonEditor",props:{readonly:Boolean,hidden:Boolean,height:String,width:String},mounted:function(){this.initCodeMirror()},watch:{value:function(t){var e=this.editor.getValue();t!==e&&this.yamlEditor.setValue(this.value)}},methods:{initCodeMirror:function(){var t=this;this.editor=s.a.fromTextArea(this.$refs.textarea,{mode:"text/x-python",lineNumbers:!0,theme:"monokai",indentWithTabs:!0,smartIndent:!0,indentUnit:4,lineWrapping:!0,gutters:["CodeMirror-linenumbers","CodeMirror-foldgutter","CodeMirror-lint-markers"],foldGutter:!0,autofocus:!0,matchBrackets:!0,autoCloseBrackets:!0,styleActiveLine:!0}),this.readonly&&this.editor.setOption("readOnly",!0),this.hidden&&this.editor.setOption("hidden",!0),this.editor.setValue(this.value),this.editor.on("change",function(e){t.$emit("changed",e.getValue()),t.$emit("input",e.getValue())})},getContent:function(){return this.editor.getValue()},setContent:function(t){this.editor.setValue(t)},setOption:function(t,e){this.editor.setOption(t,e)}}},c=a,d=(i("f3fc"),i("2877")),l=Object(d["a"])(c,n,o,!1,null,"b12d22d2",null);e["a"]=l.exports},"86aa":function(t,e,i){},"946f":function(t,e,i){"use strict";var n=i("1bbd"),o=i.n(n);o.a},b804:function(t,e,i){"use strict";var n=function(){var t=this,e=t.$createElement,i=t._self._c||e;return i("div",{style:{height:t.height+"px",zIndex:t.zIndex}},[i("div",{class:t.className,style:{top:t.isSticky?t.stickyTop+"px":"",zIndex:t.zIndex,position:t.position,width:t.width,height:t.height+"px"}},[t._t("default",[i("div",[t._v("sticky")])])],2)])},o=[],r=(i("c5f6"),{name:"Sticky",props:{stickyTop:{type:Number,default:0},zIndex:{type:Number,default:1},className:{type:String,default:""}},data:function(){return{active:!1,position:"",width:void 0,height:void 0,isSticky:!1}},mounted:function(){this.height=this.$el.getBoundingClientRect().height,window.addEventListener("scroll",this.handleScroll),window.addEventListener("resize",this.handleResize)},activated:function(){this.handleScroll()},destroyed:function(){window.removeEventListener("scroll",this.handleScroll),window.removeEventListener("resize",this.handleResize)},methods:{sticky:function(){this.active||(this.position="fixed",this.active=!0,this.width=this.width+"px",this.isSticky=!0)},handleReset:function(){this.active&&this.reset()},reset:function(){this.position="",this.width="auto",this.active=!1,this.isSticky=!1},handleScroll:function(){var t=this.$el.getBoundingClientRect().width;this.width=t||"auto";var e=this.$el.getBoundingClientRect().top;e<this.stickyTop?this.sticky():this.handleReset()},handleResize:function(){this.isSticky&&(this.width=this.$el.getBoundingClientRect().width+"px")}}}),s=r,a=i("2877"),c=Object(a["a"])(s,n,o,!1,null,null,null);e["a"]=c.exports},f3fc:function(t,e,i){"use strict";var n=i("86aa"),o=i.n(n);o.a}}]);