// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import store from './store/index'
import MyServerHttp from './plugins/http.js'
import MyBread from '@/components/common/MyBread.vue'
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css'; //样式文件单独引入

Vue.use(ElementUI); //全局注册

Vue.use(MyServerHttp);
Vue.component("MyBread", MyBread);//全局自定义组件

Vue.config.productionTip = false;


/* eslint-disable no-new */
var vm = new Vue({
  el: '#app',
  router,
  store,
  components: {App},
  template: '<App/>'
});




