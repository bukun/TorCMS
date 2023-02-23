<template>

  <q-page padding>
    <h3> {{ this.info.title }}</h3>
    <div class="row ">

    <div class="col-sm-12 col-xs-12 " style="padding-left: 20px">
      <p>{{ this.info.time_create }}</p>
      <p>{{ this.info.cnt_md }}</p>


      <div class="row">
        <div class="q-pt-sm" ref="show_edit" style="display: none">
          <br><br>

          <q-btn color="purple" size="sm" label="Edit" @click="toEdit()"></q-btn>

        </div>
      </div>


    </div>
    </div>
  </q-page>
</template>

<script>

import '../../css/leaflet.css';
import statesData from '../gson_china.js'
import {authService} from "../../service";

export default {
  data() {
    return {
      info: '',
      extinfo: '',
      city: this.$route.query.city || '',
      statesData: statesData,
      map: undefined,
      popup: undefined,

    };
  },
  mounted() {

    this.get_info();

    this.check_login();


  },
  methods: {
    check_login() {
      if (authService.getToken()) {
        this.$refs.show_edit.style.setProperty('display', 'block')
      } else {
        this.$refs.show_edit.style.setProperty('display', 'none')
      }
    },
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


  }


};
</script>

