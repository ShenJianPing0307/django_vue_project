import Vue from 'vue'
import Vuex from 'vuex'
import state from './state'
import mutations from './mutations'
import getters from './getters'
import actions from './actions'
import user from './modules/user'
import rights from './modules/right'
import roles from './modules/role'
import homes from './modules/home'


Vue.use(Vuex);

//组装模块并导出 store 的地方
export default new Vuex.Store({
  //根节点相关
  state,
  mutations,
  getters,
  actions,

  //模块相关
  modules: {
    user,
    rights,
    roles,
    homes,

  },

});


