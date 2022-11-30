<template>

  <q-page padding>
    <h3>  {{this.info.title}}</h3>
    <div class="row ">
      <div class="col-sm-9 col-xs-12">

        <div ref="map_vkz" style=" width: 100%;
    height: 80vh;
    z-index: 1;
    /*padding: .2rem;*/
    /*margin: 5px;*/
    position: absolute">

        </div>
      </div>
      <div class="col-sm-3 col-xs-12 " style="padding-left: 20px">
        <p>{{this.info.cnt_md}}</p>

<!--        8101-->
      <div ref="css8101" style="display: none">
        <p>粮食播种面积（公顷）：{{this.extinfo.tag_lsbzmj}}</p>
        <p>粮食总产量（吨）：{{this.extinfo.tag_lszcl}}</p>
        <p>水稻产量（吨）：{{this.extinfo.tag_sdcl}}</p>
        <p>玉米播种面积（公顷）：{{this.extinfo.tag_ymbzmj}}</p>
        <p>玉米产量（吨）：{{this.extinfo.tag_ymcl}}</p>
        <p>大豆播种面积（公顷）：{{this.extinfo.tag_ddbzmj}}</p>
        <p>大豆产量（吨）：{{this.extinfo.tag_ddcl}}</p>
      </div>
        <!--        8102-->
        <div ref="css8102" style="display: none">
        <p>马铃薯播种面积（公顷）：{{this.extinfo.tag_mlsbzmj}}</p>
        <p>马铃薯产量（吨）：{{this.extinfo.tag_mlscl}}</p>
</div>

<!--        8201,8301,8401-->
        <div ref="css_zhishu1" style="display: none">
        <p>水稻：{{this.extinfo.tag_sd}}</p>
        <p>玉米：{{this.extinfo.tag_ym}}</p>
        <p>大豆：{{this.extinfo.tag_dd}}</p>
        </div>
        <!--        8202,8302,8402-->
        <div ref="css_zhishu2" style="display: none">
        <p>马铃薯：{{this.extinfo.tag_mls}}</p>
        </div>
        <div class="row">
          <div class="q-pt-sm">
            <br><br>
            <q-btn color="primary" size="sm" label="Edit" @click="toEdit"></q-btn>

          </div>
        </div>
      </div>


    </div>

  </q-page>
</template>

<script>
import L from 'leaflet';
import '../../css/leaflet.css';
import statesData from '../gson_china.js'
export default {
  data() {
    return {
      info: '',
      extinfo: '',
      city:this.$route.query.city || '',
      statesData:statesData,
      map: undefined,
      popup: undefined,

    };
  },
  mounted() {

    this.init_leaf();
    this.get_info();
  },
  methods: {

    get_info() {
      this.$axios({
        url: '/post_j/j_view',
        method: 'post',
        headers: {'Content-Type': 'application/json'},
        params: {uid: this.$route.query.uid}
      }).then(response => {

          console.log(response);
          // alert(JSON.stringify(response.data))
          if (response.data.code === '1') {
            this.info = response.data
            this.extinfo = response.data.extinfo
            this.city=response.data.extinfo['tag_city']

            if(this.extinfo.def_cat_uid ==='8101'){

             this.$refs.css8101.style.setProperty('display','block')
            }
          else if(this.extinfo.def_cat_uid ==='8102'){
              this.$refs.css8101.style.setProperty('display','block')
             this.$refs.css8102.style.setProperty('display','block')
            }
            else{
             if(this.extinfo.def_cat_uid ==='8201'|| this.extinfo.def_cat_uid ==='8301' || this.extinfo.def_cat_uid ==='8401'){

                this.$refs.css_zhishu1.style.setProperty('display','block')

              }else{

               this.$refs.css_zhishu1.style.setProperty('display','block')
               this.$refs.css_zhishu2.style.setProperty('display','block')

             }
            }


          } else {
            this.$q.notify('falied')
            this.$router.push('/')
          }

        }
      )
        .catch(function (error) { // 请求失败处理
          console.log('Error for info2: ');
          console.log(error);
        });
    },
    toEdit() {
      this.$router.push({
        path: '/post/edit',
        query: {
          uid: this.$route.query.uid,
          catid: this.$route.query.catid
        }
      })
    },
    init_leaf() {
      //创建地图
      this.map = L.map(this.$refs.map_vkz, {
        center: [43.85, 126.1],
        crs: L.CRS.EPSG3857,
        zoom: 6.5,
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
    onEachstates(feature, layer) {
      if(feature.properties.Name === this.city){

        layer.bindTooltip('<div><b>' + feature.properties.Name + '</b></div>',
          {
            permanent: true
          });



    }
      layer.bindPopup(

        '<b>' + feature.properties.Name + '</b>',{
          closeButton: false
        }
      )
      },


  }


};
</script>

