import {authService} from '../../service';
import {userService} from '../../service';

const plugin = store => {
  // 当 store 初始化后调用
  store.subscribe(mutation => {
    // 每次 mutation 之后调用
    // mutation 的格式为 { type, payload }
    if (mutation.type === 'userinfo/updateToken') {
      authService.setToken(mutation.payload);
    } else if (mutation.type === 'userinfo/updateUserInfo') {
      userService.setUserInfo(mutation.payload);
    }
  });
};

export {plugin};
