import {route} from 'quasar/wrappers';

import {authService} from '../service';
import store from '../store';

import {
  createMemoryHistory,
  createRouter,
  createWebHashHistory,
  createWebHistory,
} from 'vue-router';


import routes from './routes';

/*
 * If not building with SSR mode, you can
 * directly export the Router instantiation;
 *
 * The function below can be async too; either use
 * async/await or return a Promise which resolves
 * with the Router instance.
 */


export default route(function (/* { store, ssrContext } */) {
  const createHistory = process.env.SERVER
    ? createMemoryHistory
    : (process.env.VUE_ROUTER_MODE === 'history' ? createWebHistory : createWebHashHistory);

  const Router = createRouter({
    scrollBehavior: () => ({left: 0, top: 0}),
    routes,

    // Leave this as is and make changes in quasar.conf.js instead!
    // quasar.conf.js -> build -> vueRouterMode
    // quasar.conf.js -> build -> publicPath
    history: createHistory(process.env.VUE_ROUTER_BASE),
  });


  const whiteList = ['/userinfo/login', '/403'];


  Router.beforeEach(async (to, from, next) => {


    const token = authService.getToken();
    if (token) {
      const userInfo = store.state.user.userInfo;

      if (!userInfo.username) {
        try {
          await store.dispatch('user/getUserInfo');
          next();
        } catch (e) {
          if (whiteList.indexOf(to.path) !== -1) {
            next();
          } else {
            next('/userinfo/login');
          }
        }
      } else {
        if (whiteList.indexOf(to.path) !== -1) {
          next();
        } else {
          next({path: '/403', replace: true});
        }
      }
    } else {
      if (whiteList.indexOf(to.path) !== -1) {
        next();
      } else {
        next('/userinfo/login');
      }
    }
  });


  return Router;
});
