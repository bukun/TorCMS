import { authService } from '../../service';

export default {
  token: authService.getToken(),
  userInfo: {
    username: '',
    authorities: [],
    roles: []
  }
};
