<template>
<div>
  <el-container>
    <el-header>
      <navbar></navbar>
    </el-header>
    <el-container class="mid">
      <el-container>
        <el-main style="height:fit-content">
            <full-article ref="full_article" :aid="parseInt(aid)" @init_author_card="init_author_info" @done="loading_done_msg(40)"></full-article>
            <div style="height:15px" class="clear_both"></div>
            <comment :aid="parseInt(aid)" ref="comment" @done="loading_done_msg(30)"></comment>
        </el-main>
      </el-container>
      <el-aside width="300px" style="padding-top:50px !important;height:fit-content">
        <aib :uid="parseInt(uid)" :aid="parseInt(aid)" ref="aib"></aib>
        <lb title="作者专栏" type="special" ref="slb" :uid="parseInt(uid)"></lb>
        <lb title="相关文章" type="relative_article" ref="rlb"></lb>
      </el-aside>
    </el-container>
    <el-footer></el-footer>
    <el-progress :percentage="loading_percentage" class="loading_bar" :show-text="false"></el-progress>
  </el-container>
</div>
</template>

<script>
export default {
  data () {
    return {
      aid:0,
      uid:0,
      loading_percentage:0,
      loading_count:0,
      loading_first_done:30,
    }
  },
  watch:{
      '$route'(to, from){
          if(to.name==from.name && to.params.id!=from.params.id){
              this.init();
              document.documentElement.scrollTop = 0;
          }
      }
  },
  mounted(){
    this.init();
    document.documentElement.scrollTop = 0;
    var documentHeight = 0;
    var topPadding = 25;
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
                  if(newPosition > $("main").height() + topPadding  - $(window).height() + 10){
                    let p = $("main").height() + topPadding  - $(window).height() + 10;
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
                var newPosition = ($(window).scrollTop() - offset.top) + topPadding;
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
      this.aid = this.$route.params.id;
      this.loading_start();
      if(parseInt(this.aid) <= 0){
        this.alert_msg.error('刚刚似乎打开了错误的页面');
        var that = this;
        setTimeout(function(){
          that.$router.push({path:'/index'});
        }, 0);
        return;
      }
      var that = this;
      setTimeout(function(){
        that.$refs.full_article.init();
        that.$refs.comment.init();
        that.$refs.rlb.init(that.aid, undefined);
      }, 0)
    },
    init_author_info(uid){
      this.uid = uid;
      var that = this;
      setTimeout(function(){
        that.$refs.aib.init();
        that.$refs.slb.init();
      }, 0);
    },

    loading_done_msg(add){
        this.loading_count++;
        this.loading_percentage = this.loading_percentage + add;
        if(this.loading_percentage >= 100){
            this.loading_done();
        }
    },
    loading_done(){
        this.loading_percentage = 100;
        var that = this;
        setTimeout(function(){
            $('.loading_bar').addClass('loading_bar_done');
            setTimeout(function(){
                that.loading_percentage = 0;
                that.loading_count = 0;
            }, 560);
        }, 500);
    },
    loading_start(){
        this.loading_percentage = this.loading_first_done;
        this.loading_count = 0;
        $('.loading_bar').removeClass('loading_bar_done');
    }
  }
}
</script>


<style scoped>
@import url("../assets/common.css");
  .el-aside {
    color: #333;
    padding-top:50px !important;
    padding-bottom:30px;
  }
  
  .el-main {
    color: #333;
    background-color: #fff;
    margin-top:50px;
  }
  
  .el-container:nth-child(5) .el-aside,
  .el-container:nth-child(6) .el-aside {
    line-height: 260px;
  }
  
  .el-container:nth-child(7) .el-aside {
    line-height: 320px;
  }

</style>