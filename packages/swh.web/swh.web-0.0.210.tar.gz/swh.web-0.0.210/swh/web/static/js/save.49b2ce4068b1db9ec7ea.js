/*! For license information please see save.49b2ce4068b1db9ec7ea.js.LICENSE */
!function(e,t){"object"==typeof exports&&"object"==typeof module?module.exports=t():"function"==typeof define&&define.amd?define([],t):"object"==typeof exports?exports.save=t():(e.swh=e.swh||{},e.swh.save=t())}(window,function(){return function(e){var t={};function n(r){if(t[r])return t[r].exports;var i=t[r]={i:r,l:!1,exports:{}};return e[r].call(i.exports,i,i.exports,n),i.l=!0,i.exports}return n.m=e,n.c=t,n.d=function(e,t,r){n.o(e,t)||Object.defineProperty(e,t,{enumerable:!0,get:r})},n.r=function(e){"undefined"!=typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(e,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(e,"__esModule",{value:!0})},n.t=function(e,t){if(1&t&&(e=n(e)),8&t)return e;if(4&t&&"object"==typeof e&&e&&e.__esModule)return e;var r=Object.create(null);if(n.r(r),Object.defineProperty(r,"default",{enumerable:!0,value:e}),2&t&&"string"!=typeof e)for(var i in e)n.d(r,i,function(t){return e[t]}.bind(null,i));return r},n.n=function(e){var t=e&&e.__esModule?function(){return e.default}:function(){return e};return n.d(t,"a",t),t},n.o=function(e,t){return Object.prototype.hasOwnProperty.call(e,t)},n.p="/static/",n(n.s=720)}({35:function(e,t,n){"use strict";n.d(t,"b",function(){return i}),n.d(t,"a",function(){return s}),n.d(t,"c",function(){return o});var r=n(5),i=768,s=992,o=Object(r.h)("img/swh-spinner.gif")},361:function(e,t){e.exports=function(e){return e.webpackPolyfill||(e.deprecate=function(){},e.paths=[],e.children||(e.children=[]),Object.defineProperty(e,"loaded",{enumerable:!0,get:function(){return e.l}}),Object.defineProperty(e,"id",{enumerable:!0,get:function(){return e.i}}),e.webpackPolyfill=1),e}},5:function(e,t,n){"use strict";function r(e){if(!e.ok)throw e;return e}function i(e){for(var t=0;t<e.length;++t)if(!e[t].ok)throw e[t];return e}function s(e){return"/static/"+e}function o(e,t,n){return void 0===t&&(t={}),void 0===n&&(n=null),t["X-CSRFToken"]=Cookies.get("csrftoken"),fetch(e,{credentials:"include",headers:t,method:"POST",body:n})}function a(e,t){return new RegExp("(?:git|https?|git@)(?:\\:\\/\\/)?"+t+"[/|:][A-Za-z0-9-]+?\\/[\\w\\.-]+\\/?(?!=.git)(?:\\.git(?:\\/?|\\#[\\w\\.\\-_]+)?)?$").test(e)}function u(){history.replaceState("",document.title,window.location.pathname+window.location.search)}function c(e,t){var n=window.getSelection();n.removeAllRanges();var r=document.createRange();r.setStart(e,0),"#text"!==t.nodeName?r.setEnd(t,t.childNodes.length):r.setEnd(t,t.textContent.length),n.addRange(r)}function l(e,t,n){void 0===n&&(n=!1);var r="",i="";return n&&(r='<button type="button" class="close" data-dismiss="alert" aria-label="Close">\n        <span aria-hidden="true">&times;</span>\n      </button>',i="alert-dismissible"),'<div class="alert alert-'+e+" "+i+'" role="alert">'+t+r+"</div>"}n.d(t,"b",function(){return r}),n.d(t,"c",function(){return i}),n.d(t,"h",function(){return s}),n.d(t,"a",function(){return o}),n.d(t,"e",function(){return a}),n.d(t,"f",function(){return u}),n.d(t,"g",function(){return c}),n.d(t,"d",function(){return l})},555:function(e,t){e.exports=function(){throw new Error("define cannot be used indirect")}},696:function(e,t,n){(function(e){(function(e,t,r){"use strict";var i=function(e,t,n){n=s.extend({},s.options,n);var r=s.runValidations(e,t,n);if(r.some(function(e){return s.isPromise(e.error)}))throw new Error("Use validate.async if you want support for promises");return i.processValidationResults(r,n)},s=i;s.extend=function(e){return[].slice.call(arguments,1).forEach(function(t){for(var n in t)e[n]=t[n]}),e},s.extend(i,{version:{major:0,minor:13,patch:1,metadata:null,toString:function(){var e=s.format("%{major}.%{minor}.%{patch}",s.version);return s.isEmpty(s.version.metadata)||(e+="+"+s.version.metadata),e}},Promise:"undefined"!=typeof Promise?Promise:null,EMPTY_STRING_REGEXP:/^\s*$/,runValidations:function(e,t,n){var r,i,o,a,u,c,l,f=[];for(r in(s.isDomElement(e)||s.isJqueryElement(e))&&(e=s.collectFormValues(e)),t)for(i in o=s.getDeepObjectValue(e,r),a=s.result(t[r],o,e,r,n,t)){if(!(u=s.validators[i]))throw l=s.format("Unknown validator %{name}",{name:i}),new Error(l);c=a[i],(c=s.result(c,o,e,r,n,t))&&f.push({attribute:r,value:o,validator:i,globalOptions:n,attributes:e,options:c,error:u.call(u,o,c,r,e,n)})}return f},processValidationResults:function(e,t){e=s.pruneEmptyErrors(e,t),e=s.expandMultipleErrors(e,t),e=s.convertErrorMessages(e,t);var n=t.format||"grouped";if("function"!=typeof s.formatters[n])throw new Error(s.format("Unknown format %{format}",t));return e=s.formatters[n](e),s.isEmpty(e)?void 0:e},async:function(e,t,n){var r=(n=s.extend({},s.async.options,n)).wrapErrors||function(e){return e};!1!==n.cleanAttributes&&(e=s.cleanAttributes(e,t));var i=s.runValidations(e,t,n);return new s.Promise(function(o,a){s.waitForResults(i).then(function(){var u=s.processValidationResults(i,n);u?a(new r(u,n,e,t)):o(e)},function(e){a(e)})})},single:function(e,t,n){return n=s.extend({},s.single.options,n,{format:"flat",fullMessages:!1}),s({single:e},{single:t},n)},waitForResults:function(e){return e.reduce(function(e,t){return s.isPromise(t.error)?e.then(function(){return t.error.then(function(e){t.error=e||null})}):e},new s.Promise(function(e){e()}))},result:function(e){var t=[].slice.call(arguments,1);return"function"==typeof e&&(e=e.apply(null,t)),e},isNumber:function(e){return"number"==typeof e&&!isNaN(e)},isFunction:function(e){return"function"==typeof e},isInteger:function(e){return s.isNumber(e)&&e%1==0},isBoolean:function(e){return"boolean"==typeof e},isObject:function(e){return e===Object(e)},isDate:function(e){return e instanceof Date},isDefined:function(e){return null!=e},isPromise:function(e){return!!e&&s.isFunction(e.then)},isJqueryElement:function(e){return e&&s.isString(e.jquery)},isDomElement:function(e){return!!e&&(!(!e.querySelectorAll||!e.querySelector)&&(!(!s.isObject(document)||e!==document)||("object"==typeof HTMLElement?e instanceof HTMLElement:e&&"object"==typeof e&&null!==e&&1===e.nodeType&&"string"==typeof e.nodeName)))},isEmpty:function(e){var t;if(!s.isDefined(e))return!0;if(s.isFunction(e))return!1;if(s.isString(e))return s.EMPTY_STRING_REGEXP.test(e);if(s.isArray(e))return 0===e.length;if(s.isDate(e))return!1;if(s.isObject(e)){for(t in e)return!1;return!0}return!1},format:s.extend(function(e,t){return s.isString(e)?e.replace(s.format.FORMAT_REGEXP,function(e,n,r){return"%"===n?"%{"+r+"}":String(t[r])}):e},{FORMAT_REGEXP:/(%?)%\{([^\}]+)\}/g}),prettify:function(e){return s.isNumber(e)?100*e%1==0?""+e:parseFloat(Math.round(100*e)/100).toFixed(2):s.isArray(e)?e.map(function(e){return s.prettify(e)}).join(", "):s.isObject(e)?s.isDefined(e.toString)?e.toString():JSON.stringify(e):(e=""+e).replace(/([^\s])\.([^\s])/g,"$1 $2").replace(/\\+/g,"").replace(/[_-]/g," ").replace(/([a-z])([A-Z])/g,function(e,t,n){return t+" "+n.toLowerCase()}).toLowerCase()},stringifyValue:function(e,t){return(t&&t.prettify||s.prettify)(e)},isString:function(e){return"string"==typeof e},isArray:function(e){return"[object Array]"==={}.toString.call(e)},isHash:function(e){return s.isObject(e)&&!s.isArray(e)&&!s.isFunction(e)},contains:function(e,t){return!!s.isDefined(e)&&(s.isArray(e)?-1!==e.indexOf(t):t in e)},unique:function(e){return s.isArray(e)?e.filter(function(e,t,n){return n.indexOf(e)==t}):e},forEachKeyInKeypath:function(e,t,n){if(s.isString(t)){var r,i="",o=!1;for(r=0;r<t.length;++r)switch(t[r]){case".":o?(o=!1,i+="."):(e=n(e,i,!1),i="");break;case"\\":o?(o=!1,i+="\\"):o=!0;break;default:o=!1,i+=t[r]}return n(e,i,!0)}},getDeepObjectValue:function(e,t){if(s.isObject(e))return s.forEachKeyInKeypath(e,t,function(e,t){if(s.isObject(e))return e[t]})},collectFormValues:function(e,t){var n,r,i,o,a,u,c={};if(s.isJqueryElement(e)&&(e=e[0]),!e)return c;for(t=t||{},o=e.querySelectorAll("input[name], textarea[name]"),n=0;n<o.length;++n)if(i=o.item(n),!s.isDefined(i.getAttribute("data-ignored"))){var l=i.name.replace(/\./g,"\\\\.");u=s.sanitizeFormValue(i.value,t),"number"===i.type?u=u?+u:null:"checkbox"===i.type?i.attributes.value?i.checked||(u=c[l]||null):u=i.checked:"radio"===i.type&&(i.checked||(u=c[l]||null)),c[l]=u}for(o=e.querySelectorAll("select[name]"),n=0;n<o.length;++n)if(i=o.item(n),!s.isDefined(i.getAttribute("data-ignored"))){if(i.multiple)for(r in u=[],i.options)(a=i.options[r])&&a.selected&&u.push(s.sanitizeFormValue(a.value,t));else{var f=void 0!==i.options[i.selectedIndex]?i.options[i.selectedIndex].value:"";u=s.sanitizeFormValue(f,t)}c[i.name]=u}return c},sanitizeFormValue:function(e,t){return t.trim&&s.isString(e)&&(e=e.trim()),!1!==t.nullify&&""===e?null:e},capitalize:function(e){return s.isString(e)?e[0].toUpperCase()+e.slice(1):e},pruneEmptyErrors:function(e){return e.filter(function(e){return!s.isEmpty(e.error)})},expandMultipleErrors:function(e){var t=[];return e.forEach(function(e){s.isArray(e.error)?e.error.forEach(function(n){t.push(s.extend({},e,{error:n}))}):t.push(e)}),t},convertErrorMessages:function(e,t){var n=[],r=(t=t||{}).prettify||s.prettify;return e.forEach(function(e){var i=s.result(e.error,e.value,e.attribute,e.options,e.attributes,e.globalOptions);s.isString(i)?("^"===i[0]?i=i.slice(1):!1!==t.fullMessages&&(i=s.capitalize(r(e.attribute))+" "+i),i=i.replace(/\\\^/g,"^"),i=s.format(i,{value:s.stringifyValue(e.value,t)}),n.push(s.extend({},e,{error:i}))):n.push(e)}),n},groupErrorsByAttribute:function(e){var t={};return e.forEach(function(e){var n=t[e.attribute];n?n.push(e):t[e.attribute]=[e]}),t},flattenErrorsToArray:function(e){return e.map(function(e){return e.error}).filter(function(e,t,n){return n.indexOf(e)===t})},cleanAttributes:function(e,t){function n(e,t,n){return s.isObject(e[t])?e[t]:e[t]=!!n||{}}return s.isObject(t)&&s.isObject(e)?function e(t,n){if(!s.isObject(t))return t;var r,i,o=s.extend({},t);for(i in t)r=n[i],s.isObject(r)?o[i]=e(o[i],r):r||delete o[i];return o}(e,t=function(e){var t,r={};for(t in e)e[t]&&s.forEachKeyInKeypath(r,t,n);return r}(t)):{}},exposeModule:function(e,t,n,r,i){n?(r&&r.exports&&(n=r.exports=e),n.validate=e):(t.validate=e,e.isFunction(i)&&i.amd&&i([],function(){return e}))},warn:function(e){"undefined"!=typeof console&&console.warn&&console.warn("[validate.js] "+e)},error:function(e){"undefined"!=typeof console&&console.error&&console.error("[validate.js] "+e)}}),i.validators={presence:function(e,t){if(!1!==(t=s.extend({},this.options,t)).allowEmpty?!s.isDefined(e):s.isEmpty(e))return t.message||this.message||"can't be blank"},length:function(e,t,n){if(s.isDefined(e)){var r,i=(t=s.extend({},this.options,t)).is,o=t.maximum,a=t.minimum,u=[],c=(e=(t.tokenizer||function(e){return e})(e)).length;return s.isNumber(c)?(s.isNumber(i)&&c!==i&&(r=t.wrongLength||this.wrongLength||"is the wrong length (should be %{count} characters)",u.push(s.format(r,{count:i}))),s.isNumber(a)&&c<a&&(r=t.tooShort||this.tooShort||"is too short (minimum is %{count} characters)",u.push(s.format(r,{count:a}))),s.isNumber(o)&&c>o&&(r=t.tooLong||this.tooLong||"is too long (maximum is %{count} characters)",u.push(s.format(r,{count:o}))),u.length>0?t.message||u:void 0):t.message||this.notValid||"has an incorrect length"}},numericality:function(e,t,n,r,i){if(s.isDefined(e)){var o,a,u=[],c={greaterThan:function(e,t){return e>t},greaterThanOrEqualTo:function(e,t){return e>=t},equalTo:function(e,t){return e===t},lessThan:function(e,t){return e<t},lessThanOrEqualTo:function(e,t){return e<=t},divisibleBy:function(e,t){return e%t==0}},l=(t=s.extend({},this.options,t)).prettify||i&&i.prettify||s.prettify;if(s.isString(e)&&t.strict){var f="^-?(0|[1-9]\\d*)";if(t.onlyInteger||(f+="(\\.\\d+)?"),f+="$",!new RegExp(f).test(e))return t.message||t.notValid||this.notValid||this.message||"must be a valid number"}if(!0!==t.noStrings&&s.isString(e)&&!s.isEmpty(e)&&(e=+e),!s.isNumber(e))return t.message||t.notValid||this.notValid||this.message||"is not a number";if(t.onlyInteger&&!s.isInteger(e))return t.message||t.notInteger||this.notInteger||this.message||"must be an integer";for(o in c)if(a=t[o],s.isNumber(a)&&!c[o](e,a)){var d="not"+s.capitalize(o),p=t[d]||this[d]||this.message||"must be %{type} %{count}";u.push(s.format(p,{count:a,type:l(o)}))}return t.odd&&e%2!=1&&u.push(t.notOdd||this.notOdd||this.message||"must be odd"),t.even&&e%2!=0&&u.push(t.notEven||this.notEven||this.message||"must be even"),u.length?t.message||u:void 0}},datetime:s.extend(function(e,t){if(!s.isFunction(this.parse)||!s.isFunction(this.format))throw new Error("Both the parse and format functions needs to be set to use the datetime/date validator");if(s.isDefined(e)){var n,r=[],i=(t=s.extend({},this.options,t)).earliest?this.parse(t.earliest,t):NaN,o=t.latest?this.parse(t.latest,t):NaN;return e=this.parse(e,t),isNaN(e)||t.dateOnly&&e%864e5!=0?(n=t.notValid||t.message||this.notValid||"must be a valid date",s.format(n,{value:arguments[0]})):(!isNaN(i)&&e<i&&(n=t.tooEarly||t.message||this.tooEarly||"must be no earlier than %{date}",n=s.format(n,{value:this.format(e,t),date:this.format(i,t)}),r.push(n)),!isNaN(o)&&e>o&&(n=t.tooLate||t.message||this.tooLate||"must be no later than %{date}",n=s.format(n,{date:this.format(o,t),value:this.format(e,t)}),r.push(n)),r.length?s.unique(r):void 0)}},{parse:null,format:null}),date:function(e,t){return t=s.extend({},t,{dateOnly:!0}),s.validators.datetime.call(s.validators.datetime,e,t)},format:function(e,t){(s.isString(t)||t instanceof RegExp)&&(t={pattern:t});var n,r=(t=s.extend({},this.options,t)).message||this.message||"is invalid",i=t.pattern;if(s.isDefined(e))return s.isString(e)?(s.isString(i)&&(i=new RegExp(t.pattern,t.flags)),(n=i.exec(e))&&n[0].length==e.length?void 0:r):r},inclusion:function(e,t){if(s.isDefined(e)&&(s.isArray(t)&&(t={within:t}),t=s.extend({},this.options,t),!s.contains(t.within,e))){var n=t.message||this.message||"^%{value} is not included in the list";return s.format(n,{value:e})}},exclusion:function(e,t){if(s.isDefined(e)&&(s.isArray(t)&&(t={within:t}),t=s.extend({},this.options,t),s.contains(t.within,e))){var n=t.message||this.message||"^%{value} is restricted";return s.isString(t.within[e])&&(e=t.within[e]),s.format(n,{value:e})}},email:s.extend(function(e,t){var n=(t=s.extend({},this.options,t)).message||this.message||"is not a valid email";if(s.isDefined(e))return s.isString(e)&&this.PATTERN.exec(e)?void 0:n},{PATTERN:/^(?:[a-z0-9!#$%&'*+\/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+\/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])$/i}),equality:function(e,t,n,r,i){if(s.isDefined(e)){s.isString(t)&&(t={attribute:t});var o=(t=s.extend({},this.options,t)).message||this.message||"is not equal to %{attribute}";if(s.isEmpty(t.attribute)||!s.isString(t.attribute))throw new Error("The attribute must be a non empty string");var a=s.getDeepObjectValue(r,t.attribute),u=t.comparator||function(e,t){return e===t},c=t.prettify||i&&i.prettify||s.prettify;return u(e,a,t,n,r)?void 0:s.format(o,{attribute:c(t.attribute)})}},url:function(e,t){if(s.isDefined(e)){var n=(t=s.extend({},this.options,t)).message||this.message||"is not a valid url",r=t.schemes||this.schemes||["http","https"],i=t.allowLocal||this.allowLocal||!1,o=t.allowDataUrl||this.allowDataUrl||!1;if(!s.isString(e))return n;var a="^(?:(?:"+r.join("|")+")://)(?:\\S+(?::\\S*)?@)?(?:",u="(?:\\.(?:[a-z\\u00a1-\\uffff]{2,}))";if(i?u+="?":a+="(?!(?:10|127)(?:\\.\\d{1,3}){3})(?!(?:169\\.254|192\\.168)(?:\\.\\d{1,3}){2})(?!172\\.(?:1[6-9]|2\\d|3[0-1])(?:\\.\\d{1,3}){2})",a+="(?:[1-9]\\d?|1\\d\\d|2[01]\\d|22[0-3])(?:\\.(?:1?\\d{1,2}|2[0-4]\\d|25[0-5])){2}(?:\\.(?:[1-9]\\d?|1\\d\\d|2[0-4]\\d|25[0-4]))|(?:(?:[a-z\\u00a1-\\uffff0-9]-*)*[a-z\\u00a1-\\uffff0-9]+)(?:\\.(?:[a-z\\u00a1-\\uffff0-9]-*)*[a-z\\u00a1-\\uffff0-9]+)*"+u+")(?::\\d{2,5})?(?:[/?#]\\S*)?$",o){a="(?:"+a+")|(?:^data:(?:\\w+\\/[-+.\\w]+(?:;[\\w=]+)*)?(?:;base64)?,[A-Za-z0-9-_.!~\\*'();\\/?:@&=+$,%]*$)"}return new RegExp(a,"i").exec(e)?void 0:n}},type:s.extend(function(e,t,n,r,i){if(s.isString(t)&&(t={type:t}),s.isDefined(e)){var o,a=s.extend({},this.options,t),u=a.type;if(!s.isDefined(u))throw new Error("No type was specified");if(o=s.isFunction(u)?u:this.types[u],!s.isFunction(o))throw new Error("validate.validators.type.types."+u+" must be a function.");if(!o(e,a,n,r,i)){var c=t.message||this.messages[u]||this.message||a.message||(s.isFunction(u)?"must be of the correct type":"must be of type %{type}");return s.isFunction(c)&&(c=c(e,t,n,r,i)),s.format(c,{attribute:s.prettify(n),type:u})}}},{types:{object:function(e){return s.isObject(e)&&!s.isArray(e)},array:s.isArray,integer:s.isInteger,number:s.isNumber,string:s.isString,date:s.isDate,boolean:s.isBoolean},messages:{}})},i.formatters={detailed:function(e){return e},flat:s.flattenErrorsToArray,grouped:function(e){var t;for(t in e=s.groupErrorsByAttribute(e))e[t]=s.flattenErrorsToArray(e[t]);return e},constraint:function(e){var t;for(t in e=s.groupErrorsByAttribute(e))e[t]=e[t].map(function(e){return e.validator}).sort();return e}},i.exposeModule(i,this,e,t,n(555))}).call(this,t,e,n(555))}).call(this,n(361)(e))},720:function(e,t,n){e.exports=n(721)},721:function(e,t,n){"use strict";n.r(t),n.d(t,"initOriginSave",function(){return u}),n.d(t,"validateSaveOriginUrl",function(){return c}),n.d(t,"initTakeNewSnapshot",function(){return l});var r,i=n(5),s=n(35),o=n(696);function a(e,t,n,r,s){var o=Urls.origin_save_request(e,t);$(".swh-processing-save-request").css("display","block"),Object(i.a)(o,{Accept:"application/json","Content-Type":"application/json"}).then(i.b).then(function(e){return e.json()}).then(function(e){$(".swh-processing-save-request").css("display","none"),"accepted"===e.save_request_status?n():r()}).catch(function(e){$(".swh-processing-save-request").css("display","none"),s(e.status)})}function u(){$(document).ready(function(){$.fn.dataTable.ext.errMode="none",fetch(Urls.origin_save_types_list()).then(function(e){return e.json()}).then(function(e){var t=e,n=Array.isArray(t),r=0;for(t=n?t:t[Symbol.iterator]();;){var i;if(n){if(r>=t.length)break;i=t[r++]}else{if((r=t.next()).done)break;i=r.value}var s=i;$("#swh-input-origin-type").append('<option value="'+s+'">'+s+"</option>")}}),r=$("#swh-origin-save-requests").on("error.dt",function(e,t,n,r){$("#swh-origin-save-request-list-error").text("An error occurred while retrieving the save requests list"),console.log(r)}).DataTable({serverSide:!0,processing:!0,language:{processing:'<img src="'+s.c+'"></img>'},ajax:Urls.origin_save_requests_list("all"),searchDelay:1e3,columns:[{data:"save_request_date",name:"request_date",render:function(e,t,n){return"display"===t?new Date(e).toLocaleString():e}},{data:"origin_type",name:"origin_type"},{data:"origin_url",name:"origin_url",render:function(e,t,n){if("display"===t){var r=$.fn.dataTable.render.text().display(e);return'<a href="'+r+'">'+r+"</a>"}return e}},{data:"save_request_status",name:"status"},{data:"save_task_status",name:"loading_task_status",render:function(e,t,n){if("succeed"===e){var r=Urls.browse_origin(n.origin_url);return n.visit_date&&(r+="visit/"+n.visit_date+"/"),'<a href="'+r+'">'+e+"</a>"}return e}}],scrollY:"50vh",scrollCollapse:!0,order:[[0,"desc"]],responsive:{details:{type:"none"}}}),swh.webapp.addJumpToPagePopoverToDataTable(r),$("#swh-origin-save-requests-list-tab").on("shown.bs.tab",function(){r.draw(),window.location.hash="#requests"}),$("#swh-origin-save-request-create-tab").on("shown.bs.tab",function(){Object(i.f)()});var e=Object(i.d)("success",'The "save code now" request has been accepted and will be processed as soon as possible.'),t=Object(i.d)("warning",'The "save code now" request has been put in pending state and may be accepted for processing after manual review.'),n=Object(i.d)("danger",'The "save code now" request has been rejected because the provided origin url is blacklisted.'),o=Object(i.d)("danger",'The rate limit for "save code now" requests has been reached. Please try again later.'),u=Object(i.d)("danger",'An unexpected error happened when submitting the "save code now request');$("#swh-save-origin-form").submit(function(r){(r.preventDefault(),r.stopPropagation(),$(".alert").alert("close"),r.target.checkValidity())?($(r.target).removeClass("was-validated"),a($("#swh-input-origin-type").val(),$("#swh-input-origin-url").val(),function(){return $("#swh-origin-save-request-status").html(e)},function(){return $("#swh-origin-save-request-status").html(t)},function(e){$("#swh-origin-save-request-status").css("color","red"),403===e?$("#swh-origin-save-request-status").html(n):429===e?$("#swh-origin-save-request-status").html(o):$("#swh-origin-save-request-status").html(u)})):$(r.target).addClass("was-validated")}),$("#swh-show-origin-save-requests-list").on("click",function(e){e.preventDefault(),$('.nav-tabs a[href="#swh-origin-save-requests-list"]').tab("show")}),$("#swh-input-origin-url").on("input",function(e){var t=$(this).val().trim();$(this).val(t),$("#swh-input-origin-type option").each(function(){var e=$(this).val();e&&t.includes(e)&&$(this).prop("selected",!0)})}),"#requests"===window.location.hash&&$('.nav-tabs a[href="#swh-origin-save-requests-list"]').tab("show")})}function c(e){var t=e.value.trim(),n=void 0===Object(o.validate)({website:t},{website:{url:{schemes:["http","https","svn","git"]}}});if("git"===$("#swh-input-origin-type").val()&&n){var r=t.indexOf("://github.com"),s=t.indexOf("://gitlab."),a=t.indexOf("://git.code.sf.net"),u=t.indexOf("://bitbucket.org");if(-1!==r&&r<=5)n=Object(i.e)(t,"github.com");else if(-1!==s&&s<=5){var c=s+3,l=t.indexOf("/",c);if(-1!==l){var f=t.substr(c,l-c);n=Object(i.e)(t,f)&&t.endsWith(".git")}else n=!1}else-1!==a&&a<=5?n=Object(i.e)(t,"git.code.sf.net/p"):-1!==u&&u<=5&&(n=Object(i.e)(t,"bitbucket.org"))}n?e.setCustomValidity(""):e.setCustomValidity("The origin url is not valid or does not reference a code repository")}function l(){var e=Object(i.d)("success",'The "take new snapshot" request has been accepted and will be processed as soon as possible.'),t=Object(i.d)("warning",'The "take new snapshot" request has been put in pending state and may be accepted for processing after manual review.'),n=Object(i.d)("danger",'The "take new snapshot" request has been rejected.'),r=Object(i.d)("danger",'The rate limit for "take new snapshot" requests has been reached. Please try again later.'),s=Object(i.d)("danger",'An unexpected error happened when submitting the "save code now request".');$(document).ready(function(){$("#swh-take-new-snapshot-form").submit(function(i){i.preventDefault(),i.stopPropagation(),a($("#swh-input-origin-type").val(),$("#swh-input-origin-url").val(),function(){return $("#swh-take-new-snapshot-request-status").html(e)},function(){return $("#swh-take-new-snapshot-request-status").html(t)},function(e){$("#swh-take-new-snapshot-request-status").css("color","red"),403===e?$("#swh-take-new-snapshot-request-status").html(n):429===e?$("#swh-take-new-snapshot-request-status").html(r):$("#swh-take-new-snapshot-request-status").html(s)})})})}}})});
//# sourceMappingURL=save.49b2ce4068b1db9ec7ea.js.map