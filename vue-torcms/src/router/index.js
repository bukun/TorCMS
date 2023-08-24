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


  const whiteList = ['/userinfo/login', '/403', '/'];

  function hasPermission(router) {

    if (whiteList.indexOf(router.path) !== -1) {
      return true;
    }

    return true;
  }


  Router.beforeEach(async (to, from, next) => {

    const isLogin = await store.dispatch('validate')
    const token = authService.getToken();
    const aa = isLogin
    let needLogin = to.matched.some(match => match.meta.needLogin)
    if (needLogin) {
      if (token) {
        const userInfo = store.state.userInfo;

        if (!userInfo.username) {

          try {

            if (aa.code === 0) {
              next();
            } else {
              await store.dispatch('logout');
              next('/userinfo/login');
            }

          } catch (e) {
            if (whiteList.indexOf(to.path) !== -1) {
              next();
            } else {
              next('/userinfo/login');
            }
          }
        } else {
          if (aa.code === 0) {
            next();
          } else {
            await store.dispatch('logout');
            next('/userinfo/login');
          }


        }
      } else {
        if (whiteList.indexOf(to.path) !== -1) {

          next();
        } else {
          if (aa.code === 0) {
            next();
          } else {
            await store.dispatch('logout');
            next('/userinfo/login');
          }


        }
      }
    } else {
      next()
    }
  });


  return Router;
});

