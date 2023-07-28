import {api} from '../boot/axios';

const HEADERS = {
  'Content-Type': 'application/x-www-form-urlencoded'
};

const user = {
  login: function (data) {
    return api.post('/user_j/login',
      data,
      {
        headers: HEADERS
      }
    );
  },
  logout: function () {
    return api.get('/user_j/logout',
      {
        headers: HEADERS
      }
    );
  }
};

export {user};
