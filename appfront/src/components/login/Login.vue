<template>
  <div class="login">
    <el-form ref="form" :model="form" class="container" :rules="rules">
      <el-form-item class="avatar">
        <img src="@/assets/avatar.gif" alt="">
      </el-form-item>
      <el-form-item prop="username">
        <el-input v-model="form.username" placeholder="账号" prefix-icon="myicon myicon-user"></el-input>
      </el-form-item>
      <el-form-item prop="password">
        <el-input v-model="form.password" placeholder="密码" prefix-icon="myicon myicon-key"
                  @keydown.native.enter="loginSubmit('form')"></el-input>
      </el-form-item>
      <el-form-item prop="password">
        <el-button type="primary" class="login-btn" @click="loginSubmit('form')"
                   @keydown.native.enter="loginSubmit('form')">登录
        </el-button>
      </el-form-item>

    </el-form>
  </div>
</template>

<script>

  import setCookie from "@/utils/cookies.js"

  export default {
    name: "login",
    data: function () {
      return {
        form: {
          username: '',
          password: ''
        },
        rules: {
          username: [
            {required: true, message: '请输入用户名', trigger: 'blur'},
          ],
          password: [
            {required: true, message: '请输入密码', trigger: 'blur'},
          ]
        },
      }
    },
    //获取csrf先要发送get请求获取csrftoken
    // mounted() {
    //   this.$store.dispatch("getLoginAuth",this);
    // },

    methods: {

      loginSubmit(formName) {
        this.$refs[formName].validate(async (valid) => {
          if (valid) {
            const res = await this.$http.post('login', this.form);
            const {data, meta: {message, code}} = res.data;
            if (code === 2000) {

              //将token值存储在localStorage
              localStorage.setItem('token', data.token);
              // //设置cookie
              // document.cookie = "sessionId" + "=" + escape(data.permission_session_id);
              // setCookie('permission_session_id',data.permission_session_id)
              //验证成功后直接跳转到主页
              this.$router.push({name: 'home'});
              //登陆成功提示
              this.$message.success(message)
            } else {
              this.$message.warning(message)
            }

          } else {
            this.$message.warning("用户名或密码不能为空")
          }
        });
      }
    },

  }
</script>

<style scoped>
  .login {
    position: fixed;
    width: 100%;
    height: 100%;
    background-color: #2f4050;
  }

  .container {
    position: absolute;
    left: 0;
    right: 0;
    width: 400px;
    padding: 0px 40px 15px 40px;
    margin: 200px auto;
    background: white;
  }

  .avatar {
    position: relative;
    left: 50%;
    width: 120px;
    height: 120px;
    margin-left: -60px;
    margin-top: -60px;
    box-sizing: border-box;
    border-radius: 50%;
    border: 10px solid #fff;
    box-shadow: 0 1px 5px #ccc;
    overflow: hidden;
  }

  .login-btn {
    width: 100%;
  }


</style>
