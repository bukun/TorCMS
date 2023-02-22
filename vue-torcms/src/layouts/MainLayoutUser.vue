<template>
  <q-layout view="hHh lpR fFf">

    <EssentialHead/>

    <q-drawer show-if-above v-model="leftDrawerOpen" side="left" bordered>


      <q-list>

        <EssentialLink
          v-for="link in essentialLinks"
          :key="link.title"
          v-bind="link"/>
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

 let linksList=[{
    title: 'user info',
    caption: 'userinfo',
    icon: 'school',
    link: '/#/userinfo/info'
  },
  {
    title: 'change info',
    caption: 'changeinfo',
    icon: 'school',
    link: '/#/userinfo/changeinfo'
  },
  {
    title: 'change password',
    caption: 'changepass',
    icon: 'school',
    link: '/#/userinfo/changepass'
  },
  {
    title: 'changerole',
    caption: 'changerole',
    icon: 'school',
    link: '/#/userinfo/changerole'
  }]


export default defineComponent({
  name: 'MainLayout',

  components: {
    EssentialHead,
    EssentialLink
  },

setup()
    {
      const leftDrawerOpen = ref(false)

      return {
        essentialLinks: linksList,
        leftDrawerOpen,
        toggleLeftDrawer() {
          leftDrawerOpen.value = !leftDrawerOpen.value
        }
      }
    },

});

</script>
