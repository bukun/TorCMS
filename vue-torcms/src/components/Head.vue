<template>
  <q-header elevated class="bg-primary text-white" height-hint="98">
    <q-toolbar>

      <q-toolbar-title>
        <q-avatar>
          <img src="https://cdn.quasar.dev/logo-v2/svg/logo-mono-white.svg">
        </q-avatar>
        可视化平台
      </q-toolbar-title>
    </q-toolbar>

    <q-tabs align="left">


      <q-route-tab to="/" label="首页"/>
      <q-route-tab to="/post/listp/0100" label="Technology"/>
      <q-route-tab to="/userinfo/info" label="用户中心"/>
    </q-tabs>
  </q-header>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'EssentialHead',

});
</script>
