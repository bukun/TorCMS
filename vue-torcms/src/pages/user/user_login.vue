<template>

  <q-page padding>
    <h3>Login</h3>
    <div class="row justify-left">
      <q-card class="col-sm-6 col-xs-12">
        <q-card-section>
          <q-form @submit="onSubmit" class="q-gutter-md">
            <q-input filled v-model="model.user_name"
                     label="User name must be alphabetic or alphanumeric combination (letter)."
                     hint="User name"
                     lazy-rules
                     :rules="[ val => val && val.length > 0 || 'Please type something']"/>
            <q-input v-model="model.user_pass" filled :type="isPwd ? 'password' : 'text'"
                     hint="Password" lazy-rules
                     :rules="[ val => val && val.length >= 6 || 'Please type something']">
              <template v-slot:append>
                <q-icon :name="isPwd ? 'visibility_off' : 'visibility'"
                        class="cursor-pointer"
                        @click="isPwd = !isPwd"
                />
              </template>
            </q-input>


            <q-btn label="Submit" type="submit" :disable="!model.user_name || !model.user_pass" color="primary"/>


          </q-form>
        </q-card-section>
      </q-card>

    </div>
    <div class="row">
      <div class="q-pt-sm">
        <br><br>
        Not have an account?
        <q-btn color="primary" size="sm" label="Register" @click="toRegister"></q-btn>

      </div>
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


      this.$store
        .dispatch('login', {
          user_name: this.model.user_name,
          user_pass: this.model.user_pass,
          login_method: 'vue'
        })
        .then(async (data) => {


          this.$router.push('/userinfo/info')


        })
        .catch(e => {

          this.$q.notify('Wrong username or password. Please try again.')
        });


    },
    toRegister() {
      this.$router.push('/userinfo/register')
    }
  }
};
</script>

