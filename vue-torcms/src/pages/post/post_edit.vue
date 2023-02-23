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



            <q-input
          filled
          v-model="model.tags"
          label="tags"
          hint="tags"

        ></q-input>
            <div v-for="(parItem,index) in pcatArr" :key="index" class="row">
          <div class="col-5">


            <q-select
              filled
              v-model="parItem.puid"
              label="Select category"
              :options="sub_options"
              option-value="id"
              option-label="desc"
              hint="Select category"
              emit-value
              map-options
              @update:model-value="changeSub"


            />
          </div>
          <div class="col-1"></div>
          <div class="col-6">


            <q-select
              filled
              v-model="model.gcat0"
              :options="sub2_options"
              :option-value="opt => Object(opt) === opt && 'id' in opt ? opt.id : null"
              :option-label="opt => Object(opt) === opt && 'desc' in opt ? opt.desc : '- Null -'"
              :option-disable="opt => Object(opt) === opt ? opt.inactive === true : true"
              emit-value
              map-options
              hint="Secondary classification"
              label="Secondary classification"
            />

          </div>
        </div>


        <q-input
          filled
          v-model="model.cnt_md"
          label="content"
          hint="content"
          type="textarea"

        ></q-input>




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
        cnt_md: this.model.cnt_md,
        tags: this.model.tags,
        logo: '',
        gcat0: this.model.gcat0,
      }
      // 8101



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

