import axios from 'axios'

export default {

    async getPermissions(context, object) {
      const res = await object._this.$http.get("rbac/roles/rights");
      const {data, meta: {message, code}} = res.data;
      if (code === 2000) {
        context.commit("GETPERMISSIONS", data);
        object._this.$message.error(message)
        console.log('permissions', data)
      }
    }

}



