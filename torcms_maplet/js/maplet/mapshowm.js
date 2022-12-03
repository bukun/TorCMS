(function () {
    var del_geojson, del_layout;
    del_layout = function (layout_id) {
        return $.ajax({
            url: "/layout/delete/" + layout_id,
            type: "GET",
            cache: false,
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
    };
    del_geojson = function (gson_id) {
        return $.ajax({
            url: "/geojson/delete/" + gson_id,
            type: "GET",
            cache: false,
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
    };
    $(document).ready(function () {
        var AjaxUrl, baseMaps, cities, currentX, currentY, currentZoom, drawnItems, geojsonid, map, map_uid, mapson, nexrad, onMapClick, onZoomend, osm, overlayMaps, popup, vlat, vlon, vmarker, vzoom_current, vzoom_max, vzoom_min;
        currentZoom = 0;
        currentX = 0;
        currentY = 0;
        map_uid = "";
        $("#btn_updatemap").click(function () {
            $.ajax({
                url: "/admin_map/_update_view/m" + map_uid,
                type: "POST",
                cache: false,
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
        });
        if ($("#map").length > 0) {
            if ($("#map").hasClass("mapdiv")) {
            } else {
                $("#map").css({height: "350px", width: "100%"})
            }
            mapson = $("#map").data("map");
            map_uid = mapson.i;
            vlon = mapson.x;
            vlat = mapson.y;
            vzoom_current = mapson.v;
            vzoom_max = mapson.m;
            vzoom_min = mapson.n;
            vmarker = mapson.k;
            geojsonid = mapson.g;
            $("#btn_overlay").click(function () {
                var sig_map_1, sig_map_2, url_new;
                sig_map_1 = $("#over_map_1").val();
                sig_map_2 = $("#over_map_2").val();
                url_new = "/map/overlay/m" + map_uid + "/" + sig_map_1;
                if (sig_map_2 !== "") {
                    url_new = url_new + "/" + sig_map_2
                }
                return window.location.href = url_new
            });
            $("#save_view").click(function () {
                var view_url;
                view_url = $("#current_view_url").attr("href").split("?")[1] + "&map=m" + map_uid;
                return $.ajax({
                    url: "/layout/save",
                    type: "POST",
                    cache: false,
                    data: view_url,
                    dataType: "html",
                    timeout: 1e3,
                    error: function () {
                        $("#current_view_url").text("请登陆后保存视图，或检查是否已经开始浏览地图！");
                        return $("#current_view_url").css("color", "red")
                    },
                    success: function (result) {
                        return $("#current_view_url").text("视图已成功保存！")
                    }
                })
            });
            onMapClick = function (e) {
                var cmap_coor, div_str, link_str;
                popup.setLatLng(e.latlng);
                popup.setContent("坐标位置" + e.latlng.toString());
                currentZoom = map.getZoom();
                cmap_coor = e.latlng;
                link_str = "http://www.osgeo.cn/map/m" + map_uid + "?zoom=" + currentZoom + "&lat=" + cmap_coor.lat.toFixed(4) + "&lon=" + cmap_coor.lng.toFixed(4) + "&marker=1";
                if (geojsonid !== "") {
                    link_str = link_str + "&geojson=" + geojsonid
                }
                div_str = '{"i" : "' + map_uid + '", ' + ' "x" : ' + cmap_coor.lng.toFixed(3).toString() + ', "y": ' + cmap_coor.lat.toFixed(3).toString() + ', "v":' + currentZoom.toString() + ', "m": ' + vzoom_max + ', "n": ' + vzoom_min + ', "g": "' + geojsonid + '"' + ', "k": 1' + "}";
                div_str = '&lt;div id="map" data-map = \'' + div_str + "'&gt;&lt;/div&gt;";
                $("#current_view_url").html(link_str);
                $("#mapref").html(div_str);
                $("#current_view_url").attr("href", link_str);
                return popup.openOn(map)
            };
            onZoomend = function () {
                var cmap_coor, div_str, link_str;
                currentZoom = map.getZoom();
                cmap_coor = map.getCenter();
                currentX = cmap_coor.lng.toFixed(3).toString();
                currentY = cmap_coor.lat.toFixed(3).toString();
                link_str = "http://www.osgeo.cn/map/m" + map_uid + "?zoom=" + currentZoom + "&lat=" + cmap_coor.lat.toFixed(4) + "&lon=" + cmap_coor.lng.toFixed(4);
                if (geojsonid !== "") {
                    link_str = link_str + "&geojson=" + geojsonid
                }
                div_str = '{"i" : "' + map_uid + '", ' + '"x" : ' + cmap_coor.lng.toFixed(3).toString() + ', "y": ' + cmap_coor.lat.toFixed(3).toString() + ', "v":' + currentZoom.toString() + ', "m": ' + vzoom_max + ', "n": ' + vzoom_min + ', "g": "' + geojsonid + '"' + ', "k": 0' + "}";
                div_str = '&lt;div id="map" data-map = \'' + div_str + "'&gt;&lt;/div&gt;";
                $("#current_view_url").css("color", "");
                $("#current_view_url").html(link_str);
                $("#mapref").html(div_str);
                return $("#current_view_url").attr("href", link_str)
            };
            popup = L.popup();
            cities = new L.LayerGroup;
            drawnItems = new L.FeatureGroup;
            nexrad = L.tileLayer.wms("https://tile.osgeo.cn/service?", {
                layers: "maplet_" + map_uid,
                format: "image/png",
                transparent: true,
                attribution: 'Map &copy; <a href="http://www.osgeo.cn/map/m' + map_uid + '">OSGeo China</a>'
            });
            osm = L.tileLayer.chinaProvider('Google.Satellite.Map', {
                maxZoom: 18,
                attribution: ' &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, ' + 'Imagery © <a href="http://mapbox.com">Mapbox</a>',
                id: "mapbox.streets"
            });
            nexrad.addTo(cities);
            osm.addTo(cities);
            map = L.map("map", {
                center: [vlat, vlon],
                zoom: vzoom_current,
                maxZoom: vzoom_max,
                minZoom: vzoom_min,
                layers: [cities]
            });
            if (vmarker.toString() === "1") {
                L.marker([vlat, vlon]).addTo(map)
            }
            AjaxUrl = "/geojson/gson/" + geojsonid;
            if (geojsonid !== "") {
                $.getJSON(AjaxUrl, function (gjson) {
                    var gson_arr;
                    gson_arr = new Array;
                    $.each(gjson, function (i, item) {
                        return gson_arr[i] = item
                    });
                    return L.geoJson(gson_arr).addTo(map)
                })
            }
            map.on("zoomend", onZoomend);
            map.on("moveend", onZoomend);
            map.on("click", onMapClick);
            baseMaps = {Basemap: osm};
            overlayMaps = {"专题地图": nexrad};
            return L.control.layers(baseMaps, overlayMaps).addTo(map)
        }
    })
}).call(this);
