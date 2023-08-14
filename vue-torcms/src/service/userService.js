import { user} from '../api';
import { LocalStorage } from 'quasar';

const userService = {
  login: async function(data) {
    var res = await user.login(data);
    console.log(res)
    console.log(res.data)
    return res.data;
  },
  logout: async function() {
    var res = await user.logout();
    return res.data;
  },
  getUserInfo: async function() {
    return LocalStorage.getItem('userInfo') || {};
  },
  setUserInfo: function(userInfo) {
    LocalStorage.set('userInfo', userInfo);
  }
};

export { userService };
