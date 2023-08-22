import {user} from '../api';
import {LocalStorage} from 'quasar';

const userService = {
  login: async function (data) {
    var res = await user.login(data);
    return res.data;
  },
  logout: async function () {
    var res = await user.logout();
    return res.data;
  },
  getUserInfo: async function () {
    return LocalStorage.getItem('userInfo') || {};
  },
  setUserInfo: function (userInfo) {
    LocalStorage.set('userInfo', userInfo);
  },
  iwalogin: async function (code) {
    try {
      var res = await user.verity_user(code);

      return res.data
    } catch (error) {
      console.log(error)
    }
  }
}


export {userService};
