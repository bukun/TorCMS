function select_sub_tag(html2) {
    $("#showCnt").load(html2)
}
function js_update_pass() {
    $.ajax({
        type: "POST",
        url: "/user/reset-password",
        data: "email=" + $("#user_email").val(),
        success: function (msg) {
            alert("已经成功重置了密码！请检查电子邮箱！"), location.href = "/user/info"
        },
        error: function () {
            alert("密码重置失败，请确认Email是否有效，并且两次重置时间大于1分钟！")
        }
    })
}
function g_load_kindcat() {
    $.ajax({
        url: "/list/j_kindcat/" + $("#kcat").val(), type: "GET", data: {}, timeout: 1e3, error: function () {
            alert("重新加载")
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
            alert("重新加载")
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
            alert("重新加载")
        },
        success: function (result) {
            var data = eval("(" + result + ")");
            $("#gcat" + ii.toString()).empty(), $.each(data, function (tagidx, tagname) {
                $("<option></option>").val(tagidx).text(tagname).appendTo($("#gcat" + ii.toString()))
            })
        }
    })
}
function reply_zan(reply_id, id_num) {
    id_num = id_num.toString(), zans = $("#text_zan").val();
    var AjaxUrl = "/reply/zan/" + reply_id;
    $.getJSON(AjaxUrl, function (Json) {
        0 == Json.text_zan || $("#text_zan_" + id_num).html(Json.text_zan)
    })
}
function reply_del(reply_id, id_num) {
    id_num = id_num.toString();
    var AjaxUrl = "/reply/delete/" + reply_id;
    $.getJSON(AjaxUrl, function (Json) {
        1 == Json.del_zan ? $("#del_zan_" + id_num).html("") : alert("删除失败！")
    })
}
function reply_del_com(reply_id) {
    var AjaxUrl = "/reply/delete_com/" + reply_id;
    $.getJSON(AjaxUrl, function (Json) {
         1 == Json.del_reply ? $("#" + reply_id).html("") : alert("Delete failed!")
    })
}
function reply_it(view_id) {
    var txt = $("#cnt_reply").val();
    txt.length < 10 || ($.post("/reply/add/" + view_id, {cnt_reply: txt}, function (result) {
        var msg_json = $.parseJSON(result);
        $("#pinglun").load("/reply/get/" + msg_json.uid)
    }), $("#cnt_reply").val(""), $("#cnt_reply").attr("disabled", !0), $("#btn_submit_reply").attr("disabled", !0))
}
function reply_modify(pid,cntid,cate) {
    var txt = $("#" + cntid).val();
    txt.length < 1 || ($.post("/reply/modify/" + pid +'/'+ cate, {cnt_reply: txt}, function (result) {
        var msg_json = $.parseJSON(result);
        if (cate == 0){
            $("#reply_cnt" + pid ).html(msg_json.pinglun)
        }
        else{
            $("#comment_id" + pid ).html(msg_json.pinglun)
        }

    }))
}

function comment_it(view_id,reply_id,cid,bid,id_num) {
    var txt = $("#" + cid).val();
    txt.length < 1 || ($.post("/reply/add_reply/" + view_id +'/'+ reply_id, {cnt_reply: txt}, function (result) {

        var msg_json = $.parseJSON(result);
         $("#reply_comment"+id_num).load("/reply/get_comment/" + msg_json.uid)
    }),$("#" + cid).val(""),$("#" + cid).attr("disabled", !0), $("#"+ bid ).attr("disabled", !0))
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
            return alert("删除失败！")
        },
        success: function (result) {
            return alert("删除成功！暂请手动刷新页面！")
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
            return alert("删除失败！")
        },
        success: function (result) {
            return alert("删除成功，暂请手动刷新页面！")
        }
    })
}
if ($.ready(), "undefined" == typeof CodeMirror); else if ($("#cnt_md").length > 0)var editor = CodeMirror.fromTextArea(document.getElementById("cnt_md"), {
    lineWrapping: !0,
    mode: "markdown",
    lineNumbers: !0,
    theme: "default",
    extraKeys: {Enter: "newlineAndIndentContinueMarkdownList"}
});
$("#form_reset").validate({
    rules: {user_email: {required: !0, email: !0}},
    messages: {
        user_email: {
            required: "<span class='red'>请输入正确电子邮箱</span>",
            email: "<span class='red'>请输入正确的电子邮箱</span>"
        }
    }
}), $("#sub_reset").click(function () {
    $("#form_reset").valid() ? js_update_pass() : alert("Error")
}), $("#searchForm").validate({
    rules: {searchheader: "required"},
    messages: {searchheader: "<span class='red'>Please enter keywords</span>"}
}), $("#act_collect").click(function () {


    $.ajax({
        url: "/collect/" + post_uid,
        type: "GET",
        cache: !1,
        data: {},
        dataType: "html",
        timeout: 1e3,
        error: function () {
            alert("请登陆后进行收藏！")
        },
        success: function (result) {
            $.parseJSON(result);
            $("#text_collect").text("成功收藏"), $("#text_collect").css("color", "red")
        }
    })
}), $(document).ready(function () {
    var AjaxUrl, baseMaps, cities, currentX, currentY, currentZoom, geojsonid, map, map_uid, mapson, nexrad, onMapClick, onZoomend, osm, overlayMaps, popup, vlat, vlon, vmarker, vzoom_current, vzoom_max, vzoom_min;
    if (currentZoom = 0, currentX = 0, currentY = 0, map_uid = "", $("#btn_updatemap").click(function () {
            $.ajax({
                url: "/admin_map/_update_view/m" + map_uid,
                type: "POST",
                cache: !1,
                data: {ext_lat: currentY, ext_lon: currentX, ext_zoom_current: currentZoom},
                dataType: "html",
                timeout: 1e3,
                error: function () {
                    alert("请登陆后进行收藏！")
                },
                success: function (result) {
                    $("#btn_updatemap").text("成功")
                }
            })
        }), $("#map").length > 0) {
        $("#map").hasClass("mapdiv") || $("#map").css({
            height: "350px",
            width: "92%"
        }), mapson = $("#map").data("map"), map_uid = mapson.i, vlon = mapson.x, vlat = mapson.y, vzoom_current = mapson.v, vzoom_max = mapson.m, vzoom_min = mapson.n, vmarker = mapson.k, geojsonid = mapson.g, $("#btn_overlay").click(function () {
            var sig_map_1, sig_map_2, url_new;
            return sig_map_1 = $("#over_map_1").val(), sig_map_2 = $("#over_map_2").val(), url_new = "/map/overlay/m" + map_uid + "/" + sig_map_1, "" !== sig_map_2 && (url_new = url_new + "/" + sig_map_2), window.location.href = url_new
        }), $("#save_view").click(function () {
            var view_url;
            return view_url = $("#current_view_url").attr("href").split("?")[1] + "&map=m" + map_uid, $.ajax({
                url: "/layout/save",
                type: "POST",
                cache: !1,
                data: view_url,
                dataType: "html",
                timeout: 1e3,
                error: function () {
                    return $("#current_view_url").text("请登陆后保存视图，或检查是否已经开始浏览地图！"), $("#current_view_url").css("color", "red")
                },
                success: function (result) {
                    return $("#current_view_url").text("视图已成功保存！")
                }
            })
        }), onMapClick = function (e) {
            var cmap_coor, div_str, link_str;
            return popup.setLatLng(e.latlng), popup.setContent("坐标位置" + e.latlng.toString()), currentZoom = map.getZoom(), cmap_coor = e.latlng, link_str = "http://www.osgeo.cn/map/m" + map_uid + "?zoom=" + currentZoom + "&lat=" + cmap_coor.lat.toFixed(4) + "&lon=" + cmap_coor.lng.toFixed(4) + "&marker=1", "" !== geojsonid && (link_str = link_str + "&geojson=" + geojsonid), div_str = '{"i" : "' + map_uid + '",  "x" : ' + cmap_coor.lng.toFixed(3).toString() + ', "y": ' + cmap_coor.lat.toFixed(3).toString() + ', "v":' + currentZoom.toString() + ', "m": ' + vzoom_max + ', "n": ' + vzoom_min + ', "g": "' + geojsonid + '", "k": 1}', div_str = '&lt;div id="map" data-map = \'' + div_str + "'&gt;&lt;/div&gt;", $("#current_view_url").html(link_str), $("#mapref").html(div_str), $("#current_view_url").attr("href", link_str), popup.openOn(map)
        }, onZoomend = function () {
            var cmap_coor, div_str, link_str;
            return currentZoom = map.getZoom(), cmap_coor = map.getCenter(), currentX = cmap_coor.lng.toFixed(3).toString(), currentY = cmap_coor.lat.toFixed(3).toString(), link_str = "http://www.osgeo.cn/map/m" + map_uid + "?zoom=" + currentZoom + "&lat=" + cmap_coor.lat.toFixed(4) + "&lon=" + cmap_coor.lng.toFixed(4), "" !== geojsonid && (link_str = link_str + "&geojson=" + geojsonid), div_str = '{"i" : "' + map_uid + '", "x" : ' + cmap_coor.lng.toFixed(3).toString() + ', "y": ' + cmap_coor.lat.toFixed(3).toString() + ', "v":' + currentZoom.toString() + ', "m": ' + vzoom_max + ', "n": ' + vzoom_min + ', "g": "' + geojsonid + '", "k": 0}', div_str = '&lt;div id="map" data-map = \'' + div_str + "'&gt;&lt;/div&gt;", $("#current_view_url").css("color", ""), $("#current_view_url").html(link_str), $("#mapref").html(div_str), $("#current_view_url").attr("href", link_str)
        }, popup = L.popup(), cities = new L.LayerGroup, new L.FeatureGroup, nexrad = L.tileLayer.wms("http://wcs.osgeo.cn:8088/service?", {
            layers: "maplet_" + map_uid,
            format: "image/png",
            transparent: !0,
            attribution: 'Map &copy; <a href="http://www.osgeo.cn/map/m' + map_uid + '">OSGeo China</a>'
        });
        var osm = L.tileLayer.chinaProvider("TianDiTu.Normal.Annotion", {
            maxZoom: 18,
            minZoom: 1
        }), osm1 = L.tileLayer.chinaProvider("TianDiTu.Normal.Map", {
            maxZoom: 18,
            minZoom: 1
        }), the_basemap = L.layerGroup([osm1, osm]);
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
        }), map.on("zoomend", onZoomend), map.on("moveend", onZoomend), map.on("click", onMapClick), baseMaps = {BaseMap: the_basemap}, overlayMaps = {"专题地图": nexrad}, L.control.layers(baseMaps, overlayMaps).addTo(map)
    }
});

