import { LocalStorage } from 'quasar';

const authService = {
  getToken: function() {
    return LocalStorage.getItem('user_name');
  },
  setToken: function(token) {
    LocalStorage.set('user_name', token);
  }
};

export { authService };
