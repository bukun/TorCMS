<template>
  <div id="center_fz8">

    <div ref="map_vkz" style=" width: 84%;
    height: 95vh;
    z-index: 1;
    position: absolute">

    </div>

  </div>

</template>

<script>
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

export default {
// name: 'Test',
  mounted() {

    this.init_leaf();
  },

  data() {
    return {
      config: {},
      info_map_center: undefined,
      info_map_zoom: undefined,
      info_mouse_pos: undefined,

      map: undefined,
      popup: undefined,
    }
  },
  components: {},
  methods: {
    test_fun2: function () {


      this.info_map_center = this.map.getCenter();
      this.info_map_zoom = this.map.getZoom();

    },
    test_fun3: function (e) {


      this.info_mouse_pos = e.latlng;
      this.info_map_zoom = this.map.getZoom();

    },
    onMapClick(e) {
      this.popup
        .setLatLng(e.latlng)
        .setContent('Location:' + e.latlng.toString())
        .openOn(this.map);
    },
    init_leaf() {
      //创建地图
      this.map = L.map(this.$refs.map_vkz, {
        center: [47.15, 125.1],
        crs: L.CRS.EPSG3857,
        zoom: 6,
        maxZoom: 18,
        editable: true,
        // 去除放大缩小控件
        // https://stackoverflow.com/questions/16537326/leafletjs-how-to-remove-the-zoom-control
        zoomControl: false,
        layerControl: false,
        attributionControl: false,
        // Attribution: false,
      });
      this.popup = L.popup();
      this.map.on('click', this.onMapClick);
      this.map.on('move', this.test_fun2);
      this.map.on('mousemove', this.test_fun3);


      // 天地图地图及标示  osm，osm1.
      this.osm = L.tileLayer('http://t4.tianditu.gov.cn/DataServer?T=vec_w&X={x}&Y={y}&L={z}&tk=57f1b8146ef867f14189f3f4bb1adc1c', {
        title: '天地图网格图',
        maxZoom: 18,
        id: 'mapbox.streets'
      });
      this.osm1 = L.tileLayer('http://t4.tianditu.gov.cn/DataServer?T=cia_w&X={x}&Y={y}&L={z}&tk=57f1b8146ef867f14189f3f4bb1adc1c', {
        title: '天地图中文标注',
        maxZoom: 18,
        id: 'mapbox.streets'
      });

      this.osm2 = L.tileLayer('http://t4.tianditu.gov.cn/DataServer?T=img_w&X={x}&Y={y}&L={z}&tk=57f1b8146ef867f14189f3f4bb1adc1c', {
        title: '影像',
        maxZoom: 18,
        id: 'mapbox.streets'
      });

      this.grp_tdt = new L.LayerGroup();
      this.osm2.addTo(this.grp_tdt);
      this.osm1.addTo(this.grp_tdt);

      this.grp_tdt.addTo(this.map);


      this.greenIcon = {
        radius: 5,
        color: '#000000',
        opacity: 1,
        fillColor: '#666666',
        fillOpacity: 1,
      };



      this.baseMaps = {
        '影像': this.osm2,
        // '天地图': this.osm,
        // '示范区底图': this.l27,

      };


      this.base_geography = L.tileLayer.wms('http://47.94.22.90:9012/service?', {
        layers: 'q_ht_boundary_boundary_mn0005',
        format: 'image/png',
        transparent: true,
        backgroundColor: '#0f0f0f',
      }).addTo(this.map);

      L.control.scale({
        position: 'bottomright',
        maxWidth: '100',
        imperial: false
      }).addTo(this.map);

    },

  }
}
</script>

<style lang="scss" scoped>


#center_fz8 {
  height: 95vh;

  .btn {
    &.activity {
      background: #7B68EE;
      border: #8A71AB 1px solid;
      color: #fff;
    }
  }

  input[type=checkbox].switch {
    margin-right: 5px;
    outline: none;
    appearance: none;
    -webkit-appearance: none;
    -moz-appearance: none;
    position: relative;
    width: 30px;
    height: 15px;
    border-radius: 15px;
    border: 1px solid #ccc;
    background-color: #ccc;
    top: 2px
  }

  input[type=checkbox].switch::after {
    content: '';
    display: inline-block;
    width: 15px;
    height: 14px;
    border-radius: 50%;
    background-color: #fff;
    box-shadow: 0 0 2px #999;
    transition: left 0.1s linear;
    position: absolute;
    top: 0;
    left: 0;
  }

  input[type=checkbox].switch:checked {
    background-color: #1ab394;
  }

  input[type=checkbox].switch:checked::after {
    position: absolute;
    top: 0;
    left: 50%;
  }


  .li_icon_yi {
    width: 100%;
    color: #fff;
    list-style: none;
  }

  .li_icon_yi:hover {
    cursor: pointer;
    color: #5cd9e8;
  }


  .text {
    color: #c3cbde;
  }

  .leaflet-popup-tip-container {
    background-color: rgba(255, 0, 0, 0.0);
    display: none;
  }

  .btn-sm {
    padding: 2px;
  }

  form {
    margin: .1rem;
    margin-top: .3rem;
    font-size: .18rem;
  }

  fieldset {

    label {
      font-size: 14px;
      margin: 10px 0;
      display: flex;

    }

    ul li {
      font-size: 14px;
    }
  }

  .icon_tab {
    margin-left: 15px;
  }

  .fonsize {
    font-size: 14px;
    color: #fff;
  }
}
</style>
