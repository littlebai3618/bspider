(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-349b9bc2"],{"10b2":function(t,e,n){(function(t){t(n("56b3"))})(function(t){var e={pairs:"()[]{}''\"\"",closeBefore:")]}'\":;>",triples:"",explode:"[]{}"},n=t.Pos;function i(t,n){return"pairs"==n&&"string"==typeof t?t:"object"==typeof t&&null!=t[n]?t[n]:e[n]}t.defineOption("autoCloseBrackets",!1,function(e,n,s){s&&s!=t.Init&&(e.removeKeyMap(o),e.state.closeBrackets=null),n&&(r(i(n,"pairs")),e.state.closeBrackets=n,e.addKeyMap(o))});var o={Backspace:c,Enter:l};function r(t){for(var e=0;e<t.length;e++){var n=t.charAt(e),i="'"+n+"'";o[i]||(o[i]=s(n))}}function s(t){return function(e){return u(e,t)}}function a(t){var e=t.state.closeBrackets;if(!e||e.override)return e;var n=t.getModeAt(t.getCursor());return n.closeBrackets||e}function c(e){var o=a(e);if(!o||e.getOption("disableInput"))return t.Pass;for(var r=i(o,"pairs"),s=e.listSelections(),c=0;c<s.length;c++){if(!s[c].empty())return t.Pass;var l=h(e,s[c].head);if(!l||r.indexOf(l)%2!=0)return t.Pass}for(c=s.length-1;c>=0;c--){var f=s[c].head;e.replaceRange("",n(f.line,f.ch-1),n(f.line,f.ch+1),"+delete")}}function l(e){var n=a(e),o=n&&i(n,"explode");if(!o||e.getOption("disableInput"))return t.Pass;for(var r=e.listSelections(),s=0;s<r.length;s++){if(!r[s].empty())return t.Pass;var c=h(e,r[s].head);if(!c||o.indexOf(c)%2!=0)return t.Pass}e.operation(function(){var t=e.lineSeparator()||"\n";e.replaceSelection(t+t,null),e.execCommand("goCharLeft"),r=e.listSelections();for(var n=0;n<r.length;n++){var i=r[n].head.line;e.indentLine(i,null,!0),e.indentLine(i+1,null,!0)}})}function f(e){var i=t.cmpPos(e.anchor,e.head)>0;return{anchor:new n(e.anchor.line,e.anchor.ch+(i?-1:1)),head:new n(e.head.line,e.head.ch+(i?1:-1))}}function u(e,o){var r=a(e);if(!r||e.getOption("disableInput"))return t.Pass;var s=i(r,"pairs"),c=s.indexOf(o);if(-1==c)return t.Pass;for(var l,u=i(r,"closeBefore"),h=i(r,"triples"),p=s.charAt(c+1)==o,g=e.listSelections(),m=c%2==0,v=0;v<g.length;v++){var y,b=g[v],k=b.head,w=e.getRange(k,n(k.line,k.ch+1));if(m&&!b.empty())y="surround";else if(!p&&m||w!=o)if(p&&k.ch>1&&h.indexOf(o)>=0&&e.getRange(n(k.line,k.ch-2),k)==o+o){if(k.ch>2&&/\bstring/.test(e.getTokenTypeAt(n(k.line,k.ch-2))))return t.Pass;y="addFour"}else if(p){var x=0==k.ch?" ":e.getRange(n(k.line,k.ch-1),k);if(t.isWordChar(w)||x==o||t.isWordChar(x))return t.Pass;y="both"}else{if(!m||!(0===w.length||/\s/.test(w)||u.indexOf(w)>-1))return t.Pass;y="both"}else y=p&&d(e,k)?"both":h.indexOf(o)>=0&&e.getRange(k,n(k.line,k.ch+3))==o+o+o?"skipThree":"skip";if(l){if(l!=y)return t.Pass}else l=y}var C=c%2?s.charAt(c-1):o,A=c%2?o:s.charAt(c+1);e.operation(function(){if("skip"==l)e.execCommand("goCharRight");else if("skipThree"==l)for(var t=0;t<3;t++)e.execCommand("goCharRight");else if("surround"==l){var n=e.getSelections();for(t=0;t<n.length;t++)n[t]=C+n[t]+A;e.replaceSelections(n,"around"),n=e.listSelections().slice();for(t=0;t<n.length;t++)n[t]=f(n[t]);e.setSelections(n)}else"both"==l?(e.replaceSelection(C+A,null),e.triggerElectric(C+A),e.execCommand("goCharLeft")):"addFour"==l&&(e.replaceSelection(C+C+C+C,"before"),e.execCommand("goCharRight"))})}function h(t,e){var i=t.getRange(n(e.line,e.ch-1),n(e.line,e.ch+1));return 2==i.length?i:null}function d(t,e){var i=t.getTokenAt(n(e.line,e.ch+1));return/\bstring/.test(i.type)&&i.start==e.ch&&(0==e.ch||!/\bstring/.test(t.getTokenTypeAt(e)))}r(e.pairs+"`")})},"31c5":function(t,e,n){(function(t){t(n("56b3"))})(function(t){"use strict";var e="CodeMirror-activeline",n="CodeMirror-activeline-background",i="CodeMirror-activeline-gutter";function o(t){for(var o=0;o<t.state.activeLines.length;o++)t.removeLineClass(t.state.activeLines[o],"wrap",e),t.removeLineClass(t.state.activeLines[o],"background",n),t.removeLineClass(t.state.activeLines[o],"gutter",i)}function r(t,e){if(t.length!=e.length)return!1;for(var n=0;n<t.length;n++)if(t[n]!=e[n])return!1;return!0}function s(t,s){for(var a=[],c=0;c<s.length;c++){var l=s[c],f=t.getOption("styleActiveLine");if("object"==typeof f&&f.nonEmpty?l.anchor.line==l.head.line:l.empty()){var u=t.getLineHandleVisualStart(l.head.line);a[a.length-1]!=u&&a.push(u)}}r(t.state.activeLines,a)||t.operation(function(){o(t);for(var r=0;r<a.length;r++)t.addLineClass(a[r],"wrap",e),t.addLineClass(a[r],"background",n),t.addLineClass(a[r],"gutter",i);t.state.activeLines=a})}function a(t,e){s(t,e.ranges)}t.defineOption("styleActiveLine",!1,function(e,n,i){var r=i!=t.Init&&i;n!=r&&(r&&(e.off("beforeSelectionChange",a),o(e),delete e.state.activeLines),n&&(e.state.activeLines=[],s(e,e.listSelections()),e.on("beforeSelectionChange",a)))})})},4895:function(t,e,n){(function(t){t(n("56b3"))})(function(t){"use strict";function e(e,i,r,s){if(r&&r.call){var a=r;r=null}else a=o(e,r,"rangeFinder");"number"==typeof i&&(i=t.Pos(i,0));var c=o(e,r,"minFoldSize");function l(t){var n=a(e,i);if(!n||n.to.line-n.from.line<c)return null;for(var o=e.findMarksAt(n.from),r=0;r<o.length;++r)if(o[r].__isFold&&"fold"!==s){if(!t)return null;n.cleared=!0,o[r].clear()}return n}var f=l(!0);if(o(e,r,"scanUp"))while(!f&&i.line>e.firstLine())i=t.Pos(i.line-1,0),f=l(!1);if(f&&!f.cleared&&"unfold"!==s){var u=n(e,r);t.on(u,"mousedown",function(e){h.clear(),t.e_preventDefault(e)});var h=e.markText(f.from,f.to,{replacedWith:u,clearOnEnter:o(e,r,"clearOnEnter"),__isFold:!0});h.on("clear",function(n,i){t.signal(e,"unfold",e,n,i)}),t.signal(e,"fold",e,f.from,f.to)}}function n(t,e){var n=o(t,e,"widget");if("string"==typeof n){var i=document.createTextNode(n);n=document.createElement("span"),n.appendChild(i),n.className="CodeMirror-foldmarker"}else n&&(n=n.cloneNode(!0));return n}t.newFoldFunction=function(t,n){return function(i,o){e(i,o,{rangeFinder:t,widget:n})}},t.defineExtension("foldCode",function(t,n,i){e(this,t,n,i)}),t.defineExtension("isFolded",function(t){for(var e=this.findMarksAt(t),n=0;n<e.length;++n)if(e[n].__isFold)return!0}),t.commands.toggleFold=function(t){t.foldCode(t.getCursor())},t.commands.fold=function(t){t.foldCode(t.getCursor(),null,"fold")},t.commands.unfold=function(t){t.foldCode(t.getCursor(),null,"unfold")},t.commands.foldAll=function(e){e.operation(function(){for(var n=e.firstLine(),i=e.lastLine();n<=i;n++)e.foldCode(t.Pos(n,0),null,"fold")})},t.commands.unfoldAll=function(e){e.operation(function(){for(var n=e.firstLine(),i=e.lastLine();n<=i;n++)e.foldCode(t.Pos(n,0),null,"unfold")})},t.registerHelper("fold","combine",function(){var t=Array.prototype.slice.call(arguments,0);return function(e,n){for(var i=0;i<t.length;++i){var o=t[i](e,n);if(o)return o}}}),t.registerHelper("fold","auto",function(t,e){for(var n=t.getHelpers(e,"fold"),i=0;i<n.length;i++){var o=n[i](t,e);if(o)return o}});var i={rangeFinder:t.fold.auto,widget:"↔",minFoldSize:0,scanUp:!1,clearOnEnter:!0};function o(t,e,n){if(e&&void 0!==e[n])return e[n];var o=t.options.foldOptions;return o&&void 0!==o[n]?o[n]:i[n]}t.defineOption("foldOptions",null),t.defineExtension("foldOption",function(t,e){return o(this,t,e)})})},"697eb":function(t,e,n){},"8c33":function(t,e,n){(function(t){t(n("56b3"))})(function(t){var e=/MSIE \d/.test(navigator.userAgent)&&(null==document.documentMode||document.documentMode<8),n=t.Pos,i={"(":")>",")":"(<","[":"]>","]":"[<","{":"}>","}":"{<","<":">>",">":"<<"};function o(t){return t&&t.bracketRegex||/[(){}[\]]/}function r(t,e,r){var a=t.getLineHandle(e.line),c=e.ch-1,l=r&&r.afterCursor;null==l&&(l=/(^| )cm-fat-cursor($| )/.test(t.getWrapperElement().className));var f=o(r),u=!l&&c>=0&&f.test(a.text.charAt(c))&&i[a.text.charAt(c)]||f.test(a.text.charAt(c+1))&&i[a.text.charAt(++c)];if(!u)return null;var h=">"==u.charAt(1)?1:-1;if(r&&r.strict&&h>0!=(c==e.ch))return null;var d=t.getTokenTypeAt(n(e.line,c+1)),p=s(t,n(e.line,c+(h>0?1:0)),h,d||null,r);return null==p?null:{from:n(e.line,c),to:p&&p.pos,match:p&&p.ch==u.charAt(0),forward:h>0}}function s(t,e,r,s,a){for(var c=a&&a.maxScanLineLength||1e4,l=a&&a.maxScanLines||1e3,f=[],u=o(a),h=r>0?Math.min(e.line+l,t.lastLine()+1):Math.max(t.firstLine()-1,e.line-l),d=e.line;d!=h;d+=r){var p=t.getLine(d);if(p){var g=r>0?0:p.length-1,m=r>0?p.length:-1;if(!(p.length>c))for(d==e.line&&(g=e.ch-(r<0?1:0));g!=m;g+=r){var v=p.charAt(g);if(u.test(v)&&(void 0===s||t.getTokenTypeAt(n(d,g+1))==s)){var y=i[v];if(y&&">"==y.charAt(1)==r>0)f.push(v);else{if(!f.length)return{pos:n(d,g),ch:v};f.pop()}}}}}return d-r!=(r>0?t.lastLine():t.firstLine())&&null}function a(t,i,o){for(var s=t.state.matchBrackets.maxHighlightLineLength||1e3,a=[],c=t.listSelections(),l=0;l<c.length;l++){var f=c[l].empty()&&r(t,c[l].head,o);if(f&&t.getLine(f.from.line).length<=s){var u=f.match?"CodeMirror-matchingbracket":"CodeMirror-nonmatchingbracket";a.push(t.markText(f.from,n(f.from.line,f.from.ch+1),{className:u})),f.to&&t.getLine(f.to.line).length<=s&&a.push(t.markText(f.to,n(f.to.line,f.to.ch+1),{className:u}))}}if(a.length){e&&t.state.focused&&t.focus();var h=function(){t.operation(function(){for(var t=0;t<a.length;t++)a[t].clear()})};if(!i)return h;setTimeout(h,800)}}function c(t){t.operation(function(){t.state.matchBrackets.currentlyHighlighted&&(t.state.matchBrackets.currentlyHighlighted(),t.state.matchBrackets.currentlyHighlighted=null),t.state.matchBrackets.currentlyHighlighted=a(t,!1,t.state.matchBrackets)})}t.defineOption("matchBrackets",!1,function(e,n,i){i&&i!=t.Init&&(e.off("cursorActivity",c),e.state.matchBrackets&&e.state.matchBrackets.currentlyHighlighted&&(e.state.matchBrackets.currentlyHighlighted(),e.state.matchBrackets.currentlyHighlighted=null)),n&&(e.state.matchBrackets="object"==typeof n?n:{},e.on("cursorActivity",c))}),t.defineExtension("matchBrackets",function(){a(this,!0)}),t.defineExtension("findMatchingBracket",function(t,e,n){return(n||"boolean"==typeof e)&&(n?(n.strict=e,e=n):e=e?{strict:!0}:null),r(this,t,e)}),t.defineExtension("scanForBracket",function(t,e,n,i){return s(this,t,e,n,i)})})},"9b74":function(t,e,n){(function(t){t(n("56b3"))})(function(t){"use strict";var e="CodeMirror-hint",n="CodeMirror-hint-active";function i(t,e){this.cm=t,this.options=e,this.widget=null,this.debounce=0,this.tick=0,this.startPos=this.cm.getCursor("start"),this.startLen=this.cm.getLine(this.startPos.line).length-this.cm.getSelection().length;var n=this;t.on("cursorActivity",this.activityFunc=function(){n.cursorActivity()})}t.showHint=function(t,e,n){if(!e)return t.showHint(n);n&&n.async&&(e.async=!0);var i={hint:e};if(n)for(var o in n)i[o]=n[o];return t.showHint(i)},t.defineExtension("showHint",function(e){e=s(this,this.getCursor("start"),e);var n=this.listSelections();if(!(n.length>1)){if(this.somethingSelected()){if(!e.hint.supportsSelection)return;for(var o=0;o<n.length;o++)if(n[o].head.line!=n[o].anchor.line)return}this.state.completionActive&&this.state.completionActive.close();var r=this.state.completionActive=new i(this,e);r.options.hint&&(t.signal(this,"startCompletion",this),r.update(!0))}}),t.defineExtension("closeHint",function(){this.state.completionActive&&this.state.completionActive.close()});var o=window.requestAnimationFrame||function(t){return setTimeout(t,1e3/60)},r=window.cancelAnimationFrame||clearTimeout;function s(t,e,n){var i=t.options.hintOptions,o={};for(var r in p)o[r]=p[r];if(i)for(var r in i)void 0!==i[r]&&(o[r]=i[r]);if(n)for(var r in n)void 0!==n[r]&&(o[r]=n[r]);return o.hint.resolve&&(o.hint=o.hint.resolve(t,e)),o}function a(t){return"string"==typeof t?t:t.text}function c(t,e){var n={Up:function(){e.moveFocus(-1)},Down:function(){e.moveFocus(1)},PageUp:function(){e.moveFocus(1-e.menuSize(),!0)},PageDown:function(){e.moveFocus(e.menuSize()-1,!0)},Home:function(){e.setFocus(0)},End:function(){e.setFocus(e.length-1)},Enter:e.pick,Tab:e.pick,Esc:e.close},i=/Mac/.test(navigator.platform);i&&(n["Ctrl-P"]=function(){e.moveFocus(-1)},n["Ctrl-N"]=function(){e.moveFocus(1)});var o=t.options.customKeys,r=o?{}:n;function s(t,i){var o;o="string"!=typeof i?function(t){return i(t,e)}:n.hasOwnProperty(i)?n[i]:i,r[t]=o}if(o)for(var a in o)o.hasOwnProperty(a)&&s(a,o[a]);var c=t.options.extraKeys;if(c)for(var a in c)c.hasOwnProperty(a)&&s(a,c[a]);return r}function l(t,e){while(e&&e!=t){if("LI"===e.nodeName.toUpperCase()&&e.parentNode==t)return e;e=e.parentNode}}function f(i,o){this.completion=i,this.data=o,this.picked=!1;var r=this,s=i.cm,f=s.getInputField().ownerDocument,u=f.defaultView||f.parentWindow,h=this.hints=f.createElement("ul"),d=i.cm.options.theme;h.className="CodeMirror-hints "+d,this.selectedHint=o.selectedHint||0;for(var p=o.list,g=0;g<p.length;++g){var m=h.appendChild(f.createElement("li")),v=p[g],y=e+(g!=this.selectedHint?"":" "+n);null!=v.className&&(y=v.className+" "+y),m.className=y,v.render?v.render(m,o,v):m.appendChild(f.createTextNode(v.displayText||a(v))),m.hintId=g}var b=i.options.container||f.body,k=s.cursorCoords(i.options.alignWithWord?o.from:null),w=k.left,x=k.bottom,C=!0,A=0,L=0;if(b!==f.body){var S=-1!==["absolute","relative","fixed"].indexOf(u.getComputedStyle(b).position),T=S?b:b.offsetParent,F=T.getBoundingClientRect(),O=f.body.getBoundingClientRect();A=F.left-O.left-T.scrollLeft,L=F.top-O.top-T.scrollTop}h.style.left=w-A+"px",h.style.top=x-L+"px";var H=u.innerWidth||Math.max(f.body.offsetWidth,f.documentElement.offsetWidth),M=u.innerHeight||Math.max(f.body.offsetHeight,f.documentElement.offsetHeight);b.appendChild(h);var E=h.getBoundingClientRect(),P=E.bottom-M,_=h.scrollHeight>h.clientHeight+1,B=s.getScrollInfo();if(P>0){var z=E.bottom-E.top,N=k.top-(k.bottom-E.top);if(N-z>0)h.style.top=(x=k.top-z-L)+"px",C=!1;else if(z>M){h.style.height=M-5+"px",h.style.top=(x=k.bottom-E.top-L)+"px";var I=s.getCursor();o.from.ch!=I.ch&&(k=s.cursorCoords(I),h.style.left=(w=k.left-A)+"px",E=h.getBoundingClientRect())}}var R,W=E.right-H;if(W>0&&(E.right-E.left>H&&(h.style.width=H-5+"px",W-=E.right-E.left-H),h.style.left=(w=k.left-W-A)+"px"),_)for(var U=h.firstChild;U;U=U.nextSibling)U.style.paddingRight=s.display.nativeBarWidth+"px";(s.addKeyMap(this.keyMap=c(i,{moveFocus:function(t,e){r.changeActive(r.selectedHint+t,e)},setFocus:function(t){r.changeActive(t)},menuSize:function(){return r.screenAmount()},length:p.length,close:function(){i.close()},pick:function(){r.pick()},data:o})),i.options.closeOnUnfocus)&&(s.on("blur",this.onBlur=function(){R=setTimeout(function(){i.close()},100)}),s.on("focus",this.onFocus=function(){clearTimeout(R)}));return s.on("scroll",this.onScroll=function(){var t=s.getScrollInfo(),e=s.getWrapperElement().getBoundingClientRect(),n=x+B.top-t.top,o=n-(u.pageYOffset||(f.documentElement||f.body).scrollTop);if(C||(o+=h.offsetHeight),o<=e.top||o>=e.bottom)return i.close();h.style.top=n+"px",h.style.left=w+B.left-t.left+"px"}),t.on(h,"dblclick",function(t){var e=l(h,t.target||t.srcElement);e&&null!=e.hintId&&(r.changeActive(e.hintId),r.pick())}),t.on(h,"click",function(t){var e=l(h,t.target||t.srcElement);e&&null!=e.hintId&&(r.changeActive(e.hintId),i.options.completeOnSingleClick&&r.pick())}),t.on(h,"mousedown",function(){setTimeout(function(){s.focus()},20)}),t.signal(o,"select",p[this.selectedHint],h.childNodes[this.selectedHint]),!0}function u(t,e){if(!t.somethingSelected())return e;for(var n=[],i=0;i<e.length;i++)e[i].supportsSelection&&n.push(e[i]);return n}function h(t,e,n,i){if(t.async)t(e,i,n);else{var o=t(e,n);o&&o.then?o.then(i):i(o)}}function d(e,n){var i,o=e.getHelpers(n,"hint");if(o.length){var r=function(t,e,n){var i=u(t,o);function r(o){if(o==i.length)return e(null);h(i[o],t,n,function(t){t&&t.list.length>0?e(t):r(o+1)})}r(0)};return r.async=!0,r.supportsSelection=!0,r}return(i=e.getHelper(e.getCursor(),"hintWords"))?function(e){return t.hint.fromList(e,{words:i})}:t.hint.anyword?function(e,n){return t.hint.anyword(e,n)}:function(){}}i.prototype={close:function(){this.active()&&(this.cm.state.completionActive=null,this.tick=null,this.cm.off("cursorActivity",this.activityFunc),this.widget&&this.data&&t.signal(this.data,"close"),this.widget&&this.widget.close(),t.signal(this.cm,"endCompletion",this.cm))},active:function(){return this.cm.state.completionActive==this},pick:function(e,n){var i=e.list[n];i.hint?i.hint(this.cm,e,i):this.cm.replaceRange(a(i),i.from||e.from,i.to||e.to,"complete"),t.signal(e,"pick",i),this.close()},cursorActivity:function(){this.debounce&&(r(this.debounce),this.debounce=0);var t=this.cm.getCursor(),e=this.cm.getLine(t.line);if(t.line!=this.startPos.line||e.length-t.ch!=this.startLen-this.startPos.ch||t.ch<this.startPos.ch||this.cm.somethingSelected()||!t.ch||this.options.closeCharacters.test(e.charAt(t.ch-1)))this.close();else{var n=this;this.debounce=o(function(){n.update()}),this.widget&&this.widget.disable()}},update:function(t){if(null!=this.tick){var e=this,n=++this.tick;h(this.options.hint,this.cm,this.options,function(i){e.tick==n&&e.finishUpdate(i,t)})}},finishUpdate:function(e,n){this.data&&t.signal(this.data,"update");var i=this.widget&&this.widget.picked||n&&this.options.completeSingle;this.widget&&this.widget.close(),this.data=e,e&&e.list.length&&(i&&1==e.list.length?this.pick(e,0):(this.widget=new f(this,e),t.signal(e,"shown")))}},f.prototype={close:function(){if(this.completion.widget==this){this.completion.widget=null,this.hints.parentNode.removeChild(this.hints),this.completion.cm.removeKeyMap(this.keyMap);var t=this.completion.cm;this.completion.options.closeOnUnfocus&&(t.off("blur",this.onBlur),t.off("focus",this.onFocus)),t.off("scroll",this.onScroll)}},disable:function(){this.completion.cm.removeKeyMap(this.keyMap);var t=this;this.keyMap={Enter:function(){t.picked=!0}},this.completion.cm.addKeyMap(this.keyMap)},pick:function(){this.completion.pick(this.data,this.selectedHint)},changeActive:function(e,i){if(e>=this.data.list.length?e=i?this.data.list.length-1:0:e<0&&(e=i?0:this.data.list.length-1),this.selectedHint!=e){var o=this.hints.childNodes[this.selectedHint];o&&(o.className=o.className.replace(" "+n,"")),o=this.hints.childNodes[this.selectedHint=e],o.className+=" "+n,o.offsetTop<this.hints.scrollTop?this.hints.scrollTop=o.offsetTop-3:o.offsetTop+o.offsetHeight>this.hints.scrollTop+this.hints.clientHeight&&(this.hints.scrollTop=o.offsetTop+o.offsetHeight-this.hints.clientHeight+3),t.signal(this.data,"select",this.data.list[this.selectedHint],o)}},screenAmount:function(){return Math.floor(this.hints.clientHeight/this.hints.firstChild.offsetHeight)||1}},t.registerHelper("hint","auto",{resolve:d}),t.registerHelper("hint","fromList",function(e,n){var i,o=e.getCursor(),r=e.getTokenAt(o),s=t.Pos(o.line,r.start),a=o;r.start<o.ch&&/\w/.test(r.string.charAt(o.ch-r.start-1))?i=r.string.substr(0,o.ch-r.start):(i="",s=o);for(var c=[],l=0;l<n.words.length;l++){var f=n.words[l];f.slice(0,i.length)==i&&c.push(f)}if(c.length)return{list:c,from:s,to:a}}),t.commands.autocomplete=t.showHint;var p={hint:t.hint.auto,completeSingle:!0,alignWithWord:!0,closeCharacters:/[\s()\[\]{};:>,]/,closeOnUnfocus:!0,completeOnSingleClick:!0,container:null,customKeys:null,extraKeys:null};t.defineOption("hintOptions",null)})},cbc8:function(t,e,n){(function(t){t(n("56b3"),n("4895"))})(function(t){"use strict";t.defineOption("foldGutter",!1,function(e,o,r){r&&r!=t.Init&&(e.clearGutter(e.state.foldGutter.options.gutter),e.state.foldGutter=null,e.off("gutterClick",c),e.off("changes",l),e.off("viewportChange",f),e.off("fold",u),e.off("unfold",u),e.off("swapDoc",l)),o&&(e.state.foldGutter=new n(i(o)),a(e),e.on("gutterClick",c),e.on("changes",l),e.on("viewportChange",f),e.on("fold",u),e.on("unfold",u),e.on("swapDoc",l))});var e=t.Pos;function n(t){this.options=t,this.from=this.to=0}function i(t){return!0===t&&(t={}),null==t.gutter&&(t.gutter="CodeMirror-foldgutter"),null==t.indicatorOpen&&(t.indicatorOpen="CodeMirror-foldgutter-open"),null==t.indicatorFolded&&(t.indicatorFolded="CodeMirror-foldgutter-folded"),t}function o(t,n){for(var i=t.findMarks(e(n,0),e(n+1,0)),o=0;o<i.length;++o)if(i[o].__isFold){var r=i[o].find(-1);if(r&&r.line===n)return i[o]}}function r(t){if("string"==typeof t){var e=document.createElement("div");return e.className=t+" CodeMirror-guttermarker-subtle",e}return t.cloneNode(!0)}function s(t,n,i){var s=t.state.foldGutter.options,a=n,c=t.foldOption(s,"minFoldSize"),l=t.foldOption(s,"rangeFinder");t.eachLine(n,i,function(n){var i=null;if(o(t,a))i=r(s.indicatorFolded);else{var f=e(a,0),u=l&&l(t,f);u&&u.to.line-u.from.line>=c&&(i=r(s.indicatorOpen))}t.setGutterMarker(n,s.gutter,i),++a})}function a(t){var e=t.getViewport(),n=t.state.foldGutter;n&&(t.operation(function(){s(t,e.from,e.to)}),n.from=e.from,n.to=e.to)}function c(t,n,i){var r=t.state.foldGutter;if(r){var s=r.options;if(i==s.gutter){var a=o(t,n);a?a.clear():t.foldCode(e(n,0),s)}}}function l(t){var e=t.state.foldGutter;if(e){var n=e.options;e.from=e.to=0,clearTimeout(e.changeUpdate),e.changeUpdate=setTimeout(function(){a(t)},n.foldOnChangeTimeSpan||600)}}function f(t){var e=t.state.foldGutter;if(e){var n=e.options;clearTimeout(e.changeUpdate),e.changeUpdate=setTimeout(function(){var n=t.getViewport();e.from==e.to||n.from-e.to>20||e.from-n.to>20?a(t):t.operation(function(){n.from<e.from&&(s(t,n.from,e.from),e.from=n.from),n.to>e.to&&(s(t,e.to,n.to),e.to=n.to)})},n.updateViewportTimeSpan||400)}}function u(t,e){var n=t.state.foldGutter;if(n){var i=e.line;i>=n.from&&i<n.to&&s(t,i,i+1)}}})},db91:function(t,e,n){(function(t){t(n("56b3"))})(function(t){"use strict";function e(t){return new RegExp("^(("+t.join(")|(")+"))\\b")}var n=e(["and","or","not","is"]),i=["as","assert","break","class","continue","def","del","elif","else","except","finally","for","from","global","if","import","lambda","pass","raise","return","try","while","with","yield","in"],o=["abs","all","any","bin","bool","bytearray","callable","chr","classmethod","compile","complex","delattr","dict","dir","divmod","enumerate","eval","filter","float","format","frozenset","getattr","globals","hasattr","hash","help","hex","id","input","int","isinstance","issubclass","iter","len","list","locals","map","max","memoryview","min","next","object","oct","open","ord","pow","property","range","repr","reversed","round","set","setattr","slice","sorted","staticmethod","str","sum","super","tuple","type","vars","zip","__import__","NotImplemented","Ellipsis","__debug__"];function r(t){return t.scopes[t.scopes.length-1]}t.registerHelper("hintWords","python",i.concat(o)),t.defineMode("python",function(s,a){for(var c="error",l=a.delimiters||a.singleDelimiters||/^[\(\)\[\]\{\}@,:`=;\.\\]/,f=[a.singleOperators,a.doubleOperators,a.doubleDelimiters,a.tripleDelimiters,a.operators||/^([-+*\/%\/&|^]=?|[<>=]+|\/\/=?|\*\*=?|!=|[~!@]|\.\.\.)/],u=0;u<f.length;u++)f[u]||f.splice(u--,1);var h=a.hangingIndent||s.indentUnit,d=i,p=o;void 0!=a.extra_keywords&&(d=d.concat(a.extra_keywords)),void 0!=a.extra_builtins&&(p=p.concat(a.extra_builtins));var g=!(a.version&&Number(a.version)<3);if(g){var m=a.identifiers||/^[_A-Za-z\u00A1-\uFFFF][_A-Za-z0-9\u00A1-\uFFFF]*/;d=d.concat(["nonlocal","False","True","None","async","await"]),p=p.concat(["ascii","bytes","exec","print"]);var v=new RegExp("^(([rbuf]|(br)|(fr))?('{3}|\"{3}|['\"]))","i")}else{m=a.identifiers||/^[_A-Za-z][_A-Za-z0-9]*/;d=d.concat(["exec","print"]),p=p.concat(["apply","basestring","buffer","cmp","coerce","execfile","file","intern","long","raw_input","reduce","reload","unichr","unicode","xrange","False","True","None"]);v=new RegExp("^(([rubf]|(ur)|(br))?('{3}|\"{3}|['\"]))","i")}var y=e(d),b=e(p);function k(t,e){var n=t.sol()&&"\\"!=e.lastToken;if(n&&(e.indent=t.indentation()),n&&"py"==r(e).type){var i=r(e).offset;if(t.eatSpace()){var o=t.indentation();return o>i?A(e):o<i&&S(t,e)&&"#"!=t.peek()&&(e.errorToken=!0),null}var s=w(t,e);return i>0&&S(t,e)&&(s+=" "+c),s}return w(t,e)}function w(t,e){if(t.eatSpace())return null;if(t.match(/^#.*/))return"comment";if(t.match(/^[0-9\.]/,!1)){var i=!1;if(t.match(/^[\d_]*\.\d+(e[\+\-]?\d+)?/i)&&(i=!0),t.match(/^[\d_]+\.\d*/)&&(i=!0),t.match(/^\.\d+/)&&(i=!0),i)return t.eat(/J/i),"number";var o=!1;if(t.match(/^0x[0-9a-f_]+/i)&&(o=!0),t.match(/^0b[01_]+/i)&&(o=!0),t.match(/^0o[0-7_]+/i)&&(o=!0),t.match(/^[1-9][\d_]*(e[\+\-]?[\d_]+)?/)&&(t.eat(/J/i),o=!0),t.match(/^0(?![\dx])/i)&&(o=!0),o)return t.eat(/L/i),"number"}if(t.match(v)){var r=-1!==t.current().toLowerCase().indexOf("f");return r?(e.tokenize=x(t.current(),e.tokenize),e.tokenize(t,e)):(e.tokenize=C(t.current(),e.tokenize),e.tokenize(t,e))}for(var s=0;s<f.length;s++)if(t.match(f[s]))return"operator";return t.match(l)?"punctuation":"."==e.lastToken&&t.match(m)?"property":t.match(y)||t.match(n)?"keyword":t.match(b)?"builtin":t.match(/^(self|cls)\b/)?"variable-2":t.match(m)?"def"==e.lastToken||"class"==e.lastToken?"def":"variable":(t.next(),c)}function x(t,e){while("rubf".indexOf(t.charAt(0).toLowerCase())>=0)t=t.substr(1);var n=1==t.length,i="string";function o(t){return function(e,n){var i=w(e,n);return"punctuation"==i&&("{"==e.current()?n.tokenize=o(t+1):"}"==e.current()&&(n.tokenize=t>1?o(t-1):r)),i}}function r(r,s){while(!r.eol())if(r.eatWhile(/[^'"\{\}\\]/),r.eat("\\")){if(r.next(),n&&r.eol())return i}else{if(r.match(t))return s.tokenize=e,i;if(r.match("{{"))return i;if(r.match("{",!1))return s.tokenize=o(0),r.current()?i:s.tokenize(r,s);if(r.match("}}"))return i;if(r.match("}"))return c;r.eat(/['"]/)}if(n){if(a.singleLineStringErrors)return c;s.tokenize=e}return i}return r.isString=!0,r}function C(t,e){while("rubf".indexOf(t.charAt(0).toLowerCase())>=0)t=t.substr(1);var n=1==t.length,i="string";function o(o,r){while(!o.eol())if(o.eatWhile(/[^'"\\]/),o.eat("\\")){if(o.next(),n&&o.eol())return i}else{if(o.match(t))return r.tokenize=e,i;o.eat(/['"]/)}if(n){if(a.singleLineStringErrors)return c;r.tokenize=e}return i}return o.isString=!0,o}function A(t){while("py"!=r(t).type)t.scopes.pop();t.scopes.push({offset:r(t).offset+s.indentUnit,type:"py",align:null})}function L(t,e,n){var i=t.match(/^([\s\[\{\(]|#.*)*$/,!1)?null:t.column()+1;e.scopes.push({offset:e.indent+h,type:n,align:i})}function S(t,e){var n=t.indentation();while(e.scopes.length>1&&r(e).offset>n){if("py"!=r(e).type)return!0;e.scopes.pop()}return r(e).offset!=n}function T(t,e){t.sol()&&(e.beginningOfLine=!0);var n=e.tokenize(t,e),i=t.current();if(e.beginningOfLine&&"@"==i)return t.match(m,!1)?"meta":g?"operator":c;if(/\S/.test(i)&&(e.beginningOfLine=!1),"variable"!=n&&"builtin"!=n||"meta"!=e.lastToken||(n="meta"),"pass"!=i&&"return"!=i||(e.dedent+=1),"lambda"==i&&(e.lambda=!0),":"!=i||e.lambda||"py"!=r(e).type||A(e),1==i.length&&!/string|comment/.test(n)){var o="[({".indexOf(i);if(-1!=o&&L(t,e,"])}".slice(o,o+1)),o="])}".indexOf(i),-1!=o){if(r(e).type!=i)return c;e.indent=e.scopes.pop().offset-h}}return e.dedent>0&&t.eol()&&"py"==r(e).type&&(e.scopes.length>1&&e.scopes.pop(),e.dedent-=1),n}var F={startState:function(t){return{tokenize:k,scopes:[{offset:t||0,type:"py",align:null}],indent:t||0,lastToken:null,lambda:!1,dedent:0}},token:function(t,e){var n=e.errorToken;n&&(e.errorToken=!1);var i=T(t,e);return i&&"comment"!=i&&(e.lastToken="keyword"==i||"punctuation"==i?t.current():i),"punctuation"==i&&(i=null),t.eol()&&e.lambda&&(e.lambda=!1),n?i+" "+c:i},indent:function(e,n){if(e.tokenize!=k)return e.tokenize.isString?t.Pass:0;var i=r(e),o=i.type==n.charAt(0);return null!=i.align?i.align-(o?1:0):i.offset-(o?h:0)},electricInput:/^\s*[\}\]\)]$/,closeBrackets:{triples:"'\""},lineComment:"#",fold:"indent"};return F}),t.defineMIME("text/x-python","python");var s=function(t){return t.split(" ")};t.defineMIME("text/x-cython",{name:"python",extra_keywords:s("by cdef cimport cpdef ctypedef enum except extern gil include nogil property public readonly struct union DEF IF ELIF ELSE")})})},f6b6:function(t,e,n){}}]);