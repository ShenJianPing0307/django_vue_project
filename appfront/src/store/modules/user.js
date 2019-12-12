// 这里的 `state` 对象是模块的局部状态,
import axios from 'axios'
// 使用全局 state 和 getter，rootState 和 rootGetter 会作为第三和第四参数传入 getter，
// 也会通过 context 对象的属性传入 action，比如context.rootState


export default {

  namespaced: true,

  state: {

    UserList: [],
    Total: null,
    size: 2,
    query: null,
    page: 1,
    index: null,//用于删除页面更新
    itemObject: null,//用于更新数据后页面更新
    item: {
      id: '',
      username: '',
      password: ''
    },
    DeptList: [],
    RoleList: [],
    AllRolesList: [],

  },

  mutations: {


    ////action中提交该mutation
    GETALLUSER(state, data) {
      state.UserList = data.results; //将添加成功的数据添加到状态，用于页面更新
      state.Total = data.count

    },

    DELUSER(state) {
      //回到第一页
      state.page = 1
    },

    GETDEPART(state, data) {
      state.DeptList = data
    },

    GETALLROLES(state, data) {
      state.AllRolesList = data
    },

    GETUSER(state, data) {
      state.RoleList = data.roles
    }


  },

  //有命名空间提交方式，类似this.$store.dispatch("user/getAllUserList");
  actions: {
    //将Vue实例进行传递接收
    // getAllUserList(context, _this) {
    //   //局部状态通过 context.state 暴露出来，根节点状态则为 context.rootState：
    //
    //   //发送get请求获取API数据
    //   _this.$http.get('crm/user')
    //     .then((response) => {
    //       // handle success
    //       context.commit('GETALLUSER', response.data);
    //       console.log('response', response.data)
    //
    //     })
    //     .catch((error) => {
    //       // handle error
    //       console.log(error);
    //     })
    //     .finally(() => {
    //       // always executed
    //     });
    //   // const response = await this.$http.get('crm/user');
    //   // context.commit('GETALLUSER', response);
    //
    // },

    //加入分页
    getAllUserList(context, object) {
      //局部状态通过 context.state 暴露出来，根节点状态则为 context.rootState：

      //发送get请求获取API数据  crm/user?page=${context.state.page}&size=${context.state.size}&username=${object.query}
     object._this.$http.get(`crm/user?page=${context.state.page}&size=${context.state.size}`)
        .then((response) => {
          // handle success
          context.commit('GETALLUSER', response.data);
          object._this.$message.success("获取数据成功")
          object._this.page=1

        })
        .catch((error) => {
          // handle error
          console.log(error);
        })
        .finally(() => {
          // always executed
        });
      // const response = await this.$http.get('crm/user');
      // context.commit('GETALLUSER', response);


    },

    // async getPageSizeUserList(context,object) {
    //    const res = await object._this.$http.get(`crm/user/?size=${object.size}`)
    // },

    async delUser(context, object) {
      //context包含的参数：commit,dispatch,getters,rootGetters,rootState,state
      const res = await object._this.$http.delete(`crm/user/${object.userId}`);
      const {data, meta: {message, code}} = res.data;
      if (code === 2000) {
        object._this.$message.success(message);
        //回到第一页
        context.commit('DELUSER');
        //删除后刷新页面
        context.dispatch("getAllUserList", object._this)
      }
    },

    async editUser(context, object) {
      const res = await object._this.$http.put(`crm/user/${object.userId}`, object.form);
      const {data, meta: {message, code}} = res.data;
      if (code === 2000) {
        context.dispatch("getAllUserList", {_this:object._this});
        object._this.editDialogFormVisible = false;
        object._this.$message.success(message);
      }
    },

    async getDepart(context, object) {
      const res = await object._this.$http.get(`crm/dept`);
      const {data, meta: {message, code}} = res.data;
      if (code === 2000) {
        context.commit('GETDEPART', data);
      }

    },

    async addUser(context, object) {
      const res = await object._this.$http.post(`crm/user`, object.form);
      const {data, meta: {message, code}} = res.data;
      if (code === 2000) {
        context.dispatch("getAllUserList", object._this);
        object._this.addDialogFormVisible = false
      }
    },

    async getAllRoles(context, object) {
      const res = await object._this.$http.get("rbac/roles");
      const {data, meta: {message, code}} = res.data;
      context.commit("GETALLROLES", data);
    },

    async getUser(context, object) {
      const res = await object._this.$http.get(`crm/user/${object.id}`);
      const {data, meta: {message, code}} = res.data;
      if (code === 2000) {
        context.commit("GETUSER", data);
      }

    },

    async setRole(context, object) {
      const res = await object._this.$http.put(`crm/user/${object.id}/role`, object.rid_list);
      const {data, meta: {message, code}} = res.data;
      if (code === 2000) {
        object._this.$message(message);
        context.dispatch("getAllUserList", object._this);
        object._this.rolesDialogFormVisible = false
      }
    }


  },

  getters: {
    getUserList: state => {
      // "UserList":[
      //   {
      //     "id": 1,
      //     "gender": "男",
      //     "department": {
      //       "id": 1,
      //       "name": "生产部"
      //     },
      //     "roles": [
      //       {
      //         "id": 2,
      //         "title": "总监",
      //         "permissions": []
      //       },
      //       {
      //         "id": 3,
      //         "title": "员工",
      //         "permissions": []
      //       }
      //     ],
      //     "username": "zq",
      //     "password": "93884809",
      //     "email": "dsdsd45s3456@qq.com",
      //     "name": "张庆",
      //     "phone": "123456"
      //   }
      // ]
      // let UserArray = [];
      // let array = [];
      // let roles = null;
      // state.UserList.forEach(function (item) {
      //   item.roles.forEach(role => {
      //     array.push(role.title);
      //     return array
      //   });
      //   roles = array.join("、");
      //
      //   UserArray.push({
      //     "id": item.id,
      //     "gender": item.gender,
      //     "department": item.department.name,
      //     "username": item.username,
      //     "password": item.password,
      //     "email": item.email,
      //     "name": item.name,
      //     "phone": item.phone,
      //     "roles": roles,
      //
      //   });
      // });
      // state.UserList = UserArray;
      return state.UserList;
    },

    getTotal: state => {
      return state.Total
    },

    geDeptList: state => {
      return state.DeptList;
    },

    getRolesList: state => {
      return state.RoleList;
    },

    getRoleIdList: (state, getters) => {
      let RoleIdArray = [];
      getters.getRolesList.forEach(item => {
        RoleIdArray.push(item.id);
      });
      return RoleIdArray
    },

    getALLRolesList: state => {
      return state.AllRolesList
    },

    getAllRoleIdList: (state, getters) => {
      let AllRoleIdArray = [];
      getters.getALLRolesList.forEach(item => {
        AllRoleIdArray.push(item.id);
      });
      return AllRoleIdArray
    },

  }


}
