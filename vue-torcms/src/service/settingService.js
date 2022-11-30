import { LocalStorage, SessionStorage} from 'quasar';

const settingService = {
  clear: function() {
    LocalStorage.clear();
    SessionStorage.clear();
  }
};

export { settingService };
