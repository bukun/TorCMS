import { LocalStorage } from 'quasar';

const authService = {
  getToken: function() {
    return LocalStorage.getItem('token');
  },
  setToken: function(token) {
    LocalStorage.set('token', token);
  }
};

export { authService };
