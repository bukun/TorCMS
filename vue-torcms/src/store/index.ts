import {createStore} from 'vuex'
import user from './user';
import {authService} from '../service';

const store = createStore({
  state: user.state,
  getters: user.getters,
  mutations: user.mutations,
  actions: user.actions,
  modules: {}
})

export default store
