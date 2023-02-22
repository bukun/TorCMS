<template>
  <q-layout view="hHh lpR fFf">
    <EssentialHead/>
<!--    <q-drawer show-if-above v-model="leftDrawerOpen" side="left" bordered>-->
<!--      <q-list>-->
<!--        <EssentialLink-->
<!--          v-for="link in essentialLinks"-->
<!--          :key="link.title"-->
<!--          v-bind="link"/>-->
<!--      </q-list>-->
<!--    </q-drawer>-->
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
    title: '全部列表',
    caption: '全部列表',
    icon: 'school',
    link: '/#/post/list'
  },
  {
    title: '2010年粮食作物播种面积和产量',
    caption: '2010年粮食作物播种面积和产量',
    icon: 'school',
    link: '/#/post/list/0100'
  },
  {
    title: '2020年粮食作物播种面积和产量',
    caption: '2020年粮食作物播种面积和产量',
    icon: 'school',
    link: '/#/post/list/0200'
  },


];

export default defineComponent({
  name: 'MainLayout',
  components: {
    EssentialHead,
    // EssentialLink
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
