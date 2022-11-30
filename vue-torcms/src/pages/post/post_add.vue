<template>
  <div id="q-app">
    <div class="q-pa-md" style="max-width: 600px">
      <q-form
        @submit="onSubmit"
        @reset="onReset"
        class="q-gutter-md" method="post"
      >

        <q-input
          filled
          v-model="model.title"
          label="title"
          hint="title"
          lazy-rules
          :rules="[ val => val && val.length > 0 || 'Please type something']"
        ></q-input>
        <q-input
          filled
          v-model="model.tags"
          label="tags"
          hint="tags"

        ></q-input>

        <div class="row">
          <div class="col-8">

            <q-uploader label="上传" accept=".jpg,.png" @added="file_selected" url=""  auto-expand hide-upload-button/>
            <q-btn @click="uploadFile">Upload</q-btn>

          </div>
        </div>


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
          <q-btn label="Submit" type="submit" color="primary"></q-btn>
          <q-btn label="Reset" type="reset" color="primary" flat class="q-ml-sm"></q-btn>
        </div>
      </q-form>

    </div>
  </div>



</template>
<script>//dataList存储后台数据


export default {
  data() {
    return {
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
      files: null,
      uploadProgress: [],
      uploading: null,
    };
  },
  mounted() {

    this.get_sub();


  },
  methods: {
    onSubmit() {
      let formdata = {
        title: this.model.title,
        cnt_md: this.model.cnt_md,
        tags: this.model.tags,
        gcat0: this.model.gcat0,
        gcat1: this.model.gcat1,
        gcat2: this.model.gcat2,
        gcat3: this.model.gcat3,
        gcat4: this.model.gcat4,
        logo: '',
      }

      this.$axios({
        url: '/post_j/j_add',
        method: 'post',
        headers: {'Content-Type': 'application/json'},
        params: formdata
      })
        .then(async (statusCode) => {
          // alert(JSON.stringify(formdata))
          console.log(statusCode);
          // statusCode =JSON.stringify(statusCode)
          // alert(JSON.stringify(statusCode.data['code']))
          if (statusCode.data['code'] === '1') {
            this.$q.notify('Added successfully')
            this.$router.push({
              path: '/post/view',
              query: {
                uid: statusCode.data['uid']
              }
            });
            this.$q.loading.hide();

          } else {
            this.$q.notify(statusCode.data['info'])
          }
        })
        .catch(function (error) { // 请求失败处理
          this.$q.notify('failed')
          console.log('Error for res: ');
          this.$q.loading.hide();
          console.log(error);
        });


    },

    onReset() {
      this.model.title = null
      this.model.cnt_md = null
      this.model.tags = null
      this.model.logo = null
      this.model.pcat0 = null
      this.model.gcat0 = null
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
          // alert(JSON.stringify(response.data))
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

    file_selected(file) {
      alert(JSON.stringify(file[0]))
      this.selected_file = file[0];
      this.check_if_document_upload=true

    },

    uploadFile() {

      let formdata = {
        file: this.selected_file,
        kind: '1'

      }
      // alert(JSON.stringify(formdata))
      console.log(formdata)
      this.$axios({
        url: '/entity_j/img-upload',
        method: 'post',
        headers: {'Content-Type': 'application/json'},
        params: formdata
      })
        .then(async (statusCode) => {

          console.log(statusCode);
          // statusCode =JSON.stringify(statusCode)
          // alert(JSON.stringify(statusCode.data['code']))
          if (statusCode.data['path_save']) {
            this.$q.notify('Added successfully')
            this.model.logo = statusCode.data['path_save']
            this.$q.loading.hide();
            this.toolbar = false
          } else {
            this.$q.notify('Upload failed')
          }
        })
        .catch(function (error) { // 请求失败处理
          this.$q.notify('failed')
          console.log('Error for res: ');

        })


    },


    // uploadFile(file, updateProgress) {
    //   return new Promise((resolve, reject) => {
    //     resolve(file);
    //     console.log(resolve(file));
    //   });
    // }




  }



};






</script>

