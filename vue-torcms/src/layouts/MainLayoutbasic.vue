<template>
  <q-layout view="hHh lpR fFf">

 <EssentialHead />

    <q-drawer show-if-above v-model="leftDrawerOpen" side="left" bordered>


      <q-list>

        <EssentialLink
          v-for="link in essentialLinks"
          :key="link.title"
          v-bind="link" />
      </q-list>
    </q-drawer>

    <q-page-container>
      <router-view/>
    </q-page-container>

  </q-layout>
</template>

<script lang="ts">
import {defineComponent, ref} from 'vue';
import EssentialLink from 'components/EssentialLink.vue';
import EssentialHead from 'components/Head.vue';

const linksList = [
  {
    title: 'Leaflet',
    caption: 'Leaflet',
    icon: 'school',
    link: '/#/leaflet/'
  },

  {
    title: '基础地理',
    caption: '基础地理',
    icon: 'code',
    link: '/#/basic/basic'
  },
  {
    title: '地貌类型',
    caption: '地貌类型',
    icon: 'chat',
    link: '/#/basic/geomor'
  },
  {
    title: '土壤类型',
    caption: '土壤类型',
    icon: 'code',
    link: '/#/basic/soil'
  },

  {
    title: '植被类型',
    caption: '植被类型',
    icon: 'record_voice_over',
    link: '/#/basic/vegetation'
  },
  {
    title: '海图全球底图',
    caption: '海图全球底图',
    icon: 'record_voice_over',
    link: '/#/basic/nautical'
  },
  {
    title: '海图',
    caption: '海图',
    icon: 'record_voice_over',
    link: '/#/basic/nav-map'
  },
];

export default defineComponent({
  name: 'MainLayout',

  components: {
    EssentialHead,
    EssentialLink
  },

  setup() {
    const leftDrawerOpen = ref(false)

    return {
      essentialLinks: linksList,
      leftDrawerOpen,
      toggleLeftDrawer() {
        leftDrawerOpen.value = !leftDrawerOpen.value
      }
    }
  }
});
</script>
