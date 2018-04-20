/**************************************\
 *  cssAnimate 1.1.5 for jQuery       *
 *  (c) 2012 - Clemens Damke          *
 *  Licensed under MIT License        *
 *  Works with jQuery >=1.4.3         *
\**************************************/
(function (a) {
    var b = ["Webkit", "Moz", "O", "Ms", "Khtml", ""];
    var c = ["borderRadius", "boxShadow", "userSelect", "transformOrigin", "transformStyle", "transition", "transitionDuration", "transitionProperty", "transitionTimingFunction", "backgroundOrigin", "backgroundSize", "animation", "filter", "zoom", "columns", "perspective", "perspectiveOrigin", "appearance"];
    a.fn.cssSetQueue = function (b, c) {
        v = this;
        var d = v.data("cssQueue") ? v.data("cssQueue") : [];
        var e = v.data("cssCall") ? v.data("cssCall") : [];
        var f = 0;
        var g = {};
        a.each(c, function (a, b) {
            g[a] = b
        });
        while (1) {
            if (!e[f]) {
                e[f] = g.complete;
                break
            }
            f++
        }
        g.complete = f;
        d.push([b, g]);
        v.data({
            cssQueue: d,
            cssRunning: true,
            cssCall: e
        })
    };
    a.fn.cssRunQueue = function () {
        v = this;
        var a = v.data("cssQueue") ? v.data("cssQueue") : [];
        if (a[0]) v.cssEngine(a[0][0], a[0][1]);
        else v.data("cssRunning", false);
        a.shift();
        v.data("cssQueue", a)
    };
    a.cssMerge = function (b, c, d) {
        a.each(c, function (c, e) {
            a.each(d, function (a, d) {
                b[d + c] = e
            })
        });
        return b
    };
    a.fn.cssAnimationData = function (a, b) {
        var c = this;
        var d = c.data("cssAnimations");
        if (!d) d = {};
        if (!d[a]) d[a] = [];
        d[a].push(b);
        c.data("cssAnimations", d);
        return d[a]
    };
    a.fn.cssAnimationRemove = function () {
        var b = this;
		if (b.data("cssAnimations") !=undefined) {
			var c = b.data("cssAnimations");
			var d = b.data("identity");
			a.each(c, function (a, b) {
				c[a] = b.splice(d + 1, 1)
			});
			b.data("cssAnimations", c)
		}
    };
	
	
    a.css3D = function (c) {
        a("body").data("cssPerspective", isFinite(c) ? c : c ? 1e3 : 0).cssOriginal(a.cssMerge({}, {
            TransformStyle: c ? "preserve-3d" : "flat"
        }, b))
    };
    a.cssPropertySupporter = function (d) {
        a.each(c, function (c, e) {
            if (d[e]) a.each(b, function (a, b) {
                var c = e.substr(0, 1);
                d[b + c[b ? "toUpperCase" : "toLowerCase"]() + e.substr(1)] = d[e]
            })
        });
        return d
    };
    a.cssAnimateSupport = function () {
        var c = false;
        a.each(b, function (a, b) {
            c = document.body.style[b + "AnimationName"] !== undefined ? true : c
        });
        return c
    };
    a.fn.cssEngine = function (c, d) {
        function f(a) {
            return String(a).replace(/([A-Z])/g, "-$1").toLowerCase()
        }
        var e = this;
        var e = this;
        if (typeof d.complete == "number") e.data("cssCallIndex", d.complete);
        var g = {
            linear: "linear",
            swing: "ease",
            easeIn: "ease-in",
            easeOut: "ease-out",
            easeInOut: "ease-in-out"
        };
        var h = {};
        var i = a("body").data("cssPerspective");
        if (c.transform) a.each(b, function (a, b) {
            var d = b + (b ? "T" : "t") + "ransform";
            var g = e.cssOriginal(f(d));
            var j = c.transform;
            if (!g || g == "none") h[d] = "scale(1)";
            c[d] = (i && !/perspective/gi.test(j) ? "perspective(" + i + ") " : "") + j
        });
        c = a.cssPropertySupporter(c);
        var j = [];
        a.each(c, function (a, b) {
            j.push(f(a))
        });
        var k = false;
        var l = [];
        var m = [];
	
	
	
	
	
	
	
		if (j !=undefined) {
			for (var n = 0; n < j.length; n++) {
				l.push(String(d.duration / 1e3) + "s");
				var o = g[d.easing];
				m.push(o ? o : d.easing)
			}
		
			l = e.cssAnimationData("dur", l.join(", ")).join(", ");
			m = e.cssAnimationData("eas", m.join(", ")).join(", ");
			var p = e.cssAnimationData("prop", j.join(", "));
			e.data("identity", p.length - 1);
			p = p.join(", ");
			var q = {
				TransitionDuration: l,
				TransitionProperty: p,
				TransitionTimingFunction: m
			};
			var r = {};
			r = a.cssMerge(r, q, b);
			var s = c;
			a.extend(r, c);
			if (r.display == "callbackHide") k = true;
			else if (r.display) h["display"] = r.display;
			e.cssOriginal(h);
		}
	
        setTimeout(function () {
            e.cssOriginal(r);
            var b = e.data("runningCSS");
            b = !b ? s : a.extend(b, s);
            e.data("runningCSS", b);
            setTimeout(function () {
                e.data("cssCallIndex", "a");
                if (k) e.cssOriginal("display", "none");
             


				
				e.cssAnimationRemove();
                if (d.queue) e.cssRunQueue();
                if (typeof d.complete == "number") {
                    e.data("cssCall")[d.complete].call(e);
                    e.data("cssCall")[d.complete] = 0
                } else d.complete.call(e)
            }, d.duration)
        }, 0)
    };
	
    a.str2Speed = function (a) {
        return isNaN(a) ? a == "slow" ? 1e3 : a == "fast" ? 200 : 600 : a
    };
	
    a.fn.cssAnimate = function (b, c, d, e) {
        var f = this;
        var g = {
            duration: 0,
            easing: "swing",
            complete: function () {},
            queue: true
        };
        var h = {};
        h = typeof c == "object" ? c : {
            duration: c
        };
        h[d ? typeof d == "function" ? "complete" : "easing" : 0] = d;
        h[e ? "complete" : 0] = e;
        h.duration = a.str2Speed(h.duration);
        a.extend(g, h);
        if (a.cssAnimateSupport()) {
            f.each(function (c, d) {
                d = a(d);
                if (g.queue) {
                    var e = !d.data("cssRunning");
                    d.cssSetQueue(b, g);
                    if (e) d.cssRunQueue()
                } else d.cssEngine(b, g)
            })
        } else f.animate(b, g);
        return f
    };
    a.cssPresetOptGen = function (a, b) {
        var c = {};
        c[a ? typeof a == "function" ? "complete" : "easing" : 0] = a;
        c[b ? "complete" : 0] = b;
        return c
    };
    a.fn.cssFadeTo = function (b, c, d, e) {
        var f = this;
        opt = a.cssPresetOptGen(d, e);
        var g = {
            opacity: c
        };
        opt.duration = b;
        if (a.cssAnimateSupport()) {
            f.each(function (b, d) {
                d = a(d);
                if (d.data("displayOriginal") != d.cssOriginal("display") && d.cssOriginal("display") != "none") d.data("displayOriginal", d.cssOriginal("display") ? d.cssOriginal("display") : "block");
                else d.data("displayOriginal", "block");
                g.display = c ? d.data("displayOriginal") : "callbackHide";
                d.cssAnimate(g, opt)
            })
        } else f.fadeTo(b, opt);
        return f
    };
    a.fn.cssFadeOut = function (b, c, d) {
        if (a.cssAnimateSupport()) {
            if (!this.cssOriginal("opacity")) this.cssOriginal("opacity", 1);
            this.cssFadeTo(b, 0, c, d)
        } else this.fadeOut(b, c, d);
        return this
    };
    a.fn.cssFadeIn = function (b, c, d) {
        if (a.cssAnimateSupport()) {
            if (this.cssOriginal("opacity")) this.cssOriginal("opacity", 0);
            this.cssFadeTo(b, 1, c, d)
        } else this.fadeIn(b, c, d);
        return this
    };
    a.cssPx2Int = function (a) {
        return a.split("p")[0] * 1
    };
    a.fn.cssStop = function () {
        var c = this,
            d = 0;
        c.data("cssAnimations", false).each(function (f, g) {
            g = a(g);
            var h = {
                TransitionDuration: "0s"
            };
            var i = g.data("runningCSS");
            var j = {};
            if (i) a.each(i, function (b, c) {
                c = isFinite(a.cssPx2Int(c)) ? a.cssPx2Int(c) : c;
                var d = [0, 1];
                var e = {
                    color: ["#000", "#fff"],
                    background: ["#000", "#fff"],
                    "float": ["none", "left"],
                    clear: ["none", "left"],
                    border: ["none", "0px solid #fff"],
                    position: ["absolute", "relative"],
                    family: ["Arial", "Helvetica"],
                    display: ["none", "block"],
                    visibility: ["hidden", "visible"],
                    transform: ["translate(0,0)", "scale(1)"]
                };
                a.each(e, function (a, c) {
                    if ((new RegExp(a, "gi")).test(b)) d = c
                });
                j[b] = d[0] != c ? d[0] : d[1]
            });
            else i = {};
            h = a.cssMerge(j, h, b);
            g.cssOriginal(h);
            setTimeout(function () {
                var b = a(c[d]);
                b.cssOriginal(i).data({
                    runningCSS: {},
                    cssAnimations: {},
                    cssQueue: [],
                    cssRunning: false
                });
                if (typeof b.data("cssCallIndex") == "number") b.data("cssCall")[b.data("cssCallIndex")].call(b);
                b.data("cssCall", []);
                d++
            }, 0)
        });
        return c
    };
    a.fn.cssDelay = function (a) {
        return this.cssAnimate({}, a)
    };
    a.fn.cssOriginal = a.fn.css;
    a.fn.css = function (c, d) {
        var e = this,
            f = {};
        if (typeof c == "string") if (d) f[a.camelCase(c)] = d;
        else return e.cssOriginal(c);
        else f = c;
        f = a.cssPropertySupporter(f);
        var g = a("body").data("cssPerspective");
        if (f.transform) a.each(b, function (a, b) {
            var c = b + (b ? "T" : "t") + "ransform";
            var d = f.transform;
            f[c] = (g && !/perspective/gi.test(d) ? "perspective(" + g + ") " : "") + d
        });
        e.cssOriginal(f);
        return e
    }
})(jQuery)