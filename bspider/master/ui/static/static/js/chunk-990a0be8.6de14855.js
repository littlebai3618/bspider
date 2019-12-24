(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-990a0be8"],{"05ce":function(t,e,o){"use strict";var s=o("9c00"),r=o.n(s);r.a},"0fc6":function(t,e,o){"use strict";o.r(e);var s=function(){var t=this,e=t.$createElement,o=t._self._c||e;return o("project-form",{attrs:{"is-edit":!1}})},r=[],n=o("3d63"),a={name:"Create",components:{ProjectForm:n["a"]}},i=a,c=o("2877"),l=Object(c["a"])(i,s,r,!1,null,null,null);e["default"]=l.exports},"24d2":function(t,e,o){"use strict";o.d(e,"d",function(){return r}),o.d(e,"c",function(){return n}),o.d(e,"a",function(){return a}),o.d(e,"e",function(){return i}),o.d(e,"b",function(){return c});o("386d");var s=o("b775");function r(t){return Object(s["a"])({url:"/project",method:"GET",params:{page:t.page,limit:t.limit,search:t.search}})}function n(t){return Object(s["a"])({url:"/project/"+t,method:"GET"})}function a(t){return Object(s["a"])({url:"/project",method:"POST",data:t})}function i(t,e){return Object(s["a"])({url:"/project/"+e,method:"PATCH",data:t})}function c(t){return Object(s["a"])({url:"/project/"+t,method:"DELETE"})}},"3d63":function(t,e,o){"use strict";var s=function(){var t=this,e=t.$createElement,o=t._self._c||e;return o("div",{staticClass:"createPost-container"},[o("el-form",{ref:"postForm",staticClass:"form-container",attrs:{model:t.postForm,rules:t.rules}},[o("sticky",{attrs:{"z-index":10,"class-name":"sub-navbar "+t.stickyStatus}},[o("status-dropdown",{model:{value:t.postForm.status,callback:function(e){t.$set(t.postForm,"status",e)},expression:"postForm.status"}}),t._v(" "),o("el-button",{directives:[{name:"loading",rawName:"v-loading",value:t.loading,expression:"loading"}],staticStyle:{"margin-left":"10px"},attrs:{type:"success"},on:{click:t.submitForm}},[t._v("\n        submit\n      ")])],1),t._v(" "),o("div",{staticClass:"createPost-main-container"},[o("el-row",[o("el-col",{attrs:{span:24}},[o("el-form-item",{staticStyle:{"margin-bottom":"40px"},attrs:{prop:"name"}},[o("MDinput",{attrs:{maxlength:100,name:"name",readonly:t.isEdit,required:""},model:{value:t.postForm.name,callback:function(e){t.$set(t.postForm,"name",e)},expression:"postForm.name"}},[t._v("\n              Project Name\n            ")])],1),t._v(" "),o("div",{staticClass:"postInfo-container"},[o("el-row",[o("el-col",{attrs:{span:8}},[o("el-form-item",{staticClass:"postInfo-container-item",attrs:{"label-width":"60px",label:"Editor:",prop:"editor"}},[o("el-input",{model:{value:t.postForm.editor,callback:function(e){t.$set(t.postForm,"editor",e)},expression:"postForm.editor"}})],1)],1),t._v(" "),o("el-col",{attrs:{span:8}},[o("el-form-item",{staticClass:"postInfo-container-item",attrs:{"label-width":"120px",label:"Group:",prop:"group"}},[o("el-input",{model:{value:t.postForm.group,callback:function(e){t.$set(t.postForm,"group",e)},expression:"postForm.group"}})],1)],1),t._v(" "),o("el-col",{attrs:{span:8}},[o("el-form-item",{staticClass:"postInfo-container-item",attrs:{"label-width":"120px",label:"Rate:"}},[o("el-input-number",{attrs:{min:1,max:200},model:{value:t.postForm.rate,callback:function(e){t.$set(t.postForm,"rate",e)},expression:"postForm.rate"}})],1)],1)],1)],1)],1)],1),t._v(" "),o("el-form-item",{staticStyle:{"margin-bottom":"40px"},attrs:{prop:"description","label-width":"85px",label:"Description:"}},[o("el-input",{staticClass:"article-textarea",attrs:{rows:1,type:"textarea",autosize:"",placeholder:"Please enter the content"},model:{value:t.postForm.description,callback:function(e){t.$set(t.postForm,"description",e)},expression:"postForm.description"}}),t._v(" "),o("span",{directives:[{name:"show",rawName:"v-show",value:t.contentShortLength,expression:"contentShortLength"}],staticClass:"word-counter"},[t._v(t._s(t.contentShortLength)+"words")])],1),t._v(" "),o("el-form-item",{staticStyle:{"margin-bottom":"30px"}},[o("json-editor",{ref:"editor",model:{value:t.postForm.config,callback:function(e){t.$set(t.postForm,"config",e)},expression:"postForm.config"}})],1)],1)],1)],1)},r=[],n=(o("7f7f"),o("cebc")),a=o("2f62"),i=o("1aba"),c=o("b804"),l=function(){var t=this,e=t.$createElement,o=t._self._c||e;return o("div",{staticClass:"json-editor"},[o("textarea",{ref:"textarea"})])},u=[],p=o("56b3"),m=o.n(p);o("0dd0"),o("a7be"),o("acdf"),o("f9d4"),o("8822"),o("d2de");o("ae67");var d={name:"JsonEditor",props:["value"],data:function(){return{jsonEditor:!1}},watch:{value:function(t){var e=this.jsonEditor.getValue();t!==e&&this.jsonEditor.setValue(JSON.stringify(this.value,null,2))}},mounted:function(){var t=this;this.jsonEditor=m.a.fromTextArea(this.$refs.textarea,{lineNumbers:!0,mode:"application/json",gutters:["CodeMirror-lint-markers"],theme:"rubyblue",lint:!0}),this.jsonEditor.setValue(JSON.stringify(this.value,null,2)),this.jsonEditor.on("change",function(e){t.$emit("changed",e.getValue()),t.$emit("input",e.getValue())})},methods:{getValue:function(){return this.jsonEditor.getValue()}}},f=d,h=(o("a576"),o("2877")),g=Object(h["a"])(f,l,u,!1,null,"032a8708",null),b=g.exports,v=o("24d2"),j=function(){var t=this,e=t.$createElement,o=t._self._c||e;return o("el-dropdown",{attrs:{"show-timeout":100,trigger:"click"}},[o("el-button",{attrs:{plain:""}},[t._v("\n    "+t._s(0===t.project_status?"Status: Off":"Status: On")+"\n    "),o("i",{staticClass:"el-icon-caret-bottom el-icon--right"})]),t._v(" "),o("el-dropdown-menu",{staticClass:"no-padding",attrs:{slot:"dropdown"},slot:"dropdown"},[o("el-dropdown-item",[o("el-radio-group",{staticStyle:{padding:"10px"},model:{value:t.project_status,callback:function(e){t.project_status=e},expression:"project_status"}},[o("el-radio",{attrs:{label:0}},[t._v("\n          Off\n        ")]),t._v(" "),o("el-radio",{attrs:{label:1}},[t._v("\n          On\n        ")])],1)],1)],1)],1)},F=[],x=(o("c5f6"),{props:{value:{type:Number,default:1}},computed:{project_status:{get:function(){return this.value},set:function(t){this.$emit("input",t)}}}}),w=x,_=Object(h["a"])(w,j,F,!1,null,null,null),$=_.exports,E={name:void 0,status:1,group:void 0,description:"",editor:void 0,rate:50,config:{}},O={name:"ProjectForm",components:{StatusDropdown:$,MDinput:i["a"],Sticky:c["a"],JsonEditor:b},props:{isEdit:{type:Boolean,default:!1}},data:function(){return{stickyStatus:"draft",postForm:Object.assign({},E),loading:!1,rules:{name:[{required:!0,message:"Please input ProjectName",trigger:"blur"}],editor:[{required:!0,message:"Please input editor",trigger:"blur"},{min:1,max:20,message:"1 to 20 characters in length",trigger:"blur"}],group:[{required:!0,message:"Please input group",trigger:"blur"}],description:[{required:!0,message:"Please input description",trigger:"blur"}]},tempRoute:{},projectId:void 0}},computed:Object(n["a"])({contentShortLength:function(){return this.postForm.description.length}},Object(a["b"])(["name"])),created:function(){if(this.isEdit){var t=this.$route.params&&this.$route.params.id;this.projectId=t,this.fetchData(t)}else this.initFormData();this.tempRoute=Object.assign({},this.$route)},methods:{fetchData:function(t){var e=this;Object(v["c"])(t).then(function(t){e.postForm=t.data,e.postForm.config=JSON.parse(e.postForm.config),e.setTagsViewTitle(),e.setPageTitle()}).catch(function(t){console.log(t)})},setTagsViewTitle:function(){var t="Edit Project",e=Object.assign({},this.tempRoute,{title:"".concat(t,"-").concat(this.postForm.name)});this.$store.dispatch("tagsView/updateVisitedView",e)},setPageTitle:function(){var t="Edit Project";document.title="".concat(t,"-").concat(this.postForm.name)},initFormData:function(){this.postForm.editor=this.name},submitForm:function(){this.isEdit?this.update():this.create()},update:function(){var t=this;this.postForm.config=this.$refs.editor.getValue(),this.$refs.postForm.validate(function(e){e&&Object(v["e"])(t.postForm,t.projectId).then(function(e){t.loading=!0,0===e.errno&&(t.stickyStatus="published",t.$message({message:e.msg,type:"success"})),t.loading=!1}).catch(function(t){console.log(t)})})},create:function(){var t=this;this.postForm.config=this.$refs.editor.getValue(),this.$refs.postForm.validate(function(e){e&&Object(v["a"])(t.postForm).then(function(e){t.loading=!0,0===e.errno&&(t.stickyStatus="published",t.$message({message:e.msg,type:"success"})),t.loading=!1}).catch(function(e){console.log(e),t.$message({message:e,type:"error"})})})}}},y=O,S=(o("05ce"),Object(h["a"])(y,s,r,!1,null,"504b6e38",null));e["a"]=S.exports},6751:function(t,e,o){},"9c00":function(t,e,o){},a576:function(t,e,o){"use strict";var s=o("6751"),r=o.n(s);r.a}}]);