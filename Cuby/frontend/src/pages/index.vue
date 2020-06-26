<template>
<div>
  <el-container>
    <el-header>
      <navbar></navbar>
    </el-header>
    <el-container class="mid">
      <el-container>
        <div v-if="name != ''" class="hello">
          <h1 style="font-size:30px;line-height:50px" :class="is_member?'member_color':''" @click="$router.push({path:'/userInfo/'+uid})">Hi！{{name}}</h1>
        </div>
      </el-container>
    </el-container>
    <el-container class="mid" :style="name!=''?'margin-top:0 !important':''">
      <el-container>
        <el-main style="height:fit-content;padding-top:0 !important;padding-bottom:0;height:fit-content">
          <router-view></router-view>
        </el-main>
      </el-container>
      <el-aside width="300px" style="height:fit-content">
        <crb ref="crb"></crb>
        <dab ref="dab" v-if="login_manager.get()"></dab>
        <slb ref="tag_block" title="热门标签" type="hot"></slb>
        <vcb ref="vcb" v-if="login_manager.get() && false"></vcb>
      </el-aside>
    </el-container>
    <el-footer></el-footer>
  </el-container>
</div>
</template>

<script scoped>
export default {
  name: 'index',
  data () {
    return {
      visible:false,
      //init_flag:false,
      name:'',
      uid:0,
      is_member:false
    }
  },
  mounted(){
    this.init();
    var documentHeight = 0;
    $("aside").css({
        marginTop: 0
    });
    var topPadding = 15;
    $(function() {
        var offset = $("aside").offset();
        documentHeight = $(document).height();
        $(window).off('scroll');
        $(window).scroll(function() {
            var sideBarHeight = $("aside").height();
            if($("aside").height() >= $("main").height()){
              return;
            }
            if($(window).height() <= $("aside").height()+topPadding){
              if ($(window).scrollTop()+$(window).height() > offset.top+$("aside").height()) {
                  var newPosition = ($(window).scrollTop() - offset.top + $(window).height() - $("aside").height()) - 50;
                  if(newPosition > $("main").height() + topPadding  - $(window).height() + 60){
                    let p = $("main").height() + topPadding  - $(window).height() + 60;
                    $("aside").stop().animate({
                        marginTop: p
                    });
                  }
                  else{
                    $("aside").stop().animate({
                        marginTop: newPosition
                    });
                  }
              }
              else {
                  $("aside").stop().animate({
                      marginTop: 0
                  });
              };
            }
            else{
              if($(window).scrollTop()>offset.top){
                var newPosition = ($(window).scrollTop() - offset.top) + topPadding + 60;
                $("aside").stop().animate({
                    marginTop: newPosition
                });
              }
              else {
                $("aside").stop().animate({
                    marginTop: 0
                });
              }
            }
        });
    });
  },
  methods:{
    init(){
      this.init_params();
      this.$refs.tag_block.init();
      // this.$refs.crb.init();
      if(this.login_manager.get()){
        this.apply_for_name();
        this.$refs.dab.init();
      }
      // this.$refs.vcb.init();
      document.documentElement.scrollTop = 0;
    },
    getCookie (name) {
        var value = '; ' + document.cookie
        var parts = value.split('; ' + name + '=')
        if (parts.length === 2) return parts.pop().split(';').shift()
    },
    init_params(){
      this.current_page = 0;
      this.total = 0;
      this.is_final = false;
      this.list = [];
    },
    
    apply_for_name(){
      var that = this;
      that.name = that.login_manager.get() ? that.login_manager.get_name() : '';
      $.ajax({ 
          type:'get', 
          url:'/simple_user_info',
          headers: {'X-CSRFToken': this.getCookie('csrftoken')}, 
          processData: false,
          contentType: false,
          success:function (res){ 
            if(res.uid){
              that.name = res.name;
              that.uid = res.uid;
              that.is_member = res.is_member;
            }
          },
          error:function(){
            that.name = '';
          }
      });
    },
  }
}
</script>


<style>
@import url("../assets/common.css");

  .el-aside {
    color: #333;
    padding-top:0 !important;
    padding-bottom:30px;
  }
  
  .el-main {
    color: #333;
    padding-top:50px;
  }
  
  .el-container:nth-child(5) .el-aside,
  .el-container:nth-child(6) .el-aside {
    line-height: 260px;
  }
  
  .el-container:nth-child(7) .el-aside {
    line-height: 320px;
  }

  .hello{
    text-align:center;
    width: 100%;
  }

  .hello h1{
    cursor: pointer;
    transition:0.3s all ease-in-out;
  }

  .hello h1:hover{
    color:hsl(1, 69%, 69%);
  }

  .pagination{
    margin-top:30px;
    text-align: center;
    font-weight: normal;
  }
</style>