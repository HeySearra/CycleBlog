<template>
<div id="search_top">
  <el-container>
    <el-header>
      <navbar ref="nav" @init="init"></navbar>
    </el-header>
    <div style="height:90px;width:100%"></div>
    <div style="width:35%;margin:0 auto;min-width:500px">
      <div style="float:left;margin-right:15px;width:78%">
        <el-input
          placeholder="请输入搜索内容"
          v-model="search_input"
          clearable
          @keyup.enter.native="click_search"
          maxLength="50">
        </el-input>
      </div>
    <el-button type="primary" style="width:15%;padding-left:0;padding-right:0" @click="click_search">搜索</el-button>
    </div>
    <div class="search_op" style="width:35%;margin:10px auto;min-width:500px">
      <div style="text-align:right;margin-right:1em;cursor:pointer" class="op_open_button" @click="open_op = !open_op"><i class="el-icon-arrow-down" v-if="!open_op"></i><i class="el-icon-arrow-up" v-if="open_op"></i> 搜索选项</div>
      <div id="search_op_form" style="display:none">
        <el-form ref="search_form" :model="search_form" label-width="100px" size="mini">
          <!-- <el-form-item label="搜索方式：" style="text-align:left">
            <el-radio v-model="search_form.type" :label="0">全文搜索</el-radio>
            <el-radio v-model="search_form.type" :label="1">仅标题</el-radio>
          </el-form-item> -->
          <el-form-item label="搜索范围：" style="text-align:left">
            <el-radio v-model="search_form.limit" :label="3">全部</el-radio>
            <el-radio v-model="search_form.limit" :label="2">仅文章</el-radio>
            <el-radio v-model="search_form.limit" :label="1">仅资源</el-radio>
          </el-form-item>
          <el-form-item label="搜索排序：" style="text-align:left">
            <el-radio v-model="search_form.order" :label="0">智能排序</el-radio>
            <el-radio v-model="search_form.order" :label="1">时间最近优先</el-radio>
            <el-radio v-model="search_form.order" :label="2">浏览量最多优先</el-radio>
          </el-form-item>
        </el-form>
      </div>
    </div>
    <el-container class="mid">
      <el-container>
        <el-main style="height:fit-content">
          <div style="height:50px" v-if="!list.length"></div>
          <div class="not_found" v-if="!list.length">找不到任何的内容</div>
          <div style="height:50px" v-if="!list.length"></div>
          <component v-for="item in list" :key="item.aid?item.aid+'aid':item.rid+'rid'" :is="item.aid?'arb':'rsb'" :aid="item.aid" :rid="item.rid" :cid="item.cid" ref="item" type="search" @done="loading_done_msg"></component>
          <div class="pagination" v-if="list.length&&total>page_size">
            <el-pagination
                background
                layout="total, prev, pager, next, jumper"
                :page-size="page_size"
                :total="total"
                :current-page="current_page"
                @current-change="change_page">
            </el-pagination>
          </div>
          <div style="height:10px" v-if="list.length&&total>page_size"></div>
        </el-main>
      </el-container>
      <el-aside width="300px" style="padding-top:50px !important;height:fit-content">
        <slb ref="tag_block" @change_tags="change_tags" title="标签筛选" type="choose"></slb>
        <lb v-if="false"></lb>
      </el-aside>
    </el-container>
    <el-footer></el-footer>
  </el-container>
  <el-progress :percentage="loading_percentage" class="loading_bar" :show-text="false"></el-progress>
</div>
</template>

<script>
export default {
  data () {
    return {
      keyword:'',
      search_input:'',
      search_form:{
        // type:0,
        limit:3,
        order:0
      },
      open_op:false,
      current_page:1,
      total:0,
      page_size:10,
      list:[],
      tags:[],
      chosen_tags:[],
      loading_percentage:0,
      loading_count:0,
      loading_first_done:30
    }
  },
  watch:{
    'open_op'(){
      if(this.open_op){
        $('#search_op_form').stop(true, false).slideDown(300);
      }
      else{
        $('#search_op_form').stop(true, false).slideUp(300);
      }
    },
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
    click_search(){
      if(this.search_input == ''){
        this.alert_msg.normal('请输入搜索内容');
        return;
      }
      this.$router.push({path:'/search',query:{data:this.search_input,li:this.search_form.limit, ord:this.search_form.order}})
      // this.init_new_search();
      this.init();
    },
    init(){
      this.keyword = this.$route.query?this.$route.query.data:'';
      $(window).scrollTop(0);
      $("aside").stop().animate({
          marginTop: 0
      });
      if(this.keyword!='' && this.keyword!=undefined){
        this.$refs.nav.set_search_word(this.keyword);
        this.search_input = this.keyword;
      }
      this.tags = [];
      this.search_form.limit = this.$route.query&&this.$route.query.li ? parseInt(this.$route.query.li) : 3;
      this.search_form.order = this.$route.query&&this.$route.query.ord ? parseInt(this.$route.query.ord) : 0;
      this.init_new_search();
      this.apply_for_info();
    },
    getCookie (name) {
        var value = '; ' + document.cookie
        var parts = value.split('; ' + name + '=')
        if (parts.length === 2) return parts.pop().split(';').shift()
    },
    apply_for_info(tags){
      var that = this;
      that.loading_start();
      var msg = that.search_form;
      msg.key = that.keyword;
      msg.tags = tags&&tags.length ? tags : [];
      msg.page = that.current_page;
      msg.each = that.page_size;
      $.ajax({ 
          type:'post', 
          url:"/search/main",
          headers: {'X-CSRFToken': this.getCookie('csrftoken')},
          data: JSON.stringify(msg),
          processData: false,
          contentType: false,
          success:function (res){ 
            that.list = res.result;
            that.tags = res.tags;
            that.total = res.amount;
            if(res.wrong_msg != ""){
              that.alert_msg.error(res.wrong_msg);
            }
            var keyword_array = that.keyword.trim().replace(new RegExp(/(\s)+/g)," ").split(' ');
            setTimeout(function(){
              if(that.list.length){
                var item = that.$refs.item;
                for(let i=0; i<item.length; i++){
                  item[i].init(keyword_array);
                }
              }
              else{
                that.loading_done();
              }
              if(!tags || !tags.length){
                that.$refs.tag_block.init(that.tags);
              }
            }, 0);
          },
          error:function(){
              that.alert_msg.error('连接失败');
              that.loading_done();
          }
      });
    },
    change_page(arg){
        this.current_page = arg;
        document.getElementById('search_top').scrollIntoView({behavior: 'smooth', block:'start'});
        this.apply_for_info(this.chosen_tags);
    },
    init_new_search(){
      this.current_page = 1;
      // this.search_form.limit = 3;
      // this.search_form.order = 0;
    },
    change_tags(tags){
      this.current_page = 1;
      this.chosen_tags = tags;
      $("aside").stop().animate({
          marginTop: 0
      });
      this.apply_for_info(tags);
    },
    loading_done_msg(){
          this.loading_count++;
          this.loading_percentage = this.loading_first_done + (this.loading_count/this.list.length)*(100-this.loading_first_done);
          if(this.loading_count == this.list.length){
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
              }, 690);
          }, 600);
      },
      loading_start(){
          this.loading_percentage = 10;
          this.loading_count = 0;
          $('.loading_bar').removeClass('loading_bar_done');
      }
  }
}
</script>


<style scoped>
@import url("../assets/common.css");
  body{
      scroll-behavior:smooth
  }

  .mid{
    margin-top:0 !important;
  }
  
  .el-aside {
    color: #333;
    padding-top:50px;
    padding-bottom:30px;
  }
  
  .el-main {
    color: #333;
    padding-top:0 !important;
    padding-bottom:0;
    margin-top:50px;
    height: fit-content;
  }
  
  .el-container:nth-child(5) .el-aside,
  .el-container:nth-child(6) .el-aside {
    line-height: 260px;
  }
  
  .el-container:nth-child(7) .el-aside {
    line-height: 320px;
  }

  .search_op{
    margin-top:20px;
    font-size:13px
  }

  .search_op>>>.el-form-item{
    margin-bottom:0
  }

  .op_open_button:hover{
    color:hsl(1, 69%, 69%);
  }

</style>