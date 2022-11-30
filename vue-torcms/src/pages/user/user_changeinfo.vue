<template>

  <q-page padding>
    <h3>Change info</h3>
    <div class="row justify-left">
      <q-card class="col-sm-6 col-xs-12">
        <q-card-section>
          <q-form @submit="onSubmit" class="q-gutter-md">

            <q-input v-model="model.rawpass" filled :type="isPwd ? 'password' : 'text'"
                     hint="Please input a password " lazy-rules
                     :rules="[ val => val && val.length >= 6 || 'Please type something']">
              <template v-slot:append>
                <q-icon :name="isPwd ? 'visibility_off' : 'visibility'"
                        class="cursor-pointer"
                        @click="isPwd = !isPwd"
                />
              </template>
            </q-input>

            <q-input filled type="email" v-model="model.user_email"
                     hint="Email" label="Please enter a correct E-mail."
                     lazy-rules
                     :rules="[ val => val && val.length > 0  || 'Please type your email']"/>
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
      isPwd: true,
      model: {}
    };
  },
  methods: {
    onSubmit() {
      let formdata = {
        rawpass: this.model.rawpass,
        user_email: this.model.user_email,
      }

      this.$axios({
        url: '/user_j/j_changeinfo',
        method: 'post',
        headers: {'Content-Type': 'application/json'},
        params: formdata
      })
        .then(async (statusCode) => {
          console.log(statusCode);
          // statusCode =JSON.stringify(statusCode)
          // alert(JSON.stringify(statusCode.data['code']))

          if (statusCode.data['code'] === '21') {
            this.$q.notify('Email address does not conform to the rules, please re-enter')
          } else if (statusCode.data['code'] === '22') {
            this.$q.notify('Email already exists, please re-enter')
          } else {
            this.$q.notify('Modified successfully')
            this.$router.push({
              path: '/userinfo/info'
            });
            this.$q.loading.hide();
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

