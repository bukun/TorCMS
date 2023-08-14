import {authService} from '../../service';
import {userService} from '../../service';

const plugin = store => {
  // 当 store 初始化后调用
  store.subscribe(mutation => {
    console.log('00000000000000000000000000000000000')

    // 每次 mutation 之后调用
    // mutation 的格式为 { type, payload }
    if (mutation.type === 'updateToken') {
      console.log(mutation.payload)
      authService.setToken(mutation.payload);
    } else if (mutation.type === 'updateUserInfo') {
         console.log(mutation.payload)
      userService.setUserInfo(mutation.payload);
    }
  });
};

export {plugin};
