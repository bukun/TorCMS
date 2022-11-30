
import { defineStore } from 'pinia';

export const useCounterStore = defineStore('counter1', {
  state: () => ({
    counter: 1111,
  }),
  // getters: {
  //   doubleCount: (state) => state.counter * 2,
  // },
  actions: {
    increment() {
      this.counter++;
    },
  },
});
