import {route} from 'quasar/wrappers';

import {authService} from '../service';
import {userService} from '../service';
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
    console.log('111111111111111111111111111111111')
    console.log(aa)

    let needLogin = to.matched.some(match => match.meta.needLogin)
    if (needLogin) {
      console.log('1.2.2.2.1.1.1.1.121.1.31.1.11')
      if (token) {
        console.log('1.33333.1.131313131.1313')
        const userInfo = store.state.userInfo;
        console.log('1.4.1.1.4.41.4444.4.44444')

        if (!userInfo.username) {

          console.log('2222222222222222222222222222222222222')
          try {

            if (aa.code === 0) {
              console.log('33333333333333333333333333333333333333333')
              next();
            } else {
              console.log('444444444444444444444444444444444444444444444')
              await store.dispatch('logout');
              next('/userinfo/login');
            }

          } catch (e) {
            console.log('555555555555555555555555555555555555555')
            if (whiteList.indexOf(to.path) !== -1) {
              next();
            } else {
              console.log('66666666666666666666666666666')
              next('/userinfo/login');
            }
          }
        } else {
          console.log('1.555555555555')

          console.log('7777777777777777777777777777777777777')
          console.log(aa.code)
          if (aa.code === 0) {
            console.log('1.8888888')
            next();
          } else {
            console.log('1.99999999')
            await store.dispatch('logout');
            next('/userinfo/login');
          }


        }
      } else {
        console.log('88888888888888888888888888888888888888')
        if (whiteList.indexOf(to.path) !== -1) {

          next();
        } else {
          if (aa.code === 0) {
            console.log('2.8888888')
            next();
          } else {
            console.log('2.99999999')
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

