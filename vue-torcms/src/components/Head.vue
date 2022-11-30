<template>
  <q-header elevated class="bg-primary text-white" height-hint="98">
    <q-toolbar>
      <q-btn dense flat round icon="menu" @click="toggleLeftDrawer"/>
      <q-toolbar-title>
        <q-avatar>
          <img src="https://cdn.quasar.dev/logo-v2/svg/logo-mono-white.svg">
        </q-avatar>
        县域粮食生产优势可视化平台
      </q-toolbar-title>
    </q-toolbar>

    <q-tabs align="left">
      <q-route-tab to="/" label="Home"/>
      <q-route-tab to="/post/list" label="post list"/>
      <q-route-tab to="/userinfo/login" label="Login"/>

    </q-tabs>
  </q-header>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'EssentialHead',

});
</script>
