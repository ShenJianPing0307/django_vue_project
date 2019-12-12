// 这里的 `state` 对象是模块的局部状态,
import axios from 'axios'
// 使用全局 state 和 getter，rootState 和 rootGetter 会作为第三和第四参数传入 getter，
// 也会通过 context 对象的属性传入 action，比如context.rootState


export default {

  namespaced: true,

  state: {

    RolesList: [],

  },

  mutations: {

    GETROLESLIST(state, data) {
      state.RolesList = data
    }

  },

  //有命名空间提交方式，类似this.$store.dispatch("user/getAllUserList");
  actions: {
    async getRolesList(context, object) {
      const res = await object._this.$http.get("rbac/roles");
      const {data, meta: {message, code}} = res.data;
      if (code === 2000) {
        console.log('roleslist', data)
        context.commit("GETROLESLIST", data)
      }
    },

    async deleteRight(context, object) {
      const res = await object._this.$http.delete(`rbac/roles/${object.roleId}/permission/${object.rightId}`)
      const {data, meta: {message, code}} = res.data;
      if (code === 2000) {
        context.dispatch('getRolesList', object);
        object._this.$message(message)
      }
    },

    async updateRights(context, object) {
      //更新角色权限
      const res = await object._this.$http.put(`rbac/roles/${object.roleId}/permission`,object.rightIds)
            const {data, meta: {message, code}} = res.data;
      if (code === 2000) {
        context.dispatch('getRolesList', object);
        object._this.$message.success(message);
        object._this.setRightDialogVisible = false
      }
    }


  },

  getters: {
    getRolesList: state => {
      return state.RolesList
    }

  }


}
