<template>
  <q-page padding>
    <h3>User info</h3>
    <div class="row justify-left ">
      <div class="col-sm-4 col-xs-12">
        <q-markup-table :separator="separator" flat bordered>
          <tbody>
          <tr v-for="(item,index)  in this.info.data" :key="index">
            <td class="col-2 text-right">{{ index }}</td>
            <td>{{ item }}</td>
          </tr>
          </tbody>
        </q-markup-table>
      </div>
    </div>
    <div class="row">
      <div class="q-pt-sm">
        <br><br>
        <q-btn color="primary" size="sm" label="Modify personal information " @click="toChangeinfo"></q-btn>
        <q-btn color="secondary" size="sm" label="Change password" @click="toChangepass"></q-btn>
        <!--        <q-btn color="purple" size="sm" label="Change role" @click="toChangerole"></q-btn>-->
        <q-btn color="blue-grey" size="sm" label="Logout" @click="toLogout"></q-btn>
      </div>
    </div>
  </q-page>
</template>

<script>
import {authService} from '../../service';

export default {
  data() {
    return {
      info: '',
      user_name: ''

    };
  },
  mounted() {
    this.get_info()

  },
  methods: {


    get_info() {
      this.$axios({
        url: '/user_j/j_info',
        method: 'get',
        headers: {'Content-Type': 'application/json'},
        params: {user_name: this.$route.query.user_name}
      }).then(response => {

          if (response.data.user_name) {

            this.info = response
            this.user_name = response.data.user_name
          }
        }
      )
        .catch(function (error) { // 请求失败处理
          console.log('Error for info2: ');
          console.log(error);
        });
    },
    toChangeinfo() {
      this.$router.push({
        path: '/userinfo/changeinfo'
      })
    },
    toChangepass() {
      this.$router.push({
        path: '/userinfo/changepass'
      })
    },
    toChangerole() {
      this.$router.push({
        path: '/userinfo/changerole',
        query: {
          user_name: this.user_name
        }
      })
    },
    toLogin() {
      this.$router.push({
        path: '/userinfo/login'

      })
    },
    toLogout() {
      this.$store
        .dispatch('logout')
        .then(async () => {
          this.$router.push('/userinfo/login');
        })
        .catch(e => {
          console.error(e);
        });
    }

  },

};
</script>

