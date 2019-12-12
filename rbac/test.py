list = [{'permissions__menu__position': 1, 'permissions__menu_id': 1, 'permissions__url': '/user',
         'permissions__parent_id': None, 'permissions__menu__title': '用户管理', 'permissions__title': '用户列表',
         'permissions__menu__icon': 'el-icon-location', 'permissions__id': 1, 'permissions__action__code': 'get'},
        {'permissions__menu__position': 2, 'permissions__menu_id': 2, 'permissions__url': '/rights',
         'permissions__parent_id': None, 'permissions__menu__title': '权限管理', 'permissions__title': '权限列表',
         'permissions__menu__icon': 'el-icon-s-check', 'permissions__id': 2, 'permissions__action__code': 'get'},
        {'permissions__menu__position': None, 'permissions__menu_id': None, 'permissions__url': '/user',
         'permissions__parent_id': 1, 'permissions__menu__title': None, 'permissions__title': '添加用户',
         'permissions__menu__icon': None, 'permissions__id': 5, 'permissions__action__code': 'post'},
        {'permissions__menu__position': 2, 'permissions__menu_id': 2, 'permissions__url': '/roles',
         'permissions__parent_id': None, 'permissions__menu__title': '权限管理', 'permissions__title': '角色列表',
         'permissions__menu__icon': 'el-icon-s-check', 'permissions__id': 7, 'permissions__action__code': 'get'}]
for row in list:
    if row["permissions__url"] in list:
        row["permissions__url"].append(row["permissions__action__code"])
    else:
        row["permissions__url"] = [row["permissions__action__code"], ]



