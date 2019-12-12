import Vue from 'vue'
import Router from 'vue-router'
import Login from '@/components/login/Login.vue'
import Home from '@/components/home/Home.vue'
import User from '@/components/user/User.vue'
import Rights from '@/components/power/Rights.vue'
import Roles from '@/components/power/Roles.vue'


import { Message } from 'element-ui'; //提示功能


const originalPush = Router.prototype.push
Router.prototype.push = function push(location) {
  return originalPush.call(this, location).catch(err => err)
}


Vue.use(Router);

const router = new Router({
  routes: [
    // {
    //   path: '/',
    //   redirect: '/user' // 如果用户访问的 / 根路径，则 重定向到 /login 页面
    // },
    {
      path: '/login',
      name: 'login',
      component: Login
    },

    {
      path: '/',
      name: 'home',
      component: Home,
      children: [
        {
          path: 'crm/user',
          name: 'user',
          component: User,
        },
        {
          path: 'rbac/rights/list',
          name: 'right',
          component: Rights,
        }, {
          path: 'rbac/roles',
          name: 'role',
          component: Roles,
        },
      ]
    },
  ]

});

//路由导航守卫
//在路由配置生效之前，判断token是否存在，这样home组建中不用写beforecreate()方法

router.beforeEach((to, from, next) => {
  //to 要去的路由配置
  //from 当前的路由配置
  //next 一定要调用，让to的路由配置继续生效，比如如果去登陆直接next(),否则判断token是否存在，如果存在就next()

  console.log(to)
  if (to.path === '/login') return next() ;//使用return，不需要写else

  //判断其他页面是否有token
  const token = localStorage.getItem('token');

  //存在继续往后走
  console.log(token)
  if (token) return next();


  // this.$router.push({name:'login'}) #没有this,无法使用
  Message.warning('未登录，请先登录！')
  router.push({
    name: 'login'
  })


});

export default router
