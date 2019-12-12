<template>
  <el-container class="container">
    <el-header class="header">
      <el-row>
        <el-col :span="4">
          <div class="grid-content bg-purple">

          </div>
        </el-col>
        <el-col :span="18">
          <div class="grid-content bg-purple-light">
            <h3 class="middle">YW公司CRM客户关系管理后台系统</h3>
          </div>
        </el-col>
        <el-col :span="4">
          <div class="grid-content bg-purple">
            <a href="#" @click.prevent="handleLogout()" class="logout">退出登陆</a>
          </div>
        </el-col>
      </el-row>
    </el-header>
    <el-container>
      <el-aside class="aside" width="200px">
        <!--开启路由模式-->
        <el-menu
          background-color="#545c64"
          text-color="#fff"
          active-text-color="#ffd04b"
          :unique-opened="true"
          :router="true"
        >
          <el-submenu v-for="(item,index) in menusList" :key="index" :index="''+item.id">
            <template slot="title">
              <i :class="item.icon"></i>
              <span>{{item.title}}</span>
            </template>
            <el-menu-item v-for="(item1,index) in item.children" :key="index" :index="item1.url">

              <span>{{item1.title}}</span>
            </el-menu-item>
          </el-submenu>

          <!--<el-submenu index="2">-->
            <!--<template slot="title">-->
              <!--<i class="el-icon-location"></i>-->
              <!--<span>权限管理</span>-->
            <!--</template>-->
            <!--<el-menu-item index="roles">-->
              <!--<i class="el-icon-location"></i>-->
              <!--<span>角色列表</span>-->
            <!--</el-menu-item>-->
            <!--<el-menu-item index="rights">-->
              <!--<i class="el-icon-location"></i>-->
              <!--<span>权限列表</span>-->
            <!--</el-menu-item>-->
          <!--</el-submenu>-->


        </el-menu>
      </el-aside>
      <el-main class="main">
        <router-view></router-view>
      </el-main>
    </el-container>
  </el-container>
</template>

<script>
  import {mapGetters} from 'vuex'

  export default {
    name: "Home",

    // //路由导航守卫无需再写这个方法
    // beforeCreate() {
    //   const token = localStorage.getItem('token');
    //   if (!token) {
    //     this.$router.push({name: 'login'})
    //   }
    // },

    created(){
      this.getMenus();
      this.getPermissions()
    },

    methods: {
      getMenus(){
        //动态获取左侧菜单
        this.$store.dispatch('homes/getMenu',{_this:this})

      },
      getPermissions(){
        //获取权限信息用于按钮权限检验
        this.$store.dispatch('getPermissions',{_this:this})
      },

      handleLogout() {
        //登出
        this.$router.push({name: 'login'})
      }
    },

    computed:{
      ...mapGetters({
        menusList:'homes/getMenu',
        // permissionDict:'homes/getPermission'
      })
    }
  }
</script>

<style scoped>
  .middle {
    text-align: center;
    margin-top: 0;

  }

  .logout {
    text-decoration: none;
  }

  .container {
    height: 100%;
  }

  .header {
    background-color: #B3C0D1;
    color: #333;
    text-align: center;
    line-height: 60px;
  }

  .aside {
    background-color: #D3DCE6;
    color: #333;
    text-align: center;
    line-height: 200px;
  }

  .main {
    background-color: #E9EEF3;
    color: #333;
    text-align: center;
    line-height: 160px;
    height: 100%;
  }


  /*.container {*/
  /*height: 100%;*/
  /*}*/
  /*.header {*/
  /*background-color: #B3C0D1;*/
  /*color: #333;*/
  /*text-align: center;*/

  /*}*/

  /*.aside {*/
  /*background-color: #D3DCE6;*/
  /*color: #333;*/
  /*text-align: center;*/
  /*}*/

  /*.main {*/
  /*background-color: #E9EEF3;*/
  /*color: #333;*/
  /*text-align: center;*/
  /*height: 100%;*/
  /*}*/


</style>
