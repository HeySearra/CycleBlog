<template>
<div>
  <el-container>
    <el-header>
      <navbar></navbar>
    </el-header>
    <div class="title">
        <figure class="background"></figure>
        <el-row class="block-col-2 more_option">
            <el-col :span="12">
                <el-dropdown trigger="click" @command="click_dropdown">
                    <span class="el-dropdown-link">
                        <i class="el-icon-more" :src="porsrc"></i>
                    </span>
                    <el-dropdown-menu style="padding:3px 0" slot="dropdown">
                        <el-dropdown-item command="report">举报</el-dropdown-item>
                    </el-dropdown-menu>
                </el-dropdown>
            </el-col>
        </el-row>
        <div class="title_mid">
            <div class="portrait"><el-avatar :src="porsrc"></el-avatar></div>
            <div class="title_info">
                <h2><span :class="is_member?'member_color':''">{{name}}</span>
                    <svg t="1591730811752" class="icon" viewBox="0 0 1166 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="3370" v-if="is_member"><path d="M1073.152 219.307c-39.396 0-71.339 32.569-71.339 72.789 0 10.155 1.991 19.826 5.69 28.644l-232.449 98.417-163.413-286.52a73.244 73.244 0 0 0 30.748-59.876C642.39 32.569 610.475 0 571.08 0S499.74 32.569 499.74 72.76c0 24.605 11.976 46.308 30.265 59.535l-181.39 286.692-211.968-96.854c3.982-9.159 6.315-19.171 6.315-29.866 0-40.192-31.915-72.761-71.31-72.761S0 251.904 0 292.124c0 39.68 31.09 71.908 69.831 72.761L180.395 851.2c4.153 18.489 20.28 31.545 38.883 31.545h703.09c18.603 0 34.73-13.085 38.884-31.573l110.734-486.287h1.138c39.424 0 71.338-32.569 71.338-72.76 0-40.221-31.914-72.79-71.31-72.79zM890.766 801.28H251.051l-85.618-376.718 181.703 83.114a39.538 39.538 0 0 0 49.863-15.075L569.23 220.16l154.454 270.734c9.955 17.636 31.26 24.918 49.72 17.124L977.21 421.66l-86.443 379.62z m24.121 141.141l-687.957 0.171c-22.102 0-39.908 18.148-39.908 40.676 0 22.584 17.806 40.732 39.908 40.732l687.957-0.17c22.101 0 39.88-18.148 39.88-40.705s-17.779-40.704-39.88-40.704z" p-id="3371" fill="#daab1f"></path></svg>
                </h2>
                <div>{{intro}}</div>
            </div>
        </div>
    </div>
    <el-container class="mid">
        <el-container>
            <el-main style="height:fit-contnet">
                <h2 id="art">{{me}}的文章</h2>
                <div class="mid_user">
                    <div class="not_found" v-if="!art_list.length" style="height:100px;line-height:100px">
                        {{you}}还没有任何的文章
                    </div>
                    <arb type="view" v-for="item in art_list" :key="item.aid+'aid'" :aid="item.aid" ref="arb" :top="item.is_top"></arb>
                    <div class="pagination" v-if="art_list.length&&art_total>page_size" style="margin-bottom:20px">
                        <el-pagination
                            background
                            layout="total, prev, pager, next, jumper"
                            :page-size="page_size"
                            :total="art_total"
                            :current-page="art_current_page"
                            @current-change="art_change_page">
                        </el-pagination>
                        <div style="width:100%;height:10px"></div>
                    </div>
                </div>
                <h2 id="res">{{me}}的资源</h2>
                <div class="mid_user">
                    <div class="not_found" v-if="!res_list.length" style="height:100px;line-height:100px">
                        {{you}}还没有上传任何资源
                    </div>
                    <rsb type="view" v-for="item in res_list" :key="item+'rid'" :rid="item" ref="rsb"></rsb>
                    <div class="pagination" v-if="res_list.length&&res_total>page_size">
                        <el-pagination
                            background
                            layout="total, prev, pager, next, jumper"
                            :page-size="page_size"
                            :total="res_total"
                            :current-page="res_current_page"
                            @current-change="res_change_page">
                        </el-pagination>
                        <div style="width:100%;height:10px"></div>
                    </div>
                </div>
            </el-main>
        </el-container>
        <el-aside width="300px" style="padding-top:50px !important;height:fit-content">
            <div style="width:100%;height:36px"></div>
            <dab type="only_fans" :uid="parseInt(uid)" :class="login_manager.get_uid()==uid?'pointer':'curdef'" ref="dab"></dab>
            <udb :is_me="login_manager.get_uid() == uid" :detail="detail"></udb>
            <lb :title="me+'的收藏'" type="collection" edittitle="管理" :uid="parseInt(uid)" :editable="uid==login_manager.get_uid()" ref="clb"></lb>
            <lb :title="me+'的专栏'" type="special" edittitle="管理" :uid="parseInt(uid)" :editable="uid==login_manager.get_uid()" ref="slb"></lb>
        </el-aside>
        <el-dialog title="举报用户" :visible.sync="report_dialog">
            <div class="dialog-mid">
                <el-input
                    type="textarea"
                    :rows="5"
                    placeholder="请输入举报理由"
                    v-model="report"
                    resize="none">
                </el-input>
            </div>
            <div slot="footer" class="dialog-footer">
                <el-button @click="report_dialog = false">取 消</el-button>
                <el-button type="primary" @click="submit_report">确 定</el-button>
            </div>
        </el-dialog>
    </el-container>
    <el-footer></el-footer>
  </el-container>
</div>
</template>

<script>

export default {
    // name: 'user_info',
    data () {
        return {
            name:'',
            intro:'',
            art_list:[],
            res_list:[],
            uid:0,
            porsrc:'',
            me:'',
            you:'',
            detail:[],
            art_current_page:1,
            art_total:0,
            res_current_page:1,
            res_total:0,
            page_size:6,
            report:'',
            report_dialog:false,
            is_member:false
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
        var topPadding = 0;
        $(window).off('scroll');
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
                    if(newPosition > $("main").height() + topPadding  - $(window).height()-120){
                        let p = $("main").height() + topPadding  - $(window).height()-120;
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
                    var newPosition = ($(window).scrollTop() - offset.top) + topPadding - 35;
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
            this.uid = this.$route.params.id;
            if(this.uid == 0){
                this.$router.push({path:'/index'});
                return;
            }
            var that = this;
            setTimeout(function(){
                that.apply_for_info();
                that.$refs.dab.init();
                that.apply_for_article();
                that.apply_for_resource();
                that.$refs.clb.init();
                that.$refs.slb.init();
            }, 0);
        },
        getCookie (name) {
            var value = '; ' + document.cookie
            var parts = value.split('; ' + name + '=')
            if (parts.length === 2) return parts.pop().split(';').shift()
        },
        apply_for_info(){
            var that = this;
            $.ajax({ 
                type:'get', 
                url:'/user/info_card?uid='+that.uid,
                headers: {'X-CSRFToken': this.getCookie('csrftoken')}, 
                processData: false,
                contentType: false,
                success:function (res){ 
                    that.name = res.name;
                    document.title = res.name + ' 的个人空间';
                    that.intro = res.introduction;
                    that.porsrc = res.src;
                    that.detail = res.info;
                    if(that.login_manager.get_uid() != that.uid){
                        that.me = that.you = '';
                        for(let i=0; i<res.info.length; i++){
                            if(res.info[i].key == '性别'){
                                if(res.info[i].value == '男'){
                                    that.me = that.you = '他';
                                }
                                else if(res.info[i].value == '女'){
                                    that.me = that.you = '她';
                                }
                                break;
                            }
                        }
                        if(that.me.length == 0){
                            that.me = that.you = 'Ta ';
                        }
                    }
                    else{
                        that.me = '我';
                        that.you = '你';
                    }
                },
                error:function(){
                    that.alert_msg.error('信息加载失败');
                }
            });
        },
        apply_for_article(){
            var that = this;
            $.ajax({ 
                type:'get', 
                url:"/create/article/list?page="+that.art_current_page+'&each='+that.page_size+'&uid='+that.uid,
                headers: {'X-CSRFToken': this.getCookie('csrftoken')}, 
                processData: false,
                contentType: false,
                success:function (res){ 
                    that.art_list = res.article;
                    that.art_total = res.amount;
                    setTimeout(function(){
                        if(that.art_list.length){
                            var item = that.$refs.arb;
                            for(var i=0; i<item.length; i++){
                                item[i].init();
                            }
                        }
                    }, 0);
                },
                error:function(){
                    console.log('连接失败');
                }
            });
        },
        apply_for_resource(){
            var that = this;
            $.ajax({ 
                type:'get', 
                url:"/create/resource/upload_list?page="+that.art_current_page+'&each='+that.page_size+'&uid='+that.uid,
                headers: {'X-CSRFToken': this.getCookie('csrftoken')}, 
                processData: false,
                contentType: false,
                success:function (res){ 
                    that.res_list = res.rid;
                    that.res_total = res.amount;
                    setTimeout(function(){
                        if(that.res_list.length){
                            var item = that.$refs.rsb;
                            for(var i=0; i<item.length; i++){
                                item[i].init();
                            }
                        }
                    }, 0);
                },
                error:function(){
                    console.log('连接失败');
                }
            });
        },
        to_follow(){
            this.$router.push({path:'/create/follow'});
        },
        art_change_page(arg){
            this.art_current_page = arg;
            $(window).off('scroll');
            this.apply_for_article();
            document.getElementById('art').scrollIntoView({behavior: 'smooth', block:'start'});
        },
        res_change_page(arg){
            this.res_current_page = arg;
            $(window).off('scroll');
            this.apply_for_resource();
            document.getElementById('res').scrollIntoView({behavior: 'smooth', block:'start'});
        },
        click_dropdown(command){
            var that = this;
            if(command == 'report'){
                if(that.uid == that.login_manager.get_uid()){
                    that.alert_msg.warning('住手！别举报你自己');
                    return;
                }
                that.report = '';
                that.report_dialog = true;
            }
        },
        submit_report(){
            var that = this;
            $.ajax({ 
                type:'post', 
                url:"/user/complain",
                headers: {'X-CSRFToken': that.getCookie('csrftoken')}, 
                data: JSON.stringify({uid:that.uid, reason:that.report}),
                async:false,
                success:function (res){ 
                    if(res.status == 0){
                        that.alert_msg.success('举报成功');
                        that.report_dialog = false;
                    }
                    else{
                        that.alert_msg.error('举报失败');
                    }
                },
                error:function(){
                    that.alert_msg.error('连接失败');
                }
            });
        }
    }
}
</script>


<style scoped>
@import url("../assets/common.css");
  
  .el-container:nth-child(5) .el-aside,
  .el-container:nth-child(6) .el-aside {
    line-height: 260px;
  }
  
  .el-container:nth-child(7) .el-aside {
    line-height: 320px;
  }

  .pagination{
    margin-top:30px;
    text-align: center;
    font-weight: normal;
  }

  .title{
      position: absolute;
      background-color: #eee;
      width:100vw;
      left:0;
      height:300px;
      top:60px;
      min-width:1000px
  }

  .title_mid{
      margin-bottom: 40px;
      width:1100px;
      margin:0 auto;
      position: absolute;
      bottom:0;
      height:150px;
      left:calc(50% - 550px);
  }

  @media(max-width:1250px){
      .title_mid{
          width:900px;
          left:calc(50% - 450px);
      }
  }

  .title_mid>div{
      line-height: 150px;
      height:150px;
      float:left;
  }

  .portrait>span{
      vertical-align: middle;
      width:80px;
      height:80px;
      line-height: 80px;
  }

  .title_info{
      width:calc(100% - 110px);
      margin-left:30px;
  }

  .title_info>h2{
        height: 50px;
        line-height: 50px;
        margin: 34px 0 5px;
  }

  .title_info>div{
      line-height: 20px;
      font-size: 15px;
  }

  .mid{
      margin-top:362px !important;
  }

  .el-main{
      padding-top:50px !important;
      margin-top:0;
      height: fit-content;
      padding-bottom:0;
      box-shadow: none;
      background-color: rgba(0, 0, 0, 0);
  }

  .mid_user{
      box-shadow: 0 2px 12px 1px rgba(0, 0, 0, 0.1);
      background-color: #fff;
      border-radius: 1px;
      margin-bottom:30px
  }

  .more_option{
      position: absolute;
      bottom:10px;
      right:30px;
      width:auto;
      cursor: pointer;
  }

  .title{
      background-image: url("../assets/snow.jpg");
      background-position: center top;
      background-size: cover;
      background-repeat: no-repeat;
  }

  .icon{
      width:21px !important
  }
</style>