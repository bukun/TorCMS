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
      <q-toggle v-model="enableBigFile" label="开启大文件上传模式" />

      <div v-show="!enableBigFile" class="q-py-md">
        <q-file v-model="normalFile" label="请选择文件（普通上传）">
          <template v-slot:prepend>
            <q-icon name="attach_file" />
          </template>
          <template v-slot:after>
            <q-btn round dense flat icon="cloud_upload" @click="onSubmitClick" />
          </template>
        </q-file>
      </div>

      <div v-show="enableBigFile" class="q-py-md">
        <q-file v-model="bigFile" @input="bigFileAdded" label="请选择文件（大文件上传）">
          <template v-slot:prepend>
            <q-icon name="attach_file" />
          </template>
          <template v-slot:after>
            <q-btn round dense flat icon="cloud_upload" @click="onBigSubmitClick" />
          </template>
        </q-file>
      </div>

      <div v-if="fileInfo.url" class="q-py-md">
        <a target="_blank" :href="fileInfo.url">查看文件</a>
      </div>
<!--
      <div v-if="fileInfo.url" class="q-py-md">
        <q-img
          :src="fileInfo.url"
          spinner-color="white"
          style="height: 144px; width: 144px;border: 1px solid gray"
        />
      </div>

      <div v-if="fileInfo.url" class="q-py-md">
        <q-video
          :src="fileInfo.url"
          style="height: 256px; width: 144px; border: 1px solid gray"
        />
      </div> -->
  </div>
        <div>
          <q-btn label="Submit" type="submit" color="primary"></q-btn>
          <q-btn label="Reset" type="reset" color="primary" flat class="q-ml-sm"></q-btn>
        </div>
      </q-form>

    </div>
  </div>



</template>
<script>//dataList存储后台数据
import { fileService } from '../../../src/service';

export default {
   props: {
    value: {
      required: true
    }
  },
  data() {
    return {

      model: {},
      sub_options: [],
      sub2_options: [],
      pcatArr: [{guid: 'gcat0', puid: 'pcat0'}],
      pcatArr1: [{guid: 'gcat0', puid: 'pcat0'}, {guid: 'gcat1', puid: 'pcat1'}, {guid: 'gcat2', puid: 'pcat2'},
        {guid: 'gcat3', puid: 'pcat3'}, {guid: 'gcat4', puid: 'pcat4'}],

enableBigFile: false,
      normalFile: null,
      bigFile: null,
      chunkSize: 20971520, //20MB

      chunkInfo: {},
      fileInfo: {}
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

       init() {
      console.info('CFile->init');
      this.fileInfo.url = this.value;
    },

    async onSubmitClick() {
      console.info('CFile->onSubmitClick');

      if (!this.normalFile) {
        this.$q.notify({
          message: '请选择文件！',
          type: 'warning'
        });
        return;
      }

      this.$q.loading.show({
        message: '上传中'
      });

      try {
        let form = new FormData()
        form.append('file', this.normalFile);
        alert(this.normalFile)
        this.fileInfo = await fileService.upload(form, (e)=> {
          console.info(e);
        });
        this.$q.loading.hide();
        this.$emit('input', this.fileInfo);
      } catch (error) {
        this.$q.loading.hide();
        console.error(error);
      }
    },

    bigFileAdded(f) {
      console.info('CFile->fileAdded');

      if (!f) {
        console.info('CFile->cancel');
        return;
      }

      this.$q.loading.show({
        message: '文件准备中'
      });


    },

    getChunks() {
      const size = this.bigFile.size;
      const chunkSize = this.chunkSize;
      const chunks = Math.ceil( size / chunkSize);

      return chunks;
    },

    uploadWithBlock(chunk) {
      const size = this.bigFile.size;
      const chunkSize = this.chunkSize;
      const chunks = this.getChunks();

      const start = chunk * chunkSize;
      const end = ((start + chunkSize) >= size) ? size : start + chunkSize;

      //切割文件
      const chunkFile = this.bigFile.slice(start,end);

      let form = new FormData();
      form.append('file', chunkFile);
      form.append('name', this.bigFile.name);

      form.append('size', this.bigFile.size);
      form.append('chunks', chunks);
      form.append('chunk', chunk);

      return fileService.bigUpload(form, (e)=> {
        //console.info(e);
      });
    },

    checkFinished(datas) {
      for (let i = 0; i < datas.length; ++i) {
         let data = datas[i];
         if (data.isFinished) {
            console.info('CFile->checkFinished');
            this.fileInfo = data;
            this.$emit('input', this.fileInfo);
            this.$q.loading.hide();
         }
      }
    },

    async onBigSubmitClick() {
      console.info('CFile->onBigSubmitClick');

      if (!this.bigFile) {
        this.$q.notify({
          message: '请选择文件！',
          type: 'warning'
        });
        return;
      }


      this.$q.loading.show({
        message: '上传中'
      });

      try {
        let chunks = this.getChunks();

        let reqs = [];
        for (let i = 0; i < chunks; ++i) {
          reqs.push(this.uploadWithBlock(i));
        }

        await Promise.all(reqs)
        .then((datas) => {
          console.info(datas);
          this.checkFinished(datas);
        });
      } catch (error) {
        this.$q.loading.hide();
        console.error(error);
      }
    }




  }



};






</script>

