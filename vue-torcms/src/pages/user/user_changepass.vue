<template>

  <q-page padding>
    <h3>Change password</h3>
    <div class="row justify-left">
      <q-card class="col-sm-6 col-xs-12">
        <q-card-section>
          <q-form @submit="onSubmit" class="q-gutter-md">

            <q-input v-model="model.rawpass" filled :type="isPwd ? 'password' : 'text'"
                     hint="Please enter the original password " lazy-rules
                     :rules="[ val => val && val.length >= 6 || 'Please type something']">
              <template v-slot:append>
                <q-icon :name="isPwd ? 'visibility_off' : 'visibility'"
                        class="cursor-pointer"
                        @click="isPwd = !isPwd"
                />
              </template>
            </q-input>

            <q-input v-model="model.user_pass" filled :type="isPwd ? 'password' : 'text'"
                     hint="Password at least 6, the longest 20." lazy-rules
                     :rules="[ val => val && val.length >= 6 || 'Please type something']">
              <template v-slot:append>
                <q-icon :name="isPwd ? 'visibility_off' : 'visibility'"
                        class="cursor-pointer"
                        @click="isPwd = !isPwd"
                />
              </template>
            </q-input>
            <q-input v-model="model.user_pass2" filled :type="isPwd ? 'password' : 'text'"
                     hint="Please confirm and password input." lazy-rules
                     :rules="[ val => (val === this.model.user_pass) || 'The two passwords are different']">
              <template v-slot:append>
                <q-icon :name="isPwd ? 'visibility_off' : 'visibility'"
                        class="cursor-pointer"
                        @click="isPwd = !isPwd"
                />
              </template>
            </q-input>
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


import {authService} from "../../service";

export default {
  data() {
    return {
      isPwd: true,
      model: {}
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
        rawpass: this.model.rawpass,
        user_pass: this.model.user_pass
      }

      this.$axios({
        url: '/user_j/j_changepass',
        method: 'post',
        headers: {'Content-Type': 'application/json'},
        params: formdata
      })
        .then(async (statusCode) => {
          console.log(statusCode);

          if (statusCode.data['success']) {
            this.$q.notify('Modified successfully')
            this.$router.push({
              path: '/userinfo/info'
            });
            this.$q.loading.hide();


          } else {
            this.$q.notify('The original password is incorrect.')
          }
        })
        .catch(function (error) { // 请求失败处理
          this.$q.notify('Password reset failed')
          console.log('Error for res: ');
          this.$q.loading.hide();
          console.log(error);
        });
    }

  }
};
</script>

