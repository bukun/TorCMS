import {boot} from 'quasar/wrappers';
import axios, {AxiosInstance} from 'axios';
import {Notify} from 'quasar'
import qs from "qs";
// import Router from '../router/index';

declare module '@vue/runtime-core' {
  interface ComponentCustomProperties {
    $axios: AxiosInstance;
  }
}

// Be careful when using SSR for cross-request state pollution
// due to creating a Singleton instance here;
// If any client changes this (global) instance, it might be a
// good idea to move this instance creation inside of the
// "export default () => {}" function below (which runs individually
// for each client)

const api = axios.create({
  baseURL: process.env.API,
  timeout: 10000
});


api.defaults.transformRequest = [
  function(data, headers) {
    // Do whatever you want to transform the data
    let contentType = headers["Content-Type"] || headers["content-type"];
    if (!contentType) {
      contentType = "application/json";
      headers["Content-Type"] = "application/json";
    }

    if (contentType.indexOf("multipart/form-data") >= 0) {
      return data;
    } else if (contentType.indexOf("application/x-www-form-urlencoded") >= 0) {
      return qs.stringify(data);
    }

    return JSON.stringify(data);
  }
];
//
// // Add a request interceptor
// api.interceptors.request.use(
//   function(config) {
//     if (config.permission && !permissionService.check(config.permission)) {
//       throw {
//         message: "403 forbidden"
//       };
//     }
//
//     if (config.dataSource) {
//       console.log("config.dataSource = " + config.dataSource);
//       config.headers["dataSource"] = config.dataSource;
//     }
//
//     return config;
//   },
//   function(error) {
//     // Do something with request error
//     return Promise.reject(error);
//   }
// );





// function login() {
//   setTimeout(() => {
//     Router.push({
//       path: '/userinfo/login'
//     });
//
//
//   }, 1000);
// }

// Add a response interceptor
api.interceptors.response.use(
  function(response) {
    // Any status code that lie within the range of 2xx cause this function to trigger
    // Do something with response data
    return response;
  },
  function(error) {
    // Any status codes that falls outside the range of 2xx cause this function to trigger
    // Do something with response error

    if (error.response) {
      if (error.response.status === 401) {
        Notify.create({
          message:  error.response.data.message,
          type: 'negative'
        });
        // login();
      } else if (error.response.data && error.response.data.message) {
        Notify.create({
          message: error.response.data.message,
          type: 'negative'
        });
      } else {
        Notify.create({
          message: error.response.statusText || error.response.status,
          type: 'negative'
        });
      }
    } else if (error.message.indexOf('timeout') > -1) {
      Notify.create({
        message: 'Network timeout',
        type: 'negative'
      });
    } else if (error.message) {
      Notify.create({
        message: error.message,
        type: 'negative'
      });
    } else {
      Notify.create({
        message: 'http request error',
        type: 'negative'
      });
    }

    return Promise.reject(error);
  }
);



export default boot(({app}) => {
  // for use inside Vue files (Options API) through this.$axios and this.$api

  app.config.globalProperties.$axios = axios;
  // ^ ^ ^ this will allow you to use this.$axios (for Vue Options API form)
  //       so you won't necessarily have to import axios in each vue file

  app.config.globalProperties.$api = api;
  // ^ ^ ^ this will allow you to use this.$api (for Vue Options API form)
  //       so you can easily perform requests against your app's API


});

export {api};
