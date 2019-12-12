<template>
  <el-card class="box-card">
    <!--面包屑-->
    <MyBread level1="用户管理" level2="用户列表"></MyBread>
    <!--搜索框-->
    <el-row class="SearchRow">
      <el-col :span="6">
        <el-input clearable @clear="loadUserLIst" placeholder="请输用户名" v-model="query" class="input-with-select">
          <el-button slot="append" icon="el-icon-search" @click="Search"></el-button>
        </el-input>
      </el-col>
      <el-col :span="5">
        <el-button type="success" @click="showadduser">添加用户</el-button>
      </el-col>
    </el-row>
    <!--表格组件-->
    <el-table
      :data="UserList"
      style="width: 100%">
      <el-table-column
        fixed
        type="index"
        label="#">
      </el-table-column>
      <el-table-column
        prop="username"
        label="用户名">
      </el-table-column>
      <el-table-column
        prop="name"
        label="姓名">
      </el-table-column>
      <el-table-column
        prop="password"
        label="密码">
      </el-table-column>
      <el-table-column
        prop="email"
        label="邮箱">
      </el-table-column>
      <el-table-column
        prop="roles"
        label="角色">
      </el-table-column>
      <el-table-column
        prop="phone"
        label="手机">
      </el-table-column>
      <el-table-column
        prop="gender"
        label="性别">
      </el-table-column>
      <el-table-column
        prop="department"
        label="所属部门">
      </el-table-column>
      <el-table-column
        prop="phone"
        label="手机">
      </el-table-column>
      <el-table-column
        fixed="right"
        label="操作"
        width="150">
        <template slot-scope="scope">
          <el-button size="mini" plain type="primary" icon="el-icon-edit" circle
                     @click="showedituser(scope.row)"
          ></el-button>
          <el-button size="mini" plain type="success" icon="el-icon-check" circle
                     @click="showroles(scope.row)"
          ></el-button>
          <el-button size="mini" plain type="danger" icon="el-icon-delete" circle
                     @click="showdeluser(scope.row.id)"></el-button>
        </template>
      </el-table-column>
    </el-table>
    <!--分页组件-->
    <el-pagination
      @size-change="handleSizeChange"
      @current-change="handleCurrentChange"
      :current-page="page"
      :page-sizes="[2, 4, 6, 8]"
      :page-size=size
      layout="total, sizes, prev, pager, next, jumper"
      :total="total">
    </el-pagination>

    <!--嵌套修改的表单-->
    <!-- Form -->
    <el-dialog title="编辑用户" :visible.sync="editDialogFormVisible">
      <el-form :model="form">
        <el-form-item label="用户名" :label-width="formLabelWidth">
          <el-input disabled v-model="form.username" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="密码" :label-width="formLabelWidth">
          <el-input v-model="form.password" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="邮箱" :label-width="formLabelWidth">
          <el-input v-model="form.email" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="手机" :label-width="formLabelWidth">
          <el-input v-model="form.phone" autocomplete="off"></el-input>
        </el-form-item>

      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="editDialogFormVisible = false">取 消</el-button>
        <el-button type="primary" @click="edituser()">确 定</el-button>
      </div>
    </el-dialog>

    <!--嵌套添加的表单-->
    <!-- Form -->
    <el-dialog title="添加用户" :visible.sync="addDialogFormVisible">
      <el-form :model="addform">
        <el-form-item label="用户名" :label-width="formLabelWidth">
          <el-input v-model="addform.username" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="姓名" :label-width="formLabelWidth">
          <el-input v-model="addform.name" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="密码" :label-width="formLabelWidth">
          <el-input v-model="addform.password" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="邮箱" :label-width="formLabelWidth">
          <el-input v-model="addform.email" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="手机" :label-width="formLabelWidth">
          <el-input v-model="addform.phone" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="性别" :label-width="formLabelWidth">
          <el-radio v-model="addform.gender" label="1">男</el-radio>
          <el-radio v-model="addform.gender" label="2">女</el-radio>
        </el-form-item>
        <el-form-item label="所属部门" :label-width="formLabelWidth">

          <el-select class="select-size" v-model="addform.department" placeholder="请选择">
            <el-option
              v-for="item in DeptList"
              :key="item.id"
              :label="item.name"
              :value="item.id">
            </el-option>
          </el-select>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="addDialogFormVisible = false">取 消</el-button>
        <el-button type="primary" @click="adduser()">确 定</el-button>
      </div>
    </el-dialog>

    <!--分配角色表单-->
    <!-- Form -->
    <el-dialog title="分配角色" :visible.sync="rolesDialogFormVisible">

      <el-form :model="form">
        <el-form-item label="用户名" :label-width="formLabelWidth">
          <el-input disabled v-model="currentuser.name" autocomplete="off"></el-input>
        </el-form-item>

        <el-form-item label="角色" :label-width="formLabelWidth">
          <el-select class="select-roles" @blur="blurInput" @focus="focusInput" filterable clearable
                     v-model="CheckedRolesIdList" @change="changeSelect" multiple :placeholder="showInputTitle">
            <el-option
              v-for="item in AllRoleList"
              :key="item.id"
              :label="item.title"
              :value="item.id">
            </el-option>
          </el-select>
        </el-form-item>

      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="rolesDialogFormVisible = false">取 消</el-button>
        <el-button type="primary" @click="setrole()">确 定</el-button>
      </div>
    </el-dialog>

  </el-card>
</template>

<script>

  import {mapGetters} from 'vuex'

  export default {
    name: "User",
    data: function () {
      return {
        size: 2,
        query: '',
        page: 1,

        editDialogFormVisible: false,
        addDialogFormVisible: false,
        rolesDialogFormVisible: false,
        form: {
          username: '',
          password: '',
          email: '',
          phone: '',
        },
        addform: {
          username: '',
          name: '',
          password: '',
          email: '',
          phone: '',
          gender: '1',
          department: ''

        },
        formLabelWidth: '120px',
        //分配角色多选
        CheckedRolesIdList: [], //默认值未设置
        showInputTitle: '请选择',
        //当前角色用户
        currentuser: ''


      }
    },
    created() {
      this.getUsers()
    },
    methods: {
      //点击清空搜索框，重新获取数据
      loadUserLIst() {
        this.getUsers()
      },
      //分配角色多选方法
      changeSelect(val) {
        this.CheckedRolesIdList = val
      },
      clear() {
        this.CheckedRolesIdList = []
      },
      focusInput() {
        this.showInputTitle = '请搜索'
      },
      blurInput() {
        this.showInputTitle = '请选择'
      },
      //分页方法
      handleSizeChange(val) {
        console.log(`每页 ${val} 条`);
        this.$store.state.user.size = val;
        this.getUsers()
        // this.$store.dispatch("user/getPageSizeUserList",{size:val,_this:this})
      },

      handleCurrentChange(val) {
        console.log(`当前页: ${val}`);
        this.$store.state.user.page = val;
        this.getUsers()
      },
      Search() {
        this.getUsers()
      },
      getUsers() {
        //将token设置在请求头中提交,已经在拦截器中设置
        // this.$http.defaults.headers.common['Authorization'] = localStorage.getItem("token");
        this.$store.dispatch('user/getAllUserList', {_this: this, query: this.query})//this是Vue实例

      },

      showdeluser(id) {
        this.$confirm('此操作将永久删除该用户信息, 是否继续?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          //发送删除请求的用户id
          this.$store.dispatch("user/delUser", {userId: id, _this: this});

        }).catch(() => {
          this.$message({
            type: 'info',
            message: '已取消删除'
          });
        });
      },

      showedituser(row) {
        //赋默认值
        this.form = row;
        //弹框
        this.editDialogFormVisible = true;

      },

      edituser() {
        //发送修改后的数据
        //此时form已经是每一行的row对象，row里面有id
        this.$store.dispatch("user/editUser", {userId: this.form.id, form: this.form, _this: this});
        this.editDialogFormVisible = true
      },

      showadduser() {
        //添加用户
        //获取所有的部门
        this.addDialogFormVisible = true;
        this.$store.dispatch("user/getDepart", {_this: this});
      },

      adduser() {
        this.$store.dispatch("user/addUser", {_this: this, form: this.addform});
      },

      showroles(user) {
        this.currentuser = user;

        this.$store.dispatch("user/getAllRoles", {_this: this,});
        this.$store.dispatch("user/getUser", {_this: this, id: user.id});
        //默认选中当前用户角色
        this.CheckedRolesIdList = this.RoleIdList;
        this.rolesDialogFormVisible = true;

      },

      setrole() {
        this.$store.dispatch('user/setRole', {
          _this: this,
          id: this.currentuser.id,
          rid_list: {roles: this.CheckedRolesIdList}
        })

      }


    },
    // watch:{
    //   CheckedRolesIdList(val){
    //     this.CheckedRolesIdList = val
    //   }

    // },

    computed: {

      ...mapGetters({
        UserList: 'user/getUserList',
        total: 'user/getTotal',
        DeptList: 'user/geDeptList',
        RoleList: 'user/getRolesList',
        RoleIdList: 'user/getRoleIdList',
        AllRoleList: 'user/getALLRolesList',
        AllRoleIdList: 'user/getAllRoleIdList',
        permissionDict: 'getPermission'
      }),

    }
  }
</script>

<style scoped>
  .box-card {
    height: 100%
  }

  .SearchRow {
    line-height: 80px;
  }

  .input-with-select {
    background-color: #fff;
    width: 330px;
  }

  .select-size {
    width: 514.5px;
  }

  .select-roles {
    width: 514.5px;
  }

</style>
