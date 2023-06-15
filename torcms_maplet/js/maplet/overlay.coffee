$(document).ready ->
  lyrs = new L.LayerGroup()
  mycars = new Array()
  app_url = $("#app_ctrl").val()
  app_arr = app_url.split("/")
  # wcs = "121.42.29.253"
  jj = 0

  while jj < app_arr.length
    mycars[jj] = L.tileLayer.wms("https://tile.osgeo.cn/service?",
      layers: "mp" + app_arr[jj].substring(1)
      format: "image/png"
      transparent: true
      attribution: "Maplet"
    )
    mycars[jj].addTo lyrs
    jj++
  osm = L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoiYnVrdW4iLCJhIjoiY2lqeWFjZmo4MXFubndka2lzcnZ1M2tzciJ9.C1dZUQkRZSIEKfg-DaFYpw",
    maxZoom: 18
    attribution: "Map data &copy; <a href=\"http://openstreetmap.org\">OpenStreetMap</a> contributors, " + "<a href=\"http://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, " + "Imagery © <a href=\"http://mapbox.com\">Mapbox</a>"
    id: "mapbox.satellite"
  )
  osm.addTo lyrs
  map = L.map("map",
    center: [ vlat, vlon ]
    zoom: vzoom_current
    maxZoom: vzoom_max
    minZoom: vzoom_min
    layers: [ lyrs ]
  )
  baseMaps = osm: osm
  overlayMaps = {}
  ii = 0

  while ii < app_arr.length
    overlayMaps[app_arr[ii]] = mycars[ii]
    ii++
  L.control.layers(baseMaps, overlayMaps).addTo map
