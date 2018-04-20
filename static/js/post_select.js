var BrowserUtil = { navi: navigator.userAgent.toLowerCase(),
    isIE: function () {
        var B = this;
        return (B.navi.indexOf("msie") != -1) && (B.navi.indexOf("opera") == -1) && (B.navi.indexOf("omniweb") == -1)
    },
    isIE7: function () {
        var B = this;
        return (B.navi.indexOf("msie") != -1) && (B.navi.indexOf("msie 7") != -1) && (B.navi.indexOf("opera") == -1) && (B.navi.indexOf("omniweb") == -1)
    },
    isMaxthon: function () {
        var B = this;
        return (B.navi.indexOf("msie") != -1) && (B.navi.indexOf("maxthon") != -1) && (B.navi.indexOf("opera") == -1) && (B.navi.indexOf("omniweb") == -1)
    }, isMaxthon2: function () {
        var B = this;
        return (B.navi.indexOf("msie") != -1) && (B.navi.indexOf("maxthon 2") != -1) && (B.navi.indexOf("opera") == -1) && (B.navi.indexOf("omniweb") == -1)
    }, getBody: function () {
        return (document.compatMode && document.compatMode != "BackCompat") ? document.documentElement : document.body
    }, getScrollTop: function () {
        return this.isIE() ? this.getBody().scrollTop : window.pageYOffset
    }, getScrollLeft: function () {
        return this.isIE() ? this.getBody().scrollLeft : window.pageXOffset
    }, getxy: function (E) {
        var C = E.offsetTop;
        var B = E.offsetLeft;
        var A = E.offsetWidth;
        var D = E.offsetHeight;
        while (E = E.offsetParent) {
            C += E.offsetTop;
            B += E.offsetLeft
        }
        return { x: B, y: C, w: A, h: D}
    } };
var topcurrenli;
function nav_over(D) {
//        if (topcurrenli != null) {
//            D.style.top = topcurrenli;
    //        }
    var A = BrowserUtil.getxy(D);
    var L = (D.clientHeight);
    var G = BrowserUtil.getBody().clientHeight;
    var I = G + BrowserUtil.getScrollTop();
    var F = document.getElementById("YMenu-side");
    if ((A.y + L) > I - 10) {
        if (D.style.top > (I - (A.y + L)) - 10) {
            D.style.top = (I - (A.y + L)) - 10 + "px";
        }
    }
}
/**
 * 延迟显示插件lazyShow
 */
(function (a) {
    a.fn.lazyShow = function (c) {
        var b = a.extend({curren: "hover", delay: 10}, c || {});
        a.each(this, function () {
            var f = null, e = null, d = false;
            a(this).bind("mouseover", function () {
                if (d) {
                    clearTimeout(e)
                } else {
                    var g = a(this);
                    f = setTimeout(function () {
                        g.addClass(b.curren);
                        nav_over(g.find(".ym-submnu").get(0));
                        d = true
                    }, b.delay)
                }
            }).bind("mouseout", function () {
                if (d) {
                    var g = a(this);
                    e = setTimeout(function () {
                        g.removeClass(b.curren);
                        d = false
                    }, b.delay)
                } else {
                    clearTimeout(f)
                }
            })
        })
    }
})(jQuery);
// 自动切换超链接
$(document).ready(function () {
    $("#ymenu-side > .ym-mainmnu > .ym-tab").lazyShow({ curren: "curren", delay: 120});
    var _host = location.host;
    $('#ymenu-side ul li a').each(function (i) {
        var _url = $(this).attr('href');
        if (_url) {
            $(this).attr('href', _url);
        }
    });
});