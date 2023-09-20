import {userService} from '../../service';
import {permissionService} from '../../service';

export const login = ({commit}, userInfo) => {

  return new Promise((resolve, reject) => {
    userService
      .login(userInfo)
      .then(data => {

        //session方式登录，其实不需要token，这里为了JWT登录预留，用username代替。
        //通过Token是否为空判断本地有没有登录过，方便后续处理。

        commit('updateToken', data.data.access_token);

        const newUserInfo = {
          username: data.data.username,
          authorities: data.data.user_pers || [],
          roles: data.data.user_roles || []
        };

        commit('updateUserInfo', newUserInfo);

        let permissions = data.data.user_pers || [];
        let roles = data.data.user_roles || [];
        let isSuperAdmin = false;
        // if (roles.findIndex(t => t.user_roles === 'administrators') >= 0) {
        //   isSuperAdmin = true;
        // }
        if (data.data.username === 'admin') {
          isSuperAdmin = true;
        }

        permissionService.set({
          permissions: permissions,
          isSuperAdmin: isSuperAdmin,
          roles: roles
        });

        resolve(newUserInfo);
      })
      .catch(error => {

        reject(error);
      });
  });
};

export const logout = ({commit}) => {

  return new Promise((resolve) => {
    userService
      .logout()
      .then(() => {
        resolve();
      })
      .catch(error => {
        // console.error(error);
        resolve();
      })
      .finally(() => {
        commit('updateToken', '');
        commit('updateUserInfo', {
          username: '',
          authorities: [],
          roles: []
        });

        permissionService.set({
          permissions: [],
          roles: [],
          isSuperAdmin: false
        });
      });
  });
};

export const getUserInfo = ({commit}) => {
  return new Promise((resolve, reject) => {
    userService
      .getUserInfo()
      .then(data => {
        commit('updateUserInfo', data);
        resolve(data);

      })
      .catch(error => {
        reject(error);
      });
  });
};

export const validate = ({commit}) => {
  return new Promise((resolve, reject) => {
    userService
      .validate()
      .then(data => {

      if (data.code === 0) {
        commit('updateUserInfo', data.userinfo);
        commit('updateToken', data.userinfo.access_token);

      }

        resolve(data);

      })
      .catch(error => {
        reject(error);
      });
  });
};
