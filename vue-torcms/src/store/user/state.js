import { authService } from '../../service';

export default {
  token: authService.getToken(),
  userInfo: {
    username: '',
    realname: '',
    avatar: '',
    authorities: [],
    roles: []
  }
};
