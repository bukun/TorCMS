import { LocalStorage } from 'quasar';

const authService = {
  getToken: function() {
    return LocalStorage.getItem('access_token');
  },
  setToken: function(token) {
    LocalStorage.set('access_token', token);
  },



};

export { authService };
