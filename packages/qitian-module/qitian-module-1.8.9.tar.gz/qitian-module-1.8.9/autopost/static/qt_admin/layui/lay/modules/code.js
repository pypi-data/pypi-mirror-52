/** layui-v2.4.4 MIT License By https://www.layui.com */
 ;layui.define("jquery",function(e){"use strict";var a=layui.$,l="http://www.layui.com/doc/modules/code.html";e("code",function(e){var t=[];e=e||{},e.elem=a(e.elem||".layui-code"),e.about=!("about"in e)||e.about,e.elem.each(function(){t.push(this)}),layui.each(t.reverse(),function(t,i){var c=a(i),o=c.html();(c.attr("lay-encode")||e.encode)&&(o=o.replace(/&(?!#?[a-zA-Z0-9]+;)/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/'/g,"&#39;").replace(/"/g,"&quot;")),c.html('<ol class="layui-code-ol"><li>'+o.replace(/[\r\t\n]+/g,"</li><li>")+"</li></ol>"),c.find(">.layui-code-h3")[0]||c.prepend('<h3 class="layui-code-h3">'+(c.attr("lay-title")||e.title||"code")+(e.about?'<a href="'+l+'" target="_blank">layui.code</a>':"")+"</h3>");var d=c.find(">.layui-code-ol");c.addClass("layui-box layui-code-view"),(c.attr("lay-skin")||e.skin)&&c.addClass("layui-code-"+(c.attr("lay-skin")||e.skin)),(d.find("li").length/100|0)>0&&d.css("margin-left",(d.find("li").length/100|0)+"px"),(c.attr("lay-height")||e.height)&&d.css("max-height",c.attr("lay-height")||e.height)})})}).addcss("modules/code.css","skincodecss");