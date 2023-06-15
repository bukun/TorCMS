$(document).ready ->

# 用户登录的时候，逐个添加
#  onZoomend = ->
#    currentZoom = map.getZoom()
#    cmap_coor = map.getCenter()
#    link_str = "https://www.osgeo.cn/map/" + map_uid + "?zoom=" + currentZoom + "&lat=" + cmap_coor.lat.toFixed(4) + "&lon=" + cmap_coor.lng.toFixed(4)
#    link_str = link_str + "&geojson=" + geojsonid  unless geojsonid is ""
#    $("#current_view_url").css "color", ""
#    $("#current_view_url").html link_str
#    $("#current_view_url").attr "href", link_str

# 选项为 editable的,

# 此处为视图可见

# var tt = L.geoJson.geometrytolayer;

# 用户登录的时候，逐个添加

#                        var myGeoJson = L.geoJson(item, {
#                                    onEachFeature: function (feature, layer) {
#                                        layer.on('click', function (e) {
#                                            e.target.enableEdit();
#                                        });
#                                    }
#                                }
#                        );

# 下面代码可以实现编辑属性的功能，但是会导致双击失效。
#                        var myGeoJson = L.geoJson(item,
#                                {
#                                    onEachFeature: function (feature, layer) {
#                                        var input = L.DomUtil.create('input', 'my-input');
#                                        input.value = feature.properties.name;
#                                        L.DomEvent.addListener(input, 'change', function () {
#                                            feature.properties.name = input.value;
#
#                                        });
#                                        layer.bindPopup(input);
#                                    }
#                                }
#                        );
  show_saved_info = ->
    $("#infor").css "color", "#ff0"
    $("#infor").text "用户数据已经成功保存！"
    setTimeout "$('#infor').text('');", 8000
  save_data = ->
    shape = drawnItems.toGeoJSON()
    map.doubleClickZoom.enable()
    $.ajax
      type: "POST"
      url: "/geojson/" + geojsonid
      data:
        geojson: JSON.stringify(shape)

      dataType: "html"
      timeout: 2000
      error: ->
        alert "请登陆后进行数据保存！或再次尝试进行保存！"

      success: (result) ->
        geo = $.parseJSON(result)
        if geo["status"] is 0
          alert "请检查是否拥有数据权限！"
        else
          show_saved_info()
          location.href = "/geojson/" + geo["sig"]  unless geo["sig"] is ""

  $("#btn_add_maplet").click ->
    hdata = $("#maplet_id").val()

    nexrad2 = L.tileLayer.wms("https://tile.osgeo.cn/service?",
      layers: "mp" + hdata
      format: "image/png"
      transparent: true
      attribution: "Maplet2"
    )


    map.addLayer nexrad2

    lcontrol.addOverlay(nexrad2, hdata);


  # map.removeLayer(nexrad2)
  # lcontrol.removeLayer(nexrad2)

  $("#load_geojson").click ->
    hdata = $("#hdata").val()
    gson_arr = new Array()
    gdata = $.parseJSON(hdata)["features"]
    $.each gdata, (i, item) ->
      gson_arr[i] = item
      if login is 1
        myGeoJson = L.geoJson(item)
        myGeoJson.addTo drawnItems

    L.geoJson(gson_arr).addTo drawnItems  if login is 0
    $("#hdata").val ""
    $("#infor").css "color", "#ff0"
    $("#infor").text "已经加载GeoJson数据！"
    setTimeout "$('#infor').text('');", 8000

  cities = new L.LayerGroup()
  drawnItems = new L.FeatureGroup()
  # wcs = "121.42.29.253"
  #  nexrad = L.tileLayer.wms("https://tile.osgeo.cn/service?",
  #    layers: "mp" + map_uid
  #    format: "image/png"
  #    transparent: true
  #    attribution: "Maplet"
  #  )
  osm = L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoiYnVrdW4iLCJhIjoiY2lqeWFjZmo4MXFubndka2lzcnZ1M2tzciJ9.C1dZUQkRZSIEKfg-DaFYpw",
    maxZoom: 18
    attribution: "Map data &copy; <a href=\"http://openstreetmap.org\">OpenStreetMap</a> contributors, " + "<a href=\"http://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, " + "Imagery © <a href=\"http://mapbox.com\">Mapbox</a>"
    id: "mapbox.satellite"
  )

  satellite_layer = L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoiYnVrdW4iLCJhIjoiY2lqeWFjZmo4MXFubndka2lzcnZ1M2tzciJ9.C1dZUQkRZSIEKfg-DaFYpw",
    maxZoom: 18
    attribution: "Map data &copy; <a href=\"http://openstreetmap.org\">OpenStreetMap</a> contributors, " + "<a href=\"http://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, " + "Imagery © <a href=\"http://mapbox.com\">Mapbox</a>"
    id: "mapbox.satellite"
  )


  # nexrad.addTo cities
  osm.addTo cities
  map = L.map("map",
    center: [vlat, vlon]
    zoom: vzoom_current
    maxZoom: vzoom_max
    minZoom: vzoom_min
    layers: [osm]
    editable: true
    editOptions:
      featuresLayer: drawnItems
  )
  #  map.addLayer nexrad
  map.addLayer drawnItems
  AjaxUrl = "/geojson/gson/" + geojsonid
  unless geojsonid is ""
    $.getJSON AjaxUrl, (gjson) ->
      gson_arr = new Array()
      $.each gjson, (i, item) ->
        gson_arr[i] = item
        if login is 1
          myGeoJson = L.geoJson(item)
          myGeoJson.addTo drawnItems

          

      L.geoJson(gson_arr).addTo drawnItems  if login is 0

  #  //Initialize the StyleEditor
  styleEditor = L.control.styleEditor(
        position: "topleft"
  )

  map.addControl styleEditor

  L.EditControl = L.Control.extend(
    options:
      position: "topleft"
      callback: null
      kind: ""
      html: ""

    onAdd: (map) ->
      container = L.DomUtil.create("div", "leaflet-control leaflet-bar")
      link = L.DomUtil.create("a", "", container)
      link.href = "#"
      link.title = @options.kind
      link.innerHTML = @options.html
      L.DomEvent.on(link, "click", L.DomEvent.stop).on link, "click", (->
        window.LAYER = @options.callback.call(map.editTools)
        map.doubleClickZoom.disable()
        map.dragging.disable()
      ), this
      container
  )
  L.EditSaveControl = L.EditControl.extend(options:
    position: "topleft"
    callback: save_data
    kind: "保存编辑"
    html: "<span class=\"glyphicon glyphicon-save\"></span>"
  )
  L.NewLineControl = L.EditControl.extend(options:
    position: "topleft"
    callback: map.editTools.startPolyline
    kind: "线"
    html: "\\/\\"
  )
  L.NewPolygonControl = L.EditControl.extend(options:
    position: "topleft"
    callback: map.editTools.startPolygon
    kind: "多边形"
    html: "▰"
  )
  L.NewMarkerControl = L.EditControl.extend(options:
    position: "topleft"
    callback: map.editTools.startMarker
    kind: "点标注"
    html: "<span class=\"glyphicon glyphicon-map-marker\"></span>"
  )
  L.NewRectangleControl = L.EditControl.extend(options:
    position: "topleft"
    callback: map.editTools.startRectangle
    kind: "矩形"
    html: "⬛"
  )
  L.NewCircleControl = L.EditControl.extend(options:
    position: "topleft"
    callback: map.editTools.startCircle
    kind: "circle"
    html: "⬤"
  )
  map.addControl new L.EditSaveControl()
  map.addControl new L.NewMarkerControl()
  map.addControl new L.NewLineControl()
  map.addControl new L.NewPolygonControl()
  map.addControl new L.NewRectangleControl()
  # map.addControl(new L.NewCircleControl());

  if login is 1
    Z = 90
    latlng = undefined
    redoBuffer = []
    onKeyDown = (e) ->
      if e.keyCode is Z
        return  unless @editTools._drawingEditor
        if e.shiftKey
          @editTools._drawingEditor.push redoBuffer.pop()  if redoBuffer.length
        else
          latlng = @editTools._drawingEditor.pop()
          redoBuffer.push latlng  if latlng
      else if e.keyCode is 69
        if map.dragging.enabled()
          map.dragging.disable()
        else
          map.dragging.enable()

    L.DomEvent.addListener document, "keydown", onKeyDown, map
    map.on "editable:drawing:end", ->
      redoBuffer = []

  deleteShape = (e) ->

# Ctrl + 点击删除数据。好像有问题。
    @editor.deleteShapeAt e.latlng  if (e.originalEvent.ctrlKey or e.originalEvent.metaKey) and @editEnabled()

  map.on "layeradd", (e) ->
    e.layer.on("click", L.DomEvent.stop).on "click", deleteShape, e.layer  if e.layer instanceof L.Path
    e.layer.on("dblclick",
      L.DomEvent.stop).on "dblclick", e.layer.toggleEdit  if (e.layer instanceof L.Path) or (e.layer instanceof L.Marker)

  map.on "editable:vertex:ctrlclick editable:vertex:metakeyclick", (e) ->
    index = e.vertex.getIndex()
    if index is 0
      e.layer.editor.continueBackward e.vertex.latlngs
    else e.layer.editor.continueForward e.vertex.latlngs  if index is e.vertex.getLastIndex()

  # map.on "zoomend", onZoomend
  # map.on "moveend", onZoomend
  map.on "editable:editing", (e) ->
    map.dragging.disable()
    map.doubleClickZoom.disable()

    # e.layer.setStyle({color: 'DarkRed'});

    # Marker 会出错
    e.layer.setStyle color: "Red"  if e.layer instanceof L.Path

  map.on "editable:disable", (e) ->
    map.doubleClickZoom.enable()
    map.dragging.enable()

  baseMaps = "MapBox底图": osm , "卫星影像": satellite_layer
  #  overlayMaps = "专题地图": nexrad

  # info = L.control()
  # baseMaps.addTo info.layer
  # info.layers(baseMaps, overlayMaps).addTo map
  # info.addTo map
  lcontrol = L.control.layers(baseMaps, null).addTo map
# lcontrol.removeFrom map
