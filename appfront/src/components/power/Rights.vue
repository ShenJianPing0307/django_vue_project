<template>
  <div>
    <!--面包屑-->
    <MyBread level1="权限管理" level2="权限列表"></MyBread>
    <!-- 卡片视图 -->
    <el-card class="card">
      <el-table
        :data="RightsList"
        border
        stripe
        style="width: 100%">
        <el-table-column type="index"></el-table-column>
        <el-table-column label="权限名称" prop="title"></el-table-column>
        <el-table-column label="路径" prop="url"></el-table-column>
        <el-table-column label="操作方法" prop="action"></el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script>
  import {mapGetters} from 'vuex'


  export default {
    name: "Rights",
    data: function () {
      return {
        // RightsList:[]
      }
    },

    created() {
      this.getRightsList()
    },

    methods: {
      getRightsList() {
        this.$store.dispatch('rights/getRightsList', {_this: this})
        //
        // const res = await this.$http.get("rbac/rights/list");
        //  const {data, meta: {message, code}} = res.data;
        //  if(code === 2000){
        //    this.RightsList = data
        // context.commit("GETRIGHTLIST",data)
        // }
      }
    },


    computed: {

      ...mapGetters({
        RightsList: 'rights/getRightsList'

      })

    }

  }
</script>

<style scoped>
.card {
  margin-top: 15px;
}
</style>
