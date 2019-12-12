import axios from 'axios'
import {Message} from 'element-ui';

// const MyHttpServer = {};

// MyHttpServer.install = (Vue) => {
//
//   // axios.baseURL = 'http://127.0.0.1:8000/';
//
//   //添加实例方法
//   Vue.prototype.$http = axios
//
// };
//
// export default MyHttpServer


// 设置基础apiUrl
axios.defaults.baseURL = 'http://127.0.0.1:8000/';

axios.defaults.withCredentials = true; // 允许携带cookie


// 拦截request,/ 添加请求拦截器
axios.interceptors.request.use(function (config) {
  // 在发送请求之前做些什么
  if (config.url !== "login") {
    config.headers['Authorization'] = localStorage.getItem("token");
  }

  return config;
}, function (error) {
  // 对请求错误做些什么
  return Promise.reject(error);
});
//
// 添加响应拦截器
axios.interceptors.response.use(function (response) {
  // 对响应数据做点什么

  // const res = response.data;
   console.log('response',response)

  // if (res.count) return response
  //
  // if (res.meta.code) {
  //   if (res.meta.code === 2002) {
  //     //如果返回的code === 2002,就返回无权限查看内容，不需要将整个response返回
  //     Message.warning("无权查看对应数据")
  //   }
  //   return response
  //
  // } else {
  //   return response;
  // }
  return response
}, function (error) {
  // 对响应错误做点什么
  return Promise.reject(error);
});


export default {
  install: function (Vue) {
    Object.defineProperty(Vue.prototype, '$http', {value: axios})
  }
}
