(function () {
    $(document).ready(function () {
        var app_arr, app_url, baseMaps, ii, jj, lyrs, map, mycars, osm, overlayMaps, mp_uid;
        for (lyrs = new L.LayerGroup, mycars = new Array, app_url = $("#app_ctrl").val(), app_arr = app_url.split("/"), jj = 0; jj < app_arr.length;)

            if (app_arr[jj].substring(0, 1) == 'm') {

                mp_uid = "mp" + app_arr[jj].substring(1, 5);
                mycars[jj] = L.tileLayer.wms("https://tile.osgeo.cn/service?", {
                    layers: mp_uid,
                    format: "image/png",
                    transparent: !0,
                    attribution: "TorCMS"
                }), mycars[jj].addTo(lyrs), jj++;

            } else {

                mp_uid = "qn" + app_arr[jj].substring(1, 5);
                mycars[jj] = L.tileLayer.wms("https://tile.osgeo.cn/service?", {
                    layers: mp_uid,
                    format: "image/png",
                    transparent: !0,
                    attribution: "TorCMS"
                }), mycars[jj].addTo(lyrs), jj++;


            }

        var osm = L.tileLayer.chinaProvider("TianDiTu.Normal.Annotion", {maxZoom: 18, minZoom: 1}),
            osm1 = L.tileLayer.chinaProvider("TianDiTu.Normal.Map", {maxZoom: 18, minZoom: 1}),
            the_basemap = L.layerGroup([osm1, osm]);
        for (map = L.map("map", {
            center: [vlat, vlon],
            zoom: vzoom_current,
            maxZoom: vzoom_max,
            minZoom: vzoom_min,
            layers: [lyrs]
        }), the_basemap.addTo(map), baseMaps = {osm: the_basemap}, overlayMaps = {}, ii = 0; ii < app_arr.length;) overlayMaps[app_arr[ii]] = mycars[ii], ii++;
        return L.control.layers(baseMaps, overlayMaps).addTo(map)


    })
}).call(this);
