<template>
<div>
  <el-container>
    <el-header>
      <navbar></navbar>
    </el-header>
    <el-container class="mid">
        <el-aside width="200px">
        <el-row class="tac">
        <el-col :span="12">
        <el-menu
            default-active="2"
            class="create_menu"
            @open="handleOpen"
            @close="handleClose"
            unique-opened=true>
            <el-menu-item index="1">
                <i class="el-icon-menu"></i>
                <span slot="title">用户管理</span>
            </el-menu-item>
            <el-menu-item index="2">
                <i class="el-icon-menu"></i>
                <span slot="title">文章管理</span>
            </el-menu-item>
            <el-menu-item index="3">
                <i class="el-icon-menu"></i>
                <span slot="title">资源管理</span>
            </el-menu-item>
            <el-menu-item index="4">
                <i class="el-icon-menu"></i>
                <span slot="title">评论管理</span>
            </el-menu-item>
            <el-menu-item index="5">
                <i class="el-icon-menu"></i>
                <span slot="title">创建管理员</span>
            </el-menu-item>
            <el-menu-item index="6">
                <i class="el-icon-menu"></i>
                <span slot="title">举报管理</span>
            </el-menu-item>
            <el-menu-item index="7">
                <i class="el-icon-menu"></i>
                <span slot="title">个人信息</span>
            </el-menu-item>
    </el-menu>
  </el-col>
</el-row>
        </el-aside>
        <el-container>
            <el-main>
                <adb></adb>
            </el-main>
        </el-container>
    </el-container>
    <el-footer></el-footer>
  </el-container>
</div>
</template>

<script>
export default {
  data () {
    return {
      
    }
  }
}
</script>


<style scoped>
  @import url("../assets/common.css");

  .el-aside {
      color: #333;
      padding-bottom:30px;
      height:1100px;
      border:1px solid #000;
      padding-top:0;
      margin-top:50px;
      overflow: hidden;
  }
  
  .el-main {
    color: #333;
    padding:10px 0 0 0; 
    height:1100px;
    border:1px solid #000;
    margin-top:50px;
  }
  
  .mid {
    margin-bottom: 40px;
    margin:0 auto;
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

</style>