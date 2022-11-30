<template>
  <q-page class="row items-center justify-evenly">

    <div ref="map_vkz" style=" width: 100%;
    height: 100vh;
    z-index: 1;
    /*padding: .2rem;*/
    /*margin: 5px;*/
    position: absolute">

    </div>


  </q-page>
</template>

<script>
import L from 'leaflet';
import '../css/leaflet.css';
import statesData from './gson_china.js'
import jsondata from './data.json'
export default {
  data() {
    return {
      info: '',
      statesData:statesData,
      map: undefined,
      popup: undefined,
      showdata:jsondata

    };
  },
  mounted() {

    this.init_leaf();


  },
  methods: {
    init_leaf() {
      //创建地图

      this.map = L.map(this.$refs.map_vkz, {
        center: [43.85, 126.1],
        crs: L.CRS.EPSG3857,
        zoom: 7,
        maxZoom: 18,
        editable: true,
        // 去除放大缩小控件
        // https://stackoverflow.com/questions/16537326/leafletjs-how-to-remove-the-zoom-control
        zoomControl: false,
        layerControl: false,
        attributionControl: false,
      });
      this.popup = L.popup();


      // 天地图地图及标示  osm，osm1.
      this.osm = L.tileLayer('http://t{s}.tianditu.gov.cn/DataServer?T=vec_w&X={x}&Y={y}&L={z}&tk=57f1b8146ef867f14189f3f4bb1adc1c', {
        subdomains: ['0', '1', '2', '3', '4', '5', '6', '7'],
        title: '天地图网格图',
        maxZoom: 18,
        id: 'mapbox.streets'
      });
      this.osm1 = L.tileLayer('http://t{s}.tianditu.gov.cn/DataServer?T=cia_w&X={x}&Y={y}&L={z}&tk=57f1b8146ef867f14189f3f4bb1adc1c', {
        subdomains: ['0', '1', '2', '3', '4', '5', '6', '7'],
        title: '天地图中文标注',
        maxZoom: 18,
        id: 'mapbox.streets'
      });
      this.osm.addTo(this.map)
      this.osm1.addTo(this.map)

      this.states= L.geoJson(this.statesData, {
          style: this.style_fushqv,
          onEachFeature: this.onEachstates
        }
      ).addTo(this.map)


    },
    onEachstates: function (feature, layer) {
      // alert(this.showdata)



      layer.bindTooltip('<div><b>' + feature.properties.Name + '</b></div>',
        {
          permanent: true,
        });
      for(var x in this.showdata){

        if (this.showdata[x].city ===feature.properties.Name ){
          var datahtml = ''
          var datas = ''
          for(var info in this.showdata[x].data){

            datahtml = '<b>' + this.showdata[x].data[info].title + '</b><p>'+JSON.stringify(this.showdata[x].data[info].extinfo)+'</p>'
            datas =datas + datahtml
          }

        layer.bindPopup(
          '<b>' + feature.properties.Name + '</b><br>'+datas ,{
            closeButton: false
          }
        )
        }
      }

    },
  }


};
</script>
