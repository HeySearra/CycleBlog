<template>
    <div style="padding:10px 30px" :class="list.length==0?'':'bottom0'">
        <div>
            <h2>我的粉丝</h2>
            <el-divider></el-divider>
            <div v-if="!list.length&&!loading" class="not_found">你还没有任何的粉丝</div>
            <div v-if="loading" class="not_found">加载中 <i class="el-icon-loading"></i></div>
            <div v-for="item in list" :key="item" class="margin0">
                <ulb type="view" :uid="item" ref="ulb" @done="loading_done_msg"></ulb>
                <el-divider class="margin0"></el-divider>
            </div>
        </div>
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
        <el-progress :percentage="loading_percentage" class="loading_bar" :show-text="false"></el-progress>
    </div>
</template>

<script>
export default {
    data () {
        return {
            current_page:1,
            total:0,
            page_size:10,
            list:[],
            loading:true,
            loading_percentage:0,
            loading_count:0,
            loading_first_done:30,
        }
    },
    mounted(){
        this.init();
    },
    methods:{
        init(){
            if(!this.login_manager.get()){
                this.$router.push({path:'/index'});
                return;
            }
            this.apply_for_info();
        },
        getCookie (name) {
            var value = '; ' + document.cookie
            var parts = value.split('; ' + name + '=')
            if (parts.length === 2) return parts.pop().split(';').shift()
        },
        apply_for_info(){
            var that = this;
            that.loading_start();
            that.loading = true;
            $.ajax({ 
                type:'get', 
                url:'/create/fans?page='+that.current_page+'&each='+that.page_size,
                headers: {'X-CSRFToken': this.getCookie('csrftoken')}, 
                processData: false,
                contentType: false,
                success:function (res){ 
                    that.list = res.uid;
                    that.total = res.amount;
                    setTimeout(function(){
                        if(that.list.length != 0){
                            var item = that.$refs.ulb;
                            for(var i=0; i<item.length; i++){
                                item[i].init();
                            }
                        }
                        else{
                            that.loading_done();
                        }
                    }, 0);
                    that.loading = false;
                },
                error:function(){
                    console.log('连接失败');
                    that.loading = false;
                }
            });
        },
        change_page(arg){
            this.current_page = arg;
            this.apply_for_info();
            document.documentElement.scrollTop = 0;
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
@import "../assets/side_block.css";
    body{
        scroll-behavior:smooth
    }

  .pagination{
    margin-top:30px;
    text-align: center;
    font-weight: normal;
  }

  .bottom0>>>.el-divider{
    margin: 24px 0 0;
  }

  .margin0 .el-divider{
      margin:0;
  }
</style>

