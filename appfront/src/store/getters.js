//根节点getters

export default {

  getPermission: state => {
    console.log('getters',state)
    return state.permissions_dict
  }

}
