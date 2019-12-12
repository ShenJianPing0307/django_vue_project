export default {

  namespaced: true,

  state: {
    menus_list: [],
     permissions_dict: {}


  },

  mutations: {

    GETMENU(state, data) {
      state.menus_list = data
    },
   // GETPERMISSIONS(state, data) {
   //   console.log('mutation',data)
   //    state.permissions_dict = data
   //  }

  },
  //有命名空间提交方式，类似this.$store.dispatch("user/getAllUserList");
  actions: {
    async getMenu(context, object) {
      const res = await object._this.$http.get("crm/menus");
      const {data, meta: {message, code}} = res.data;
      if (code === 2000) {
        context.commit("GETMENU", data.menus_list);
        object._this.$message.error(message)
        console.log('menus', data)
      }
    },

    //     async getPermissions(context, object) {
    //   const res = await object._this.$http.get("rbac/roles/rights");
    //   const {data, meta: {message, code}} = res.data;
    //   if (code === 2000) {
    //     context.commit("GETPERMISSIONS", data);
    //     localStorage.setItem('permissionDict',data)
    //     console.log(data)
    //     console.log('pdisiidsi',data["/crm/dept"])
    //     if (data["/crm/dept"].indexOf('post') >= 0){
    //       console.log("存在")
    //     }else {
    //       console.log("bucunzai ")
    //     }
    //     object._this.$message.error(message)
    //
    //   }
    // }


  },

  getters: {
    getMenu: state => {
      return state.menus_list
    },
  //     getPermission: state => {
  //   return state.permissions_dict
  // }



}

}
