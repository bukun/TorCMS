<template>
  <q-page class="row items-center justify-evenly">

    <div>
      <h3>核心GIS组件</h3>
      <ul>
        <li>Leaflet</li>
        <li>OpenLayers</li>
        <li>MapTalks</li>
        <li>MapBox</li>
        <li>Cesium</li>
      </ul>
    </div>

    <div>
      <h3>基础框架</h3>
      <ul>
        <li>VueJS 3</li>
        <li>Quasar 2</li>
      </ul>
    </div>

    <div>
      <h3>扩展组件</h3>
      <ul>
        <li>Three JS</li>
      </ul>
    </div>

    <example-component
      title="Example component"
      active
      :todos="todos"
      :meta="meta"
    ></example-component>
  </q-page>
</template>

<script lang="ts">
import {Todo, Meta} from 'components/models';
import ExampleComponent from 'components/ExampleComponent.vue';
import {defineComponent, ref} from 'vue';

export default defineComponent({
  name: 'IndexPage',
  components: {ExampleComponent},
  setup() {
    const todos = ref<Todo[]>([
      {
        id: 1,
        content: 'ct1'
      },
      {
        id: 2,
        content: 'ct2'
      },
      {
        id: 3,
        content: 'ct3'
      },
      {
        id: 4,
        content: 'ct4'
      },
      {
        id: 5,
        content: 'ct5'
      }
    ]);
    const meta = ref<Meta>({
      totalCount: 1200
    });
    return {todos, meta};
  }
});
</script>
