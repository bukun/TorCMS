import { LocalStorage } from 'quasar';

const permissionService = {
  get: function() {
    return LocalStorage.getItem('permission');
  },
  set: function(data) {
    LocalStorage.set('permission', data);
  },
  check: function(needPermissions) {
    if (needPermissions && needPermissions.length > 0) {
      let data = this.get();
      if (!data) {
        return false;
      }

      let isSuperAdmin = data.isSuperAdmin;
      if (isSuperAdmin) {
        return true;
      }

      if (!data.permissions) {
        return false;
      }

      let permissions = data.permissions;
      let hasPermission = permissions.some(s => {
        return needPermissions.indexOf(s.authority) > -1;
      });

      return hasPermission;
    }
    return true;
  }
};

export { permissionService };
