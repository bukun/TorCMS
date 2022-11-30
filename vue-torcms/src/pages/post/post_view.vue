<template>

  <q-page padding>
    <h3> </h3>
    <div class="row justify-left ">
      <div class="col-sm-12 col-xs-12">

        <q-markup-table :separator="separator" flat bordered>

          <tr v-for="(item,index)  in this.info.data" :key="index">
            <td class="col-2 text-right">{{ index }}</td>
            <td>{{ item }}</td>

          </tr>

        </q-markup-table>
      </div>

    </div>
<!--    <div class="row">-->
<!--      <div class="q-pt-sm">-->
<!--        <br><br>-->
<!--        <q-btn color="primary" size="sm" label="Edit" @click="toEdit"></q-btn>-->

<!--      </div>-->
<!--    </div>-->
  </q-page>
</template>

<script>

export default {
  data() {
    return {
      info: '',

    };
  },
  mounted() {
    this.get_info()

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
            this.info = response

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
          uid: this.$route.query.uid
        }
      })
    }

  }


};
</script>

