<template>
<div>
  <el-container>
    <el-header>
      <navbar></navbar>
    </el-header>
    <div class="return_bar">
        <el-page-header @back="back" content="收藏管理"></el-page-header>
    </div>
    <el-container class="mid" style="padding-top: 0 !important;">
        <el-aside width="200px">
        <el-row class="tac">
        <el-col :span="12">
        <el-menu
            default-active="-1"
            class="create_menu"
            v-loading="loading">
            <el-menu-item index="0" @click="click_new">
                <div style="padding:0 20px">
                  <i class="el-icon-menu"></i>
                  <span slot="title">新建收藏夹</span>
                </div>
            </el-menu-item>
            <el-menu-item v-for="item in list" :index="''+item.index" :key="item.cid" @click="click_item(item.cid, item.title, item.condition)">
                <clb :cid="item.cid" :name="item.title" :count="item.count" :condition="item.condition" @edit="edit"></clb>
            </el-menu-item>
        </el-menu>
        </el-col>
        </el-row>
        </el-aside>
        <el-container>
            <el-main style="padding-top: 0 !important;">
                <cmb :name="name" :cid="cid" :condition="condition" ref="cmb" v-if="cid" @refresh="apply_for_info"></cmb>
            </el-main>
        </el-container>
    </el-container>
  </el-container>
  <el-dialog :title="dialog_title" :visible.sync="dialog" @closed="editing=false">
    <div class="dialog-mid">
        <el-form ref="new_form" :model="new_form" label-width="100px" class="form">
          <el-form-item label="名称">
            <el-input v-model="new_form.title" maxlength="20"></el-input>
          </el-form-item>
          <el-form-item label="可见性">
            <el-radio v-model="new_form.condition" :label="0">所有人可见</el-radio>
            <el-radio v-model="new_form.condition" :label="1">仅自己可见</el-radio>
          </el-form-item>
      </el-form>
    </div>
    <div slot="footer" class="dialog-footer">
        <el-button @click="dialog=false">取 消</el-button>
        <el-button type="primary" @click="click_confirm">确 定</el-button>
    </div>
  </el-dialog>
</div>
</template>

<script scoped>
export default {
  data () {
    return {
      new_form:{
        title:'',
        condition:0,
      },
      dialog:false,
      list:[],
      name:'',
      cid:0,
      dialog_title:'新建收藏夹',
      editing_cid:0,
      editing:false,
      condition:0,
      loading:true
    }
  },
  mounted(){
    this.init();
    document.documentElement.scrollTop = 0;
    $(window).off('scroll');
  },
  methods:{
    init(){
      if(!this.login_manager.get()){
        this.$router.push({path:'/index'});
        return;
      }
      this.index_order = 0;
      this.list = [];
      document.documentElement.scrollTop = 0;
      this.apply_for_info();
      if(this.cid != 0){
        this.$refs.cmb.init();
      }
    },
    apply_for_info(){
      var that = this;
      that.loading = true;
      $.ajax({ 
          type:'get', 
          url:"/collection/list",
          headers: {'X-CSRFToken': this.getCookie('csrftoken')}, 
          processData: false,
          contentType: false,
          success:function (res){ 
            let i = 1;
            for(var j=0; j<res.collections.length; j++){
              res.collections[j].index = i++;
            }
            setTimeout(function(){
              that.list = res.collections;
            }, 0);
            that.loading = false;
          },
          error:function(){
            that.alert_msg.error('连接失败');
          }
      });
    },
    back(){
      var from = this.$route.query.from;
      //console.log(from);
      if(from){
        this.$router.push({path:from});
      }
      else{
        this.$router.push({path:'/index'});
      }
    },
    click_new(){
      this.new_form.title = '';
      this.new_form.condition = 0;
      this.dialog_title = '新建收藏夹';
      this.dialog = true;
    },
    getCookie (name) {
        var value = '; ' + document.cookie
        var parts = value.split('; ' + name + '=')
        if (parts.length === 2) return parts.pop().split(';').shift()
    },
    new_collection(){
      var that = this;
      if(that.new_form.title.length > 20){
        that.alert_msg.warning('收藏夹名称不能多于 20 个字');
        return;
      }
      if(that.new_form.title.length == ''){
        that.alert_msg.warning('收藏夹名称不得为空');
        return;
      }
      $.ajax({ 
          type:'post', 
          url:"/collection/new",
          headers: {'X-CSRFToken': this.getCookie('csrftoken')}, 
          data: JSON.stringify(that.new_form),
          async:false,
          success:function (res){ 
              if(res.status == 0){
                that.alert_msg.success('新建收藏夹成功');
                that.dialog = false;
                that.init();
              }
              else{
                  switch(res.status){
                      case 1:
                          that.alert_msg.error('该收藏夹已存在');
                          break;
                      default:
                          that.alert_msg.error('新建收藏夹失败，请重试');
                  }
              }
          },
          error:function(){
              that.alert_msg.error('连接失败');
          }
      });
    },
    click_item(cid, name, condition){
      if(cid==0 || cid==this.cid){
        return;
      }
      this.cid = cid;
      this.name = name;
      this.condition = condition;
      var that = this;
      setTimeout(function(){
        that.$refs.cmb.init();
      }, 0);
    },
    click_confirm(){
      if(this.editing){
        this.submit_edit();
      }
      else{
        this.new_collection();
      }
    },
    edit(cid, name, condition){
      this.editing_cid = cid;
      this.new_form.title = name;
      this.new_form.condition = condition;
      this.dialog_title = '编辑 ' + name + ' 收藏夹';
      this.editing = true;
      this.dialog = true;
    },
    submit_edit(){
      var that = this;
      if(that.new_form.title.length > 20){
        that.alert_msg.warning('收藏夹名称不能多于 20 个字');
        return;
      }
      if(that.new_form.title.length == ''){
        that.alert_msg.warning('收藏夹名称不得为空');
        return;
      }
      var flag = true;
      $.ajax({ 
          type:'post', 
          url:"/collection/rename",
          headers: {'X-CSRFToken': this.getCookie('csrftoken')}, 
          data: JSON.stringify({cid:that.editing_cid, name:that.new_form.title}),
          async:false,
          success:function (res){ 
              if(res.status == 0){}
              else{
                  switch(res.status){
                      case 1:
                          that.alert_msg.error('收藏夹名字不得重复');
                          break;
                      default:
                          that.alert_msg.error('编辑收藏夹失败，请重试');
                  }
                  flag = false;
              }
          },
          error:function(){
              that.alert_msg.error('连接失败');
              flag = false;
          }
      });
      if(!flag){
        return;
      }
      $.ajax({ 
          type:'post', 
          url:"/collection/condition",
          headers: {'X-CSRFToken': this.getCookie('csrftoken')}, 
          data: JSON.stringify({cid:that.editing_cid, condition:that.new_form.condition}),
          async:false,
          success:function (res){ 
              if(res.status == 0){}
              else{
                  switch(res.status){
                      default:
                          that.alert_msg.error('编辑收藏夹失败，请重试');
                      flag = false;
                  }
              }
          },
          error:function(){
              that.alert_msg.error('连接失败');
              flag = false;
          }
      });
      if(flag){
        that.alert_msg.success('编辑成功');
        that.dialog = false;
        if(that.editing_cid == that.cid){
          that.condition = that.new_form.condition;
        }
        that.init();
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
      height:1100px;
      border-right:0;
      padding-top:0;
      overflow: hidden;
      background-color: #fff;
      margin-right:3px;
      box-shadow: none;
  }
  
  .el-main {
    color: #333;
    padding:10px 0 0 0; 
    height:1100px;
    background-color: #fff;
    box-shadow: none;
    margin-right:0;
    margin-top:0;
  }
  
  .mid {
    margin:0 auto !important;
    margin-bottom: 50px !important;
    box-shadow: 0 2px 12px 1px rgba(0, 0, 0, 0.1);
  }

  .el-menu-item{
    padding:0 !important;
    padding-left: 0;
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

  .el-menu>>>.el-submenu__title:hover, .el-menu-item:focus, .el-menu-item:hover{
    background-color: hsl(1, 64%, 93%);
  }

  .el-menu-item.is-active{
    background-color: hsl(1, 69%, 78%);
    color:#fff;
  }

  .el-menu>>>.el-menu-item.is-active a, .el-menu>>>.el-menu-item.is-active .el-dropdown{
    color:#fff;
  }

  .el-menu>>>.el-menu-item *{
    vertical-align: unset;
  }

  .el-menu>>>ul{
    box-shadow:inset 0px 15px 6px -15px rgba(0, 0, 0, 0.1), inset 0px -15px 6px -15px rgba(0, 0, 0, 0.1);
    border:1px 0 solid #ddd;
    background-color: hsl(1, 18%, 99%);
  }

  .return_bar{
      margin:100px auto 10px;
      width:1500px;
  }

  @media (max-width: 1500px){
    .return_bar{
        width:1250px;
    }
}

@media (max-width: 1300px){
    .return_bar{
        width:1000px;
    }
}

</style>