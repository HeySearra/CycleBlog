<template>
    <div style="padding:10px 30px" :class="list.length==0?'':'bottom0'">
        <div>
            <h2>回收站</h2>
            <el-divider></el-divider>
            <div class="not_found" v-if="!list.length&&!loading">找不到任何的文章</div>
            <div v-if="loading" class="not_found">加载中 <i class="el-icon-loading"></i></div>
            <arb type="recycle" ref="arb" v-for="item in list" :key="item" :aid="item" @refresh="refresh" @done="loading_done_msg"></arb>
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
    name: 'rbb',
    data () {
        return {
            no_article:false,
            page_size:7,
            total:0,
            current_page:1,
            list:[],
            loading_percentage:0,
            loading_count:0,
            loading_first_done:30,
            loading:true
        }
    },
    mounted(){
        $(window).scroll(0);
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
            $.ajax({ 
                type:'get', 
                url:"/create/recycle/list?page="+that.current_page+'&each='+that.page_size,
                headers: {'X-CSRFToken': this.getCookie('csrftoken')}, 
                processData: false,
                contentType: false,
                success:function (res){ 
                    that.list = res.article;
                    that.total = res.amount;
                    that.loading_percentage = that.loading_first_done;
                    setTimeout(function(){
                        if(that.list.length != 0){
                            var item = that.$refs.arb;
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
                    that.loading_done();
                    that.loading = false;
                }
            });
        },
        change_page(arg){
            this.current_page = arg;
            this.apply_for_info();
            document.documentElement.scrollTop = 0;
        },
        refresh(arg){
            if(true){
                if(this.list.length == 1){
                    this.current_page = this.current_page==1 ? 1 : this.current_page-1;
                }
                this.apply_for_info();
            }
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
            this.loading = true;
            $('.loading_bar').removeClass('loading_bar_done');
        }
    }
}
</script>

<style scoped>
    body{
        scroll-behavior:smooth
    }

    .pagination{
        margin-top:30px;
        text-align: center;
        font-weight: normal;
    }

    .not_found{
        text-align: center;
        color: #aaa;
    }

    .bottom0>>>.el-divider{
        margin: 24px 0 0 !important;
    }
</style>

