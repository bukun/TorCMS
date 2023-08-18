import {api} from '../boot/axios';

const HEADERS = {

   'Content-Type': 'application/json'

};


const user = {
  login: function (data) {

  return api.post('/api/user/login',
      data,
      {
        headers: HEADERS
      }
    );
  },
  logout: function () {
    return api.get('/api/user/vuelogout',
      {
        headers: HEADERS
      }
    );
  }
};

export {user};
