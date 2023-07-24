import Vue from 'vue'
import Vuex from 'vuex'

// import example from './module-example'

import config from './config';
import user from './user';

import { plugin as userPlugin } from './user';




/*
 * If not building with SSR mode, you can
 * directly export the Store instantiation;
 *
 * The function below can be async too; either use
 * async/await or return a Promise which resolves
 * with the Store instance.
 */

const Store = new Vuex.Store({
  modules: {
    config,
    user
  },

  plugins: [userPlugin],


});

export default Store;
