<template>
<div>
  <el-container>
    <el-header>
      <navbar></navbar>
    </el-header>
    <el-container class="mid">
        <el-aside width="200px" style="padding-top: 0 !important;">
        <el-row class="tac">
        <el-col :span="12">
        <el-menu
            :default-active="active"
            class="create_menu"
            :unique-opened="true">
            <el-submenu index="1">
                <template slot="title">
                    <i class="el-icon-edit"></i>
                    <span>文章管理</span>
                </template>
                  <router-link :to="{path:'/edit',query:{from:this.$route.path}}" tag="el-menu-item" index="1-1" class="sub">
                    <a href="javascript:void(0)" class="link">撰写文章</a>
                  </router-link>
                <el-menu-item index="1-2">
                  <router-link to="/create/article" class="sub">
                    <a href="javascript:void(0)" class="link">我的文章</a>
                  </router-link>
                </el-menu-item>
                <el-menu-item index="1-3">
                  <router-link to="/create/special" class="sub">
                    <a href="javascript:void(0)" class="link">我的专栏</a>
                  </router-link>
                </el-menu-item>
                <el-menu-item index="1-4">
                  <router-link to="/create/recycle" class="sub">
                    <a href="javascript:void(0)" class="link">回收站</a>
                  </router-link>
                </el-menu-item>
            </el-submenu>
            <el-submenu index="2">
                <template slot="title">
                    <i class="el-icon-document"></i>
                    <span>资源管理</span>
                </template>
                <el-menu-item index="2-1">
                  <router-link to="/create/resource/upload" class="sub">
                    <a href="javascript:void(0)" class="link">上传资源</a>
                  </router-link>
                </el-menu-item>
                <el-menu-item index="2-2">
                  <router-link to="/create/resource/upload_list" class="sub">
                    <a href="javascript:void(0)" class="link">上传明细</a>
                  </router-link>
                </el-menu-item>
                <el-menu-item index="2-3">
                  <router-link to="/create/resource/download" class="sub">
                    <a href="javascript:void(0)" class="link">下载明细</a>
                  </router-link>
                </el-menu-item>
                <el-menu-item index="2-4">
                  <router-link to="/create/point" class="sub">
                    <a href="javascript:void(0)" class="link">积分管理</a>
                  </router-link>
                </el-menu-item>
            </el-submenu>
            <el-menu-item index="3">
              <router-link :to="{path:'/collection',query:{from:$route.path}}">
                <a href="javascript:void(0)" class="link">
                  <i class="el-icon-star-off"></i>
                  <span slot="title">收藏管理</span>
                </a>
              </router-link>
            </el-menu-item>
            <el-submenu index="4">
                <template slot="title">
                    <i class="el-icon-bell"></i>
                    <span>关注管理</span>
                </template>
                <el-menu-item index="4-1">
                  <router-link to="/create/follows" class="sub">
                    <a href="javascript:void(0)" class="link">我的关注</a>
                  </router-link>
                </el-menu-item>
                <el-menu-item index="4-2">
                  <router-link to="/create/fans" class="sub">
                    <a href="javascript:void(0)" class="link">我的粉丝</a>
                  </router-link>
                </el-menu-item>
            </el-submenu>
            <el-menu-item index="6">
              <router-link to="/create/data">
                <a href="javascript:void(0)" class="link">
                  <i class="el-icon-copy-document"></i>
                  <span slot="title">数据中心</span>
                </a>
              </router-link>
            </el-menu-item>
            <el-menu-item index="7">
              <router-link to="/create/vip">
                <a href="javascript:void(0)" class="link">
                  <i class="el-icon-cpu"></i>
                  <span slot="title">VIP</span>
                </a>
              </router-link>
            </el-menu-item>
            <el-menu-item index="8">
              <router-link to="/create/message">
                <a href="javascript:void(0)" class="link">
                  <i class="el-icon-chat-line-square"></i>
                  <span slot="title">消息中心</span>
                </a>
              </router-link>
            </el-menu-item>
            <el-submenu index="9">
                <template slot="title">
                    <i class="el-icon-setting"></i>
                    <span>设置</span>
                </template>
                <el-menu-item index="9-1">
                  <router-link to="/create/setting/myinfo" class="sub">
                    <a href="javascript:void(0)" class="link">个人信息</a>
                  </router-link>
                </el-menu-item>
                <el-menu-item index="9-2">
                  <router-link to="/create/setting/account" class="sub">
                    <a href="javascript:void(0)" class="link">账号设置</a>
                  </router-link>
                </el-menu-item>
                <el-menu-item index="9-3" v-if="false">
                  <router-link to="/create/setting/diy" class="sub">
                    <a href="javascript:void(0)" class="link">定制页面</a>
                  </router-link>
                </el-menu-item>
            </el-submenu>
    </el-menu>
  </el-col>
</el-row>
        </el-aside>
        <el-container>
            <el-main style="padding-top: 0 !important;">
                <div class="child">
                  <router-view></router-view>
                </div>
            </el-main>
        </el-container>
    </el-container>
  </el-container>
</div>
</template>

<script>
export default {
  data () {
    return {
      path:this.$route.fullPath,
      active:''
    }
  },
  watch:{
        '$route'(to, from){
            this.change_active_item();
        }
    },
  mounted(){
    // if(!this.login_manager.get()){
    //   this.$router.push({path:'/index'});
    //   return;
    // }
    if(!this.login_manager.get()){
      this.$router.push({path:'/index'});
      return;
    }
    $(window).off('scroll');
    this.change_active_item();
    $(window).scroll(0);
    $("aside").css({
        marginTop: 0
    });
  },
  methods:{
    change_active_item(){
      let block = this.$route.name;
      switch(block){
        case 'create_article':
          this.active = '1-2';
          break;
        case 'create_special':
          this.active = '1-3';
          break;
        case 'create_recycle':
          this.active = '1-4';
          break;
        case 'create_resource_upload':
          this.active = '2-1';
          break;
        case 'create_resource_upload_list':
          this.active = '2-2';
          break;
        case 'create_resource_download':
          this.active = '2-3';
          break;
        case 'create_point':
          this.active = '2-4';
          break;
        case 'create_follows':
          this.active = '4-1';
          break;
        case 'create_fans':
          this.active = '4-2';
          break;
        case 'create_data':
          this.active = '6';
          break;
        case 'create_vip':
          this.active = '7';
          break;
        case 'create_message':
          this.active = '8';
          break;
        case 'create_setting_myinfo':
          this.active = '9-1';
          break;
        case 'create_setting_account':
          this.active = '9-2';
          break;
        case 'create_setting_diy':
          this.active = '9-3';
          break;
      }
    }
  }
}
</script>


<style scoped>
  @import url("../assets/common.css");

  .el-aside {
      color: #333;
      padding-bottom:30px;
      height:1250px;
      border-right:0;
      padding-top:0 !important;
      overflow: hidden;
      background-color: #fff;
      margin-right:3px;
      box-shadow: none;
  }
  
  .el-main {
    color: #333;
    padding:10px 0 0 0; 
    height:1250px;
    background-color: #fff;
    box-shadow: none;
    margin-right:0;
    margin-top:0;
  }
  
  .mid {
    margin:110px auto 50px !important;
    box-shadow: 0 2px 12px 1px rgba(0, 0, 0, 0.1);
  }
  
  .el-container:nth-child(5) .el-aside,
  .el-container:nth-child(6) .el-aside {
    line-height: 260px;
  }
  
  .el-container:nth-child(7) .el-aside {
    line-height: 320px;
  }

  .el-col-12{
      width:100% !important;
  }

  .el-menu{
      border:0;
  }

  .el-menu>>>.el-menu-item{
    padding-left:0 !important;
    padding-right:0 !important;
    margin:1px 0;
    color:#333;
  }

  .el-menu>>>.el-menu-item a{
    color:#333;
  }

  .link{
    text-decoration: none;
    display: inline-block;
    padding:0 20px;
    width:100%;
  }

  .sub .link{
    padding:0 40px;
  }

  .el-menu>>>.el-submenu__title:hover, .el-menu-item:focus, .el-menu-item:hover{
    background-color: hsl(1, 64%, 93%);
  }

  .el-menu-item.is-active{
    background-color: hsl(1, 69%, 78%);
  }

  .el-menu-item.is-active a{
    color:#fff;
  }

  .el-menu>>>ul{
    box-shadow:inset 0px 15px 6px -15px rgba(0, 0, 0, 0.1), inset 0px -15px 6px -15px rgba(0, 0, 0, 0.1);
    border:1px 0 solid #ddd;
    background-color: hsl(1, 18%, 99%);
  }

</style>