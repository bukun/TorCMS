import {user} from '../api';
import {LocalStorage} from 'quasar';
import state from '../store/user/state';
import {authService} from './authService';

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
  validate: async function () {

    var code={user_name: state.userInfo.username, token: authService.getToken()}
    try {
      var res = await user.verity_user(code);
      return res.data
    } catch (error) {
      return {'code':1}
    }
  }
}


export {userService};
