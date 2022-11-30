import { api } from 'boot/axios';

const HEADERS = {
  'Content-Type': 'application/x-www-form-urlencoded'
};

const user = {
  login: function(data) {
    return api.post('/user/j_login',
      data,
      {
        headers: HEADERS
      }
    );
  },
  logout: function() {
    return api.get('/user/j_logout',
      {
        headers: HEADERS
      }
    );
  }
};

export { user };
