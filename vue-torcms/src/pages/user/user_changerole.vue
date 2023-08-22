<template>

  <q-page padding>
    <h3>Change Role</h3>
    <div class="row justify-left">
      <q-card class="col-sm-6 col-xs-12">
        <q-card-section>
          <q-form @submit="onSubmit" class="q-gutter-md">


            <q-input filled v-model="model.role"
                     hint="permissions" label="Please enter administrative permission, case 0000"
                     lazy-rules
                     :rules="[ val => val && val.length > 0  || 'Please enter administrative permission, case 0000']"/>
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


import {authService} from '../../service/authService'

export default {

  data() {
    return {
      isPwd: true,
      model: {},

    };
  },
  mounted() {
    this.check_login()

  },
  methods: {
    check_login() {


      this.$store
        .dispatch('getUserInfo')
        .then(async (data) => {

          let formdata = {
            user_name: data.username,
            token: authService.getToken(),
          }

          this.$axios({
            url: '/api/user/verify_jwt',
            method: 'post',
            headers: {'Content-Type': 'application/json'},
            params: formdata
          })
            .then(async (info) => {
                if (info.data.state == true) {
                  this.get_info()
                } else {
                  this.$router.push({
                    path: '/userinfo/login'

                  })
                }
              }
            )
            .catch(function (error) { // 请求失败处理
              console.log(error);
              this.$q.notify('Token signature expired')
              console.log('Error for res: ');
              this.$q.loading.hide();
              console.log(error);
            });


        })
        .catch(e => {

          this.$router.push({
            path: '/userinfo/login'

          })
        });


    },
    onSubmit() {


      let formdata = {
        role: this.model.role,
      }

      this.$axios({
        url: '/user_j/changerole/' + this.$route.query.user_name,
        method: 'post',
        headers: {'Content-Type': 'application/json'},
        params: formdata
      })
        .then(async (statusCode) => {
          console.log(statusCode);
          // statusCode =JSON.stringify(statusCode)
          // alert(JSON.stringify(statusCode.data))

          if (statusCode.data['changerole'] === '1') {


            this.$q.notify('Modified successfully')
            this.$router.push({
              path: '/userinfo/info'
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
    }

  }
};
</script>

