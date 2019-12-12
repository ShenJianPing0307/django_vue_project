// 这里的 `state` 对象是模块的局部状态,
import axios from 'axios'
// 使用全局 state 和 getter，rootState 和 rootGetter 会作为第三和第四参数传入 getter，
// 也会通过 context 对象的属性传入 action，比如context.rootState


export default {

  namespaced: true,

  state: {

    RightsList: [],
    RightsTree: {}

  },

  mutations: {

    GETRIGHTLIST(state, data) {
      state.RightsList = data
    },

    GETRIGHTTREE(state, data) {
      state.RightsTree = data
    }

  },

  //有命名空间提交方式，类似this.$store.dispatch("user/getAllUserList");
  actions: {
    async getRightsList(context, object) {
      const res = await object._this.$http.get("rbac/rights/list");
      console.log('getRightsList',res)
      const {data, meta: {message, code}} = res.data;
      if (code === 2000) {
        context.commit("GETRIGHTLIST", data)
      }
    },

    async getRightsTree(context, object) {
      const res = await object._this.$http.get("rbac/rights/tree");
      const {data, meta: {message, code}} = res.data;
      if (code === 2000) {
        context.commit("GETRIGHTTREE", data)
      }

    }


  },

  getters: {
    getRightsList: state => {
      return state.RightsList
    },

    getRightsTree: state => {
      return state.RightsTree
    }

  }


}
