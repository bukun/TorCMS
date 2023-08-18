import {createStore} from 'vuex'
import user from './user';
import {plugin as userPlugin} from './user/plugin';


const store = createStore({
  state: user.state,
  getters: user.getters,
  mutations: user.mutations,
  actions: user.actions,
  modules: {},
  plugins: [userPlugin]
})


export default store
