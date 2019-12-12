//根节点mutations

export default {
   GETPERMISSIONS(state, data) {
     console.log('mutation',data)
      state.permissions_dict = data
    }
}
