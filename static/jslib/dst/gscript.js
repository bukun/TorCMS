function select_sub_tag(html2) {
    $("#showCnt").load(html2)
}

function js_update_pass() {
    $.ajax({
        type: "POST",
        url: "/user/reset-password",
        data: "email=" + $("#user_email").val(),
        success: function (msg) {
            alert("Your password has been reset！Please check your e-mail！"), location.href = "/user/info"
        },
        error: function () {
            alert("Password reset failed. Please confirm that your e-mail address is valid, and the interval between two reset should be longer than 1 minute.")
        }
    })
}

function entity_down(uid) {

    $.ajax({
        url: "/entity/down/" + uid,
        type: "post",
        data: '',
        timeout: 1e3,
        processData: false,
        contentType: false,
        error: function () {
//                    alert("Reload")
        },
        success: function (result) {
            var msg_json = $.parseJSON(result);
            if (msg_json.down_code == 1) {
                window.open(msg_json.down_url)
            }
        }
    })

}

function g_load_kindcat() {
    $.ajax({
        url: "/list/j_kindcat/" + $("#kcat").val(), type: "GET", data: {}, timeout: 1e3, error: function () {
            // alert("Reload")
        }, success: function (result) {
            var data = eval("(" + result + ")");
            $("#pcat0").empty(), $("<option></option>").val("0").text("selectd").appendTo($("#pcat0")), $.each(data, function (tagidx, tagname) {
                $("<option></option>").val(tagidx).text(tagname).appendTo($("#pcat0"))
            })
        }
    })
}

function g_load_postcat(ii) {
    0 == $("#pcat" + ii.toString()).val() ? $("#gcat" + ii.toString()).empty() : $.ajax({
        url: "/list/j_subcat/" + $("#pcat" + ii.toString()).val(),
        type: "GET",
        data: {},
        timeout: 1e3,
        error: function () {
            alert("Reload")
        },
        success: function (result) {
            var data = eval("(" + result + ")");
            $("#gcat" + ii.toString()).empty(), $.each(data, function (tagidx, tagname) {
                $("<option></option>").val(tagidx).text(tagname).appendTo($("#gcat" + ii.toString()))
            })
        }
    })
}

function g_load_infocat(ii) {
    0 == $("#pcat" + ii.toString()).val() ? $("#gcat" + ii.toString()).empty() : $.ajax({
        url: "/list/j_subcat/" + $("#pcat" + ii.toString()).val(),
        type: "GET",
        data: {},
        timeout: 1e3,
        error: function () {
            alert("Reload")
        },
        success: function (result) {
            var data = eval("(" + result + ")");
            $("#gcat" + ii.toString()).empty(), $.each(data, function (tagidx, tagname) {
                $("<option></option>").val(tagidx).text(tagname).appendTo($("#gcat" + ii.toString()))
            })
        }
    })
}

function reply_zan(reply_id) {

    var AjaxUrl = "/reply/zan/" + reply_id;
    $.getJSON(AjaxUrl, function (Json) {
        0 == Json.text_zan || $("#text_zan_" + reply_id).html(Json.text_zan)
    })
}

function reply_del(reply_id) {
    var AjaxUrl = "/reply/delete/" + reply_id;
    $.getJSON(AjaxUrl, function (Json) {
        1 == Json.del_zan ? $("#del_zan_" + reply_id).html("") : alert("删除失败！")
    })
}

function reply_it(view_id) {
    var txt = $("#cnt_reply").val();
    txt.length < 1 || ($.post("/reply/add/" + view_id, {cnt_reply: txt}, function (result) {
        var msg_json = $.parseJSON(result);
        $("#pinglun").load("/reply/get/" + msg_json.uid)
    }), $("#cnt_reply").val(""), $("#cnt_reply").attr("disabled", !0), $("#btn_submit_reply").attr("disabled", !0))
    comment_count(view_id)
}

function comment_count(reply_id) {

    var AjaxUrl = "/reply/com_count/" + reply_id;
    $.getJSON(AjaxUrl, function (Json) {
        0 == Json.comment_count || $("#comment_count").html(Json.comment_count)

    })
}

function reply_del_com(reply_id) {
    var AjaxUrl = "/reply/delete_com/" + reply_id;
    $.getJSON(AjaxUrl, function (Json) {
        1 == Json.del_reply ? $("#" + reply_id).html("") : alert("Delete failed!")
    })
}

function comment_it(view_id, reply_id, cid, bid, isreply) {
    var txt = $("#" + cid).val();
    txt.length < 1 || ($.post("/reply/add_reply/" + view_id + '/' + reply_id, {cnt_reply: txt}, function (result) {

        var msg_json = $.parseJSON(result);
        $("#reply_comment" + reply_id).load("/reply/get/" + msg_json.uid + "?isreply=" + isreply)
    }), $("#" + cid).val(""), $("#" + cid).attr("disabled", !0), $("#" + bid).attr("disabled", !0))
    reply_count(reply_id)

}

function reply_count(reply_id) {

    var AjaxUrl = "/reply/count/" + reply_id;
    $.getJSON(AjaxUrl, function (Json) {
        0 == Json.reply_count || $("#reply_count_" + reply_id).html(Json.reply_count)
        0 == Json.reply_count || $("#reply_count1_" + reply_id).html(Json.reply_count)
    })
}

function reply_modify(pid, cntid, cate) {
    var txt = $("#" + cntid).val();
    txt.length < 1 || ($.post("/reply/modify/" + pid + '/' + cate, {cnt_reply: txt}, function (result) {
        var msg_json = $.parseJSON(result);
        if (cate == 0) {
            $("#reply_cnt" + pid).html(msg_json.pinglun)
        } else {
            $("#comment_id" + pid).html(msg_json.pinglun)
        }

    }))
}

function del_layout(layout_id) {
    return $.ajax({
        url: "/layout/delete/" + layout_id,
        type: "GET",
        cache: !1,
        data: {},
        dataType: "html",
        timeout: 1e3,
        error: function () {
            return alert("Delete failed!")
        },
        success: function (result) {
            return alert("Delete successfully! Please refresh the page manually!")
        }
    })
}

function del_geojson(gson_id) {
    return $.ajax({
        url: "/geojson/delete/" + gson_id,
        type: "GET",
        cache: !1,
        data: {},
        dataType: "html",
        timeout: 1e3,
        error: function () {
            return alert("Delete failed!")
        },
        success: function (result) {
            return alert("Delete successfully! Please refresh the page manually!")
        }
    })
}

if ($.ready(), "undefined" == typeof CodeMirror) ; else if ($("#cnt_md").length > 0) var editor = CodeMirror.fromTextArea(document.getElementById("cnt_md"), {
    lineWrapping: !0,
    mode: "markdown",
    lineNumbers: !0,
    theme: "default",
    extraKeys: {Enter: "newlineAndIndentContinueMarkdownList"}
});
$("#sub_reset").click(function () {
    $("#form_reset").valid() ? js_update_pass() : alert("Error")
}), $("#act_collect").click(function () {
    $.ajax({
        url: "/collect/" + post_uid,
        type: "GET",
        cache: !1,
        data: {},
        dataType: "html",
        timeout: 1e3,
        error: function () {
            alert("Please log in first.")
        },
        success: function (result) {
            $.parseJSON(result);
            var al_collect = document.getElementById('already_collect');
            var act_collect = document.getElementById('act_collect');
            al_collect.style.display = 'inline';
            act_collect.style.display = 'none';

        }
    })
}), $("#already_collect").click(function () {

    $.ajax({
        url: "/collect/remove/" + post_uid,
        type: "GET",
        cache: !1,
        data: {},
        dataType: "html",
        timeout: 1e3,
        error: function () {
            // alert("Please log in first.")
        },
        success: function (result) {
            $.parseJSON(result);
            var al_collect = document.getElementById('already_collect');
            var act_collect = document.getElementById('act_collect');
            act_collect.style.display = 'inline';
            al_collect.style.display = 'none';

        }
    })
}), $(document).ready(function () {
    var AjaxUrl, baseMaps, cities, currentX, currentY, currentZoom, geojsonid, map, map_uid, mp_uid, mapson, nexrad,
        onMapClick,
        onZoomend, osm, overlayMaps, popup, vlat, vlon, vmarker, vzoom_current, vzoom_max, vzoom_min;
    if (currentZoom = 0, currentX = 0, currentY = 0, map_uid = "", $("#btn_updatemap").click(function () {
        $.ajax({
            url: "/admin_map/_update_view/" + map_uid,
            type: "POST",
            cache: !1,
            data: {ext_lat: currentY, ext_lon: currentX, ext_zoom_current: currentZoom},
            dataType: "html",
            timeout: 1e3,
            error: function () {
                alert("Please log in first.")
            },
            success: function (result) {
                $("#btn_updatemap").text("Successfully")
            }
        })
    }), $("#map").length > 0) {
        $("#map").hasClass("mapdiv") || $("#map").css({
            height: "350px",
            width: "92%"
        }), mapson = $("#map").data("map");

            if (mapson.i.substr(0, 1) == 'm') {

                 mp_uid = "mp" + mapson.i.substr(-4);

            } else {

                 mp_uid = "qn" + mapson.i.substr(-4);

            };
       

        map_uid=mapson.i, vlon = mapson.x, vlat = mapson.y, vzoom_current = mapson.v, vzoom_max = mapson.m, vzoom_min = mapson.n, vmarker = mapson.k, geojsonid = mapson.g, $("#btn_overlay").click(function () {
            var sig_map_1, sig_map_2, url_new;
            return sig_map_1 = $("#over_map_1").val(), sig_map_2 = $("#over_map_2").val(), url_new = "/map/overlay/" + map_uid + "/" + sig_map_1, "" !== sig_map_2 && (url_new = url_new + "/" + sig_map_2), window.location.href = url_new
        }), $("#save_view").click(function () {
            var view_url;
            return view_url = $("#current_view_url").attr("href").split("?")[1] + "&map=" + map_uid, $.ajax({
                url: "/layout/save",
                type: "POST",
                cache: !1,
                data: view_url,
                dataType: "html",
                timeout: 1e3,
                error: function () {
                    return $("#current_view_url").text("Please save the view after login, or check to see if you've started browsing the map."), $("#current_view_url").css("color", "red")
                },
                success: function (result) {
                    return $("#current_view_url").text("The view has been saved successfully.")
                }
            })
        }), onMapClick = function (e) {

            var cmap_coor, div_str, link_str;
            return popup.setLatLng(e.latlng), popup.setContent("Coordinate position" + e.latlng.toString()), currentZoom = map.getZoom(), cmap_coor = e.latlng, link_str = "http://drr.ikcest.org/map/" + map_uid + "?zoom=" + currentZoom + "&lat=" + cmap_coor.lat.toFixed(4) + "&lon=" + cmap_coor.lng.toFixed(4) + "&marker=1", "" !== geojsonid && (link_str = link_str + "&geojson=" + geojsonid), div_str = '{"i" : "' + mp_uid + '",  "x" : ' + cmap_coor.lng.toFixed(3).toString() + ', "y": ' + cmap_coor.lat.toFixed(3).toString() + ', "v":' + currentZoom.toString() + ', "m": ' + vzoom_max + ', "n": ' + vzoom_min + ', "g": "' + geojsonid + '", "k": 1}', map_add_log(div_str, mapson), div_str = '&lt;div id="map" data-map = \'' + div_str + "'&gt;&lt;/div&gt;", $("#current_view_url").html(link_str), $("#mapref").html(div_str), $("#current_view_url").attr("href", link_str), popup.openOn(map)
        }, onZoomend = function () {
            var cmap_coor, div_str, link_str;
            return currentZoom = map.getZoom(), cmap_coor = map.getCenter(), currentX = cmap_coor.lng.toFixed(3).toString(), currentY = cmap_coor.lat.toFixed(3).toString(), link_str = "http://drr.ikcest.org/map/" + map_uid + "?zoom=" + currentZoom + "&lat=" + cmap_coor.lat.toFixed(4) + "&lon=" + cmap_coor.lng.toFixed(4), "" !== geojsonid && (link_str = link_str + "&geojson=" + geojsonid), div_str = '{"i" : "' + mp_uid + '", "x" : ' + cmap_coor.lng.toFixed(3).toString() + ', "y": ' + cmap_coor.lat.toFixed(3).toString() + ', "v":' + currentZoom.toString() + ', "m": ' + vzoom_max + ', "n": ' + vzoom_min + ', "g": "' + geojsonid + '", "k": 0}', map_add_log(div_str, mapson), div_str = '&lt;div id="map" data-map = \'' + div_str + "'&gt;&lt;/div&gt;", $("#current_view_url").css("color", ""), $("#current_view_url").html(link_str), $("#mapref").html(div_str), $("#current_view_url").attr("href", link_str)
        }, popup = L.popup(), cities = new L.LayerGroup, new L.FeatureGroup, nexrad = L.tileLayer.wms("https://tile.osgeo.cn/service?", {
            layers: mp_uid,
            format: "image/png",
            transparent: !0,
            attribution: 'Map &copy; <a href="http://drr.ikcest.org/map/' + map_uid + '">DRRKS</a>'
        });
        var osm = L.tileLayer.chinaProvider("TianDiTu.Normal.Annotion", {
                maxZoom: 18,
                minZoom: 1
            }), osm1 = L.tileLayer.chinaProvider("TianDiTu.Normal.Map", {
                maxZoom: 18,
                minZoom: 1
            }),
            osm2 = L.tileLayer("http://t{s}.tianditu.gov.cn/DataServer?T=eva_w&x={x}&y={y}&l={z}&tk=57f1b8146ef867f14189f3f4bb1adc1c", {
                subdomains: ['0', '1', '2', '3', '4', '5', '6', '7']
            }), the_basemap = L.layerGroup([osm1, osm2]);
        return nexrad.addTo(cities), map = L.map("map", {
            center: [vlat, vlon],
            zoom: vzoom_current,
            maxZoom: vzoom_max,
            minZoom: vzoom_min,
            layers: [cities]
        }), the_basemap.addTo(map), "1" === vmarker.toString() && L.marker([vlat, vlon]).addTo(map), AjaxUrl = "/geojson/gson/" + geojsonid, "" !== geojsonid && $.getJSON(AjaxUrl, function (gjson) {
            var gson_arr;
            return gson_arr = new Array, $.each(gjson, function (i, item) {
                return gson_arr[i] = item
            }), L.geoJson(gson_arr).addTo(map)
        }), map.on("zoomend", onZoomend), map.on("moveend", onZoomend), map.on("click", onMapClick), baseMaps = {BaseMap: the_basemap}, overlayMaps = {"Layer": nexrad}, L.control.layers(baseMaps, overlayMaps).addTo(map)
    }
});

function map_add_log(map_str, mapson) {
    map_str = JSON.parse(map_str);


    var _browserType, userAgent = window.navigator.userAgent.toLowerCase();

//获取浏览器类型
    if (userAgent.indexOf('firefox') !== -1) {
        _browserType = 'Firefox';
    } else if ((userAgent.indexOf("msie") !== -1 || userAgent.indexOf("rv") !== -1) && userAgent.indexOf("trident") !== -1) {
        _browserType = 'IE';
    } else if (userAgent.indexOf('wow') < 0 && userAgent.indexOf("edge") < 0) {
        if (userAgent.indexOf("safari") !== -1 && userAgent.indexOf("chrome") === -1) {
            _browserType = 'Safari';
        } else {
            _browserType = 'Chrome';
        }
    } else if (userAgent.indexOf('wow') !== -1 && userAgent.indexOf('net') < 0 && userAgent.indexOf('firefox') < 0) {
        _browserType = '360';
    } else {
        _browserType = 'other';
    }


    var map_data = new FormData();

    map_data.append("uid", map_str.i);
    map_data.append("lat", map_str.y);
    map_data.append("lon", map_str.x);
    map_data.append("center", '[' + mapson.y + ',' + mapson.x + ']');
    map_data.append("zoom", map_str.v);
    map_data.append("zoom_max", map_str.m);
    map_data.append("zoom_min", map_str.n);
    map_data.append("geojson", map_str.g);
    map_data.append("kind", map_str.k);
    map_data.append("browser", _browserType);


    $.ajax({
        url: "/map_log/_add/",
        type: "post",
        data: map_data,
        timeout: 1e3,
        processData: false,
        contentType: false,
        error: function () {
//                    alert("Reload")
        },
        success: function (result) {

        }
    })

}