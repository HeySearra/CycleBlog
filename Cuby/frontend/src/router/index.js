import Vue from 'vue'
import Router from 'vue-router'
import index from '@/pages/index.vue'
import search from '@/pages/search.vue'
import article_block from '@/components/subscribe_manager_block.vue'
import create from '@/pages/create.vue'
import user_info from '@/pages/user_info.vue'
import login from '@/pages/login.vue'
import register from '@/pages/register.vue'
import article from '@/pages/article.vue'
import collection from '@/pages/collection.vue'
import edit from '@/pages/edit_article.vue'
import administrator from '@/pages/administrator.vue'
import resource from '@/pages/resource.vue'
import page404 from '@/pages/404.vue'

import amb from '@/components/article_manager_block';
import smb from '@/components/special_manager_block';
import rbmb from '@/components/recycle_bin_manager_block';
import urb from '@/components/upload_resource_block';
import urmb from '@/components/upload_resource_manager_block';
import drmb from '@/components/download_resource_manager_block';
import fmb from '@/components/fans_manager_block';
import vmb from '@/components/vip_manager_block';
import mb from '@/components/myinfo_block';
import sdb from '@/components/setting_diy_block';
import sab from '@/components/setting_account_block';
import ssmb from '@/components/subscribe_manager_block';
import msb from '@/components/message_block';
import cmb from '@/components/collection_manager_block';
import pb from '@/components/point_block';
import rec from '@/components/recommend';
import fn from '@/components/follow_new';
import hot from '@/components/hot';
import dmb from '@/components/data_manager';
//import login from './components/login_block';


const originalPush = Router.prototype.push
Router.prototype.push = function push(location) {
  return originalPush.call(this, location).catch(err => err)
}

Vue.use(Router)

const router =  new Router({
  mode: 'history',//改成history模式
  routes: [
    {
      path: '/',
      redirect:'/index',
    },
    {
      path: '/index',
      name: 'index',
      component: index,
      children:[
        {
          path:'/',
          name: 'index',
          component:rec,
          meta:{
            title:'Cuby 创造你的博客空间',
          }
        },
        {
          path:'/index/new',
          name: 'follow_new',
          component:fn,
          meta:{
            title:'Cuby 关注动态',
          }
        },
        {
          path:'/index/hotart',
          name: 'hot',
          component:hot,
          meta:{
            title:'Cuby 热门文章',
          }
        },
        {
          path: '*',
          redirect:'/404'
        }
      ]
    },
    // {
    //   path: '/cl',
    //   name: 'article_block',
    //   component: article_block,
    //   meta:{
    //     title:'Cuby 浏览文章',
    //   }
    // },
    {
      path: '/search',
      name: 'search',
      component: search,
      meta:{
        title:'Cuby 搜索',
      }
    },
    {
      path: '/create',
      name: 'create',
      component: create,
      children:[
        {
          path:'/create/',
          redirect:'/create/article',
        },
        {
          name:'create_article',
          path:'/create/article',
          component: amb,
          meta:{
            title:'Cuby 我的文章',
          }
        },
        {
          name:'create_special',
          path:'/create/special',
          component:smb,
          meta:{
            title:'Cuby 我的专栏',
          }
        },
        {
          name:'create_recycle',
          path:'/create/recycle',
          component:rbmb,
          meta:{
            title:'Cuby 回收站',
          }
        },
        {
          name:'create_resource_upload',
          path:'/create/resource/upload',
          component:urb,
          meta:{
            title:'Cuby 上传资源',
          }
        },
        {
          name:'create_resource_upload_list',
          path:'/create/resource/upload_list',
          component:urmb,
          meta:{
            title:'Cuby 上传明细',
          }
        },
        {
          name:'create_resource_download',
          path:'/create/resource/download',
          component:drmb,
          meta:{
            title:'Cuby 下载明细',
          }
        },
        {
          name:'create_point',
          path:'/create/point',
          component:pb,
          meta:{
            title:'Cuby 积分管理',
          }
        },
        {
          name:'create_follows',
          path:'/create/follows',
          component:ssmb,
          meta:{
            title:'Cuby 我的关注',
          }
        },
        {
          name:'create_fans',
          path:'/create/fans',
          component:fmb,
          meta:{
            title:'Cuby 我的粉丝',
          }
        },
        {
          name:'create_data',
          path:'/create/data',
          component: dmb,
          meta:{
            title:'Cuby 数据中心',
          }
        },
        {
          name:'create_vip',
          path:'/create/vip',
          component:vmb,
          meta:{
            title:'Cuby 会员',
          }
        },
        {
          name:'create_message',
          path:'/create/message',
          component:msb,
          meta:{
            title:'Cuby 消息中心',
          }
        },
        {
          name:'create_setting_myinfo',
          path:'/create/setting/myinfo',
          component:mb,
          meta:{
            title:'Cuby 个人信息',
          }
        },
        {
          name:'create_setting_account',
          path:'/create/setting/account',
          component:sab,
          meta:{
            title:'Cuby 账号设置',
          }
        },
        // {
        //   name:'create_setting_diy',
        //   path:'/create/setting/diy',
        //   component:sdb,
        //   meta:{
        //     title:'Cuby 定制页面',
        //   }
        // },
        {
          path: '*',
          redirect:'/404'
        }
      ]
    },
    {
      path: '/userInfo/:id',
      name: 'userInfo',
      component: user_info,
      meta:{
        title:'Cuby 个人空间',
      }
    },
    {
      path: '/login',
      name: 'login',
      component: login,
      meta:{
        title:'Cuby 登录',
      }
    },
    {
      path: '/register',
      name: 'register',
      component: register,
      meta:{
        title:'Cuby 注册',
      }
    },
    {
      path: '/article/:id',
      name: 'article',
      component: article,
      meta:{
        title:'Cuby 文章',
      }
    },
    {
      path: '/collection',
      name: 'collection',
      component: collection,
      children:[
        {
          path:'/collection/:cid',
          component:cmb,
          meta:{
            title:'Cuby 收藏夹',
          }
        }
      ]
    },
    {
      path: '/edit/:id',
      name: 'edit',
      component: edit,
      meta:{
        title:'Cuby 撰写文章',
      }
    },
    {
      path: '/edit',
      name: 'edit',
      component: edit,
      meta:{
        title:'Cuby 撰写文章',
      }
    },
    // {
    //   path: '/administrator',
    //   name: 'administrator',
    //   component: administrator,
    //   meta:{
    //     title:'Cuby 后台管理',
    //   }
    // },
    {
      path: '/resource/:id',
      name: 'resource',
      component: resource,
      meta:{
        title:'Cuby 资源',
      }
    },
    {
      path: '/404',
      name: 'page404',
      component: page404,
      meta:{
        title:'Cuby 找不到页面',
      }
    },
    {
      path: '*',
      redirect:'/404'
    }
  ],
});

export default router;
