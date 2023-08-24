import {user} from '../api';
import {LocalStorage} from 'quasar';
import state from '../store/user/state';
import {authService} from './authService';
import store from '../store';


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
    const local_user_rec = await store.dispatch('getUserInfo');
    if(local_user_rec.code===0){
      store.state.userInfo.username=local_user_rec.username
    }
    var code={user_name: store.state.userInfo.username, token: authService.getToken()}

    var res = await user.verity_user(code);

    return res.data

  }
}


export {userService};
