<template>
  <div>
    <!-- 面包屑导航条 -->
    <MyBread level1="权限管理" level2="角色列表"></MyBread>
    <el-card class="card">
      <el-row>
        <el-col :span="4">
          <el-button type="primary" @click="addDialogVisible=true">添加角色</el-button>
        </el-col>
      </el-row>

      <el-table :data="RolesList" border stripe style="width: 100%">
        <el-table-column type="expand" width="150">
          <template slot-scope="scope">
            <el-row v-for="(item1,index) in scope.row.children" :key="index">
              <el-col :span="4">
                <el-tag type="warning" size="small">{{item1.title}}</el-tag>
                <i class="el-icon-d-arrow-right"></i>
              </el-col>

              <el-col :span="20">
                <el-row v-for="(item2,index) in item1.children" :key="index">
                  <el-col :span="4">
                    <el-tag @close="deleteRight(scope.row.id,item2.id)" closable type="success" size="small">
                      {{item2.title}}
                    </el-tag>
                    <i class="el-icon-d-arrow-right"></i>
                  </el-col>

                  <el-col :span="20">
                    <el-row v-for="(item3,index) in item2.children " :key="index">
                      <el-col :span="4">
                        <el-tag @close="deleteRight(scope.row.id,item3.id)" closable type="info" size="small">
                          {{item3.title}}
                        </el-tag>
                      </el-col>
                    </el-row>
                  </el-col>
                </el-row>
              </el-col>
            </el-row>

            <span v-if="scope.row.children.length === 0">该角色未分配权限</span>

          </template>


        </el-table-column>
        <el-table-column type="index">
        </el-table-column>
        <el-table-column prop="title" label="角色名称">
        </el-table-column>
        <el-table-column prop="desc" label="描述">
        </el-table-column>
        <el-table-column label="操作" width="350">
          <template slot-scope="scope">
            <el-button type="primary" plain icon="el-icon-edit" size="mini" @click="showEditDialog(scope.row.id)">编辑
            </el-button>
            <el-button type="danger" plain icon="el-icon-delete" size="mini" @click="remove(scope.row.id)">删除
            </el-button>
            <el-button type="warning" plain icon="el-icon-setting" size="mini"
                       @click="showSetRightDialog(scope.row)">
              分配权限
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 添加角色的对话框 -->
    <el-dialog title="添加新角色" :visible.sync="addDialogVisible" width="50%" @close="addDialogClosed"></el-dialog>

    <!-- 分配权限的对话框 -->
    <el-dialog title="分配权限" :visible.sync="setRightDialogVisible" width="50%">
      <!-- 树形结构组件 -->
      <!-- :data 用来指定当前这棵树，要绑定到的数据 -->
      <!-- node-key 用来指定，每个节点，被选中时候，所选中的哪个值 -->
      <!-- :props 用来指定每个节点的配置项 -->
      <!--     比如，通过 label 指定要展示的名称 -->
      <!--     比如，通过 children 属性指定 通过 哪个属性来实现嵌套 -->
      <!--<el-tree ref="tree" :data="RightsTree" node-key="id" :props="treeProps" show-checkbox :default-expand-all="true"-->
      <!--:default-checked-keys="defaultCheckedLeafKeys">-->

      <!--</el-tree>-->

      <el-tree
        ref="tree"
        :data="RightsTree"
        show-checkbox
        node-key="id"
        :default-expanded-keys="showCheckBoxArry"
        :default-checked-keys="defaultCheckedArray"
        :props="defaultProps"

      >
      </el-tree>
      {{permissionDict}}
      <span slot="footer" class="dialog-footer">
        <el-button @click="setRightDialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="updateRights">确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
  import {mapGetters} from 'vuex'

  export default {
    name: "Roles",
    data: function () {
      return {
        addDialogVisible: false,
        setRightDialogVisible: false,
        defaultProps: {
          children: 'children',
          label: 'title'
        },
        //默认展开
        showCheckBoxArry: [],
        //默认选中
        defaultCheckedArray: [],
        //用于确定更改权限使用的角色id
        currentRoleId: -1,


      }
    },
    created() {
      this.getRolesList();
      this.getRightsTree();
    },
    methods: {


      deleteRight(roleId, rightId) {
        console.log(roleId, rightId)

        //删除tag触发的事件,取消权限
        this.$store.dispatch('roles/deleteRight', {_this: this, roleId: roleId, rightId: rightId})
      },
      getRolesList() {
        this.$store.dispatch('roles/getRolesList', {_this: this})
      },

      getRightsTree() {
        this.$store.dispatch('rights/getRightsTree', {_this: this})
      },

      showEditDialog(id) {

      },
      remove(id) {

      },
      showSetRightDialog(role) {
        //分配权限

        this.$store.dispatch('rights/getRightsTree', {_this: this});
        //默认展开，默认展开的另一种简单方式设置属性 :default-expand-all
        let tempArray = [];
        this.RightsTree.forEach(item1 => {
          tempArray.push(item1.id)
          item1.children.forEach(item2 => {
            tempArray.push(item2.id)
            item2.children.forEach(item3 => {
              tempArray.push(item3.id)
            })
          })
        });
        this.showCheckBoxArry = tempArray;

        //获取默认选中的角色的权限id列表
        let tempArray2 = []
        role.children.forEach(item4 => {
          // tempArray2.push(item4.id)

          item4.children.forEach(item5 => {
            // tempArray2.push(item5.id)
            if (item5.children.length === 0) {
              //最后一层权限时类似于用户列表，没有添加用户这样的权限
              tempArray2.push(item5.id)

            } else {
              //最后一层权限有添加用户这样的权限
              item5.children.forEach(item6 => {
                tempArray2.push(item6.id)

              })

            }

          })
        });
        console.log('arrays', tempArray2)

        this.defaultCheckedArray = tempArray2;
        //给角色id赋值
        this.currentRoleId = role.id;
        //显示对话框
        this.setRightDialogVisible = true

      },
      updateRights() {
        //点击确定进行更新角色的权限
        //获取所有全选和半选的权限id

        //获取全选状态权限id的数组
        // let array1 = this.$refs.tree.getCheckedKeys();
        // //获取半选状态的权限id数组
        // let array2 = this.$refs.tree.getHalfCheckedKeys()
        // //合并数组
        // let array = [...array1,...array2]
        let rightIds = [];
        let array = this.$refs.tree.getCheckedNodes(false, true);
        array.forEach(item => {
          if (!item.is_menu) {
            rightIds.push(item.id)
          }
        });
        this.$store.dispatch("roles/updateRights", {_this: this, roleId: this.currentRoleId, rightIds: rightIds});


      },
      addDialogClosed() {

      },

    },
    computed: {
      ...mapGetters({
        RolesList: 'roles/getRolesList',
        RightsTree: 'rights/getRightsTree',

      }),


    }

  }
</script>

<style scoped>
  .card {
    margin-top: 15px;
  }

  .el-table__header th {
    padding: 0;
    line-height: 30px;
  }


</style>
