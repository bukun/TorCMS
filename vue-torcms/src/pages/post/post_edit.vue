<template>

  <q-page padding>
    <h3>Modify-{{this.info.title}}</h3>

    <div class="row justify-left">
      <q-card class="col-sm-6 col-xs-12">
        <q-card-section>
          <q-form @submit="onSubmit" class="q-gutter-md">

            <q-input filled v-model="model.title"
              label="标题"
              lazy-rules :rules="[ val => val && val.length > 0 || 'Please type something']"
            >{{this.info.title}}</q-input>
            <!--8101-->
            <div ref="css8101" style="display: none">
              <q-input filled v-model="model.tag_lsbzmj"
                       label="粮食播种面积（公顷）"
              >{{this.extinfo.tag_lsbzmj}}</q-input>
              <q-input filled v-model="model.tag_lszcl"
                       label="粮食总产量（吨）"
              >{{this.extinfo.tag_lszcl}}</q-input>
              <q-input filled v-model="model.tag_sdcl"
                       label="水稻播种面积（公顷）"
              >{{this.extinfo.tag_sdbzmj}}</q-input>
              <q-input filled v-model="model.tag_sdcl"
                       label="水稻产量（吨）"
              >{{this.extinfo.tag_sdcl}}</q-input>
              <q-input filled v-model="model.tag_ymbzmj"
                       label="玉米播种面积（公顷）"
              >{{this.extinfo.tag_ymbzmj}}</q-input>
              <q-input filled v-model="model.tag_ymcl"
                       label="玉米产量（吨）"
              >{{this.extinfo.tag_ymcl}}</q-input>
              <q-input filled v-model="model.tag_ddbzmj"
                       label="大豆播种面积（公顷）"
              >{{this.extinfo.tag_ddbzmj}}</q-input>
              <q-input filled v-model="model.tag_ddcl"
                       label="大豆产量（吨）"
              >{{this.extinfo.tag_ddcl}}</q-input>

            </div>

            <!-- 8102-->
            <div ref="css8102" style="display: none">
              <q-input filled v-model="model.tag_mlsbzmj"
                       label="马铃薯播种面积（公顷）"
              >{{this.extinfo.tag_mlsbzmj}}</q-input>
              <q-input filled v-model="model.tag_mlscl"
                       label="马铃薯产量（吨）"
              >{{this.extinfo.tag_mlscl}}</q-input>

            </div>

            <!--        8201,8301,8401-->
            <div ref="css_zhishu1" style="display: none">
              <q-input filled v-model="model.tag_sd"
                       label="水稻"
              >{{this.extinfo.tag_sd}}</q-input>
              <q-input filled v-model="model.tag_ym"
                       label="玉米"
              >{{this.extinfo.tag_ym}}</q-input>
              <q-input filled v-model="model.tag_dd"
                       label="大豆"
              >{{this.extinfo.tag_dd}}</q-input>

            </div>
            <!--        8202,8302,8402-->
            <div ref="css_zhishu2" style="display: none">
              <q-input filled v-model="model.tag_mls"
                       label="马铃薯"
              >{{this.extinfo.tag_mls}}</q-input>

            </div>


            <div>
              <q-btn label="Submit" type="submit" color="primary"/>

            </div>
          </q-form>
        </q-card-section>
      </q-card>
    </div>
  </q-page>
</template>

<script>


export default {
  data() {
    return {
      info:'',
      extinfo:'',
      file_model: {},
      selected_file: '',
      check_if_document_upload: false,
      toolbar: false,
      model: {},
      sub_options: [],
      sub2_options: [],
      pcatArr: [{guid: 'gcat0', puid: 'pcat0'}],
      pcatArr1: [{guid: 'gcat0', puid: 'pcat0'}, {guid: 'gcat1', puid: 'pcat1'}, {guid: 'gcat2', puid: 'pcat2'},
        {guid: 'gcat3', puid: 'pcat3'}, {guid: 'gcat4', puid: 'pcat4'}],
    };
  },
  mounted() {
    this.get_info()
    this.get_sub()
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
            // alert(JSON.stringify(response.data))
            this.info = response.data
            this.extinfo = response.data.extinfo
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
    onSubmit() {
      let formdata = {
        title: this.model.title,
        cnt_md: '',
        tags: '',
        logo: '',
        gcat0: this.extinfo.def_cat_uid,
      }
      // 8101
      if (this.extinfo.def_cat_uid === '8101' || this.extinfo.def_cat_uid === '8102') {

        formdata['tag_lsbzmj'] = this.model.tag_lsbzmj || this.extinfo.tag_lsbzmj,
          formdata['tag_lszcl'] = this.model.tag_lszcl || this.extinfo.tag_lszcl,
          formdata['tag_sdbzmj'] = this.model.tag_sdbzmj || this.extinfo.tag_sdbzmj,
          formdata['tag_sdcl'] = this.model.tag_sdcl || this.extinfo.tag_sdcl,
          formdata['tag_ymbzmj'] = this.model.tag_ymbzmj || this.extinfo.tag_ymbzmj,
          formdata['tag_ymcl'] = this.model.tag_ymcl || this.extinfo.tag_ymcl,
          formdata['tag_ddbzmj'] = this.model.tag_ddbzmj || this.extinfo.tag_ddbzmj,
          formdata['tag_ddcl'] = this.model.tag_ddcl || this.extinfo.tag_ddcl
      } else if (this.extinfo.def_cat_uid === '8102') {
        // 8102
        formdata['tag_mlsbzmj'] = this.model.tag_mlsbzmj || this.extinfo.tag_mlsbzmj,
          formdata['tag_mlscl'] = this.model.tag_mlscl || this.extinfo.tag_mlscl
      } else if (this.extinfo.def_cat_uid === '8201' || this.extinfo.def_cat_uid === '8301' || this.extinfo.def_cat_uid === '8401') {
        // 8201,8301,8401
        formdata['tag_sd'] = this.model.tag_sd || this.extinfo.tag_sd,
          formdata['tag_ym'] = this.model.tag_ym || this.extinfo.tag_ym,
          formdata['tag_dd'] = this.model.tag_dd || this.extinfo.tag_dd
      } else {
        // 8202,8302,8402
        formdata['tag_mls'] = this.model.tag_mls || this.extinfo.tag_mls
      }


      this.$axios({
        url: '/post_j/j_edit/' + this.$route.query.uid,
        method: 'post',
        headers: {'Content-Type': 'application/json'},
        params: formdata
      })
        .then(async (statusCode) => {
          console.log(statusCode);
          // alert(JSON.stringify(statusCode.data))

          if (statusCode.data['code'] === '1') {
            this.$q.notify('Modified successfully')
            this.$router.push({
              path: '/post/view',
              query: {
                uid: this.$route.query.uid,
                city:this.extinfo.tag_city
              }
            });
            this.$q.loading.hide();
          } else {
            this.$q.notify('Modified failed')
          }
        })
        .catch(function (error) { // 请求失败处理
          this.$q.notify('Modified failed')
          console.log('Error for res: ');
          this.$q.loading.hide();
          console.log(error);
        });
    },
    get_sub() {

      this.$axios({
        url: '/list/j_kindcat/1',
        method: 'get',
        headers: {'Content-Type': 'application/json'}

      }).then(response => {

          console.log(response);
          for (let i in response.data) {
            this.sub_options.push({'id': i, 'desc': response.data[i]})

          }


        }
      )
        .catch(function (error) { // 请求失败处理
          console.log('Error for info2: ');
          console.log(error);
        });
    },
    changeSub(id) {

      this.$axios({
        url: '/list/j_subcat/' + id,
        method: 'get',
        headers: {'Content-Type': 'application/json'}

      }).then(response => {

          console.log(response);
          this.sub2_options = []
          for (let i in response.data) {
            this.sub2_options.push({'id': i, 'desc': response.data[i]})

          }


        }
      )
        .catch(function (error) { // 请求失败处理
          console.log('Error for info2: ');
          console.log(error);
        });
    },

  }
};
</script>

