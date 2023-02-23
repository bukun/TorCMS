<template>
  <q-page padding>
    <h3>
      {{ this.pagetitle }}
    </h3>
    <div class="row justify-left ">
      <div class="col-sm-12 col-xs-12">
        <q-markup-table :separator="separator" flat bordered>
          <tbody>
          <tr v-for="(item,index)  in this.info.recs" :key="index">
            <td> {{ index + this.pagination.offset * this.pagination.limit - this.pagination.limit + 1 }}</td>
            <td><a @click="tolink(item.uid,item.city)" class="text-primary ">{{ item.title }}</a></td>
            <td>{{ item.cnt_md }}</td>
          </tr>
          </tbody>
        </q-markup-table>
      </div>
    </div>
    <div class="row q-my-md fs-14">
      <span class="self-center col-auto q-pb-sm q-mt-md q-mr-md">共{{ this.info.count }}条，第{{ this.pagination.offset }} /{{ this.info.maxpage }}页</span>
      <q-select
        class="col-auto self-center q-mr-md q-mt-md"
        style="width: 90px"
        v-model="perPageNum"
        :options="perPageNumOptions"
      />
      <q-pagination class="col q-mt-md" v-model="page" :max=this.info.maxpage size="sm" boundary-links boundary-numbers
                    :max-pages="10" direction-links ellipses/>
    </div>
  </q-page>
</template>

<script>
export default {
  data() {
    return {
      info: '',
      catid:this.$route.params.catid || '',
      pid:this.$route.params.pid || '',
      pagetitle:'列表',
      pagination: {
        offset: 1,
        limit: 10
      },
      perPageNumOptions: [
        {
          label: '每页10条',
          value: 10
        },
        {
          label: '每页20条',
          value: 20
        },
        {
          label: '每页50条',
          value: 50
        },
        {
          label: '每页100条',
          value: 100
        }
      ],
      pageChangeFlag: false


    };
  },

  mounted() {
    this.init()
    this.get_info();
  },
  async beforeRouteUpdate (to, from, next) {
    console.info('beforeRouteUpdate');
    await this.init(to.params.pid);
    next();

  },
  methods: {
    async init(pid) {

      this.catid = this.$route.params.catid;
      this.pid = pid || this.$route.params.pid;
      if(this.pid ==='0100'){
        this.pagetitle = 'Technology'
      }
      else if(this.pid ==='0200'){
        this.pagetitle = 'Education'
      }

      else {
        this.pagetitle='列表'
      }
      this.get_info()

    },

    get_info() {
      console.log(this.catid)
      console.log(this.pid)
      this.$axios({
        url: '/post_j/j_recent',
        method: 'post',
        headers: {'Content-Type': 'application/json'},
        params: {kind: '1', catid: this.catid,pid:this.pid, offset: this.pagination.offset, limit: this.pagination.limit}

      }).then(response => {
          console.log(response);
          if (response.data.code === '1') {
            this.info = response.data
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
    tolink(uid,city) {

      this.$router.push({
        path: '/post/view',
        query: {
          uid: uid,
          city:city,
          catid:this.$route.params.catid
        }
      })
    },


  },

  watch: {
    // 每页显示数量改变即触发事件
    'pagination.limit': function () {
      if (!this.pageChangeFlag) {
        this.$emit('pageChange', this.pagination.limit, this.pagination.offset)
      } else {
        this.pageChangeFlag = false
      }
    },
    // 偏移量改变即触发事件
    'pagination.offset': function () {
      this.$emit('pageChange', this.pagination.limit, this.pagination.offset)

    },
    // 改变emitEvent强制触发事件
    'emitEvent': function () {
      if (this.pagination.offset === 0) {
        this.$emit('pageChange', this.pagination.limit, this.pagination.offset)
      } else {
        this.pagination.offset = 0
      }
    }
  },
  created() {
    // 默认首次就触发事件
    this.$emit('pageChange', this.pagination.limit, this.pagination.offset)
  },
  computed: {
    page: {
      get: function () {
        if (this.count === 0) {
          return 0
        }
        // 偏移量/每页显示数量 向下取整 + 1
        return Math.floor(this.pagination.offset)
      },
      set: function (val) {
        // 页码改变动态的更新偏移量
        this.pagination.offset = val
        this.get_info()
      }
    },
    perPageNum: {
      get: function () {
        return this.pagination.limit
      },
      set: function (val) {
        if (val !== this.perPageNum) {
          this.pagination.limit = val['value']
          this.get_info()
          // 进行每页显示数量切换时，判断当前偏移量是否大于改变后的偏移量，如果是，则不触发limit改变的事件，因为偏移量的改变也会触发
          if (this.pagination.offset > (Math.floor(this.pagination.offset / val)) * val) {
            this.pageChangeFlag = true
          }
        }
      }
    },
    max: function () {
      // 最大页数，总数/每页显示数量，向上取整
      return Math.ceil(this.count / this.perPageNum)
    }
  },
  props: {
    count: {
      required: true
    },
    emitEvent: {
      required: true,
      default: false
    }
  }
};
</script>
