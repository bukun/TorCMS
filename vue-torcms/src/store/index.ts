import {createStore} from 'vuex'
import user from './user';
import {authService} from '../service';
import { plugin } from './user/plugin';

export { plugin };
const store = createStore({
  state: user.state,
  getters: user.getters,
  mutations: user.mutations,
  actions: user.actions,
  modules: {}
})

export default store
