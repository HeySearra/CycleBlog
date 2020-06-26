<template>
    <div style="padding:10px 30px" :class="article.length==0?'':'bottom0'" id="amb">
        <div>
            <h2>我的文章</h2>
            <el-divider></el-divider>
            <div class="not_found" v-if="!article.length&&!loading">找不到任何的文章</div>
            <div v-if="loading" class="not_found">加载中 <i class="el-icon-loading"></i></div>
            <arb type="edit" v-for="item in article" :key="item.aid" :aid="item.aid" :top="item.is_top" ref="arb" @refresh="refresh" @done="loading_done_msg"></arb>
        </div>
        <div class="pagination" v-if="article.length!=0&&total>page_size">
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
    props: {
        current_page:{
            type:Number,
            default:1
        }
    },
    data () {
        return {
            page_size:7,
            total:0,
            article:[],
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
            this.apply_for_article_list();
        },
        apply_for_article_list(){
            var that = this;
            that.loading_start();
            $.ajax({ 
                type:'get', 
                url:"/create/article/list?page="+that.current_page+'&each='+that.page_size,
                headers: {'X-CSRFToken': this.getCookie('csrftoken')}, 
                processData: false,
                contentType: false,
                success:function (res){ 
                    that.article = res.article;
                    that.total = res.amount;
                    that.loading_percentage = that.loading_first_done;
                    that.loading = false;
                    setTimeout(function(){
                        if(that.article.length != 0){
                            var item = that.$refs.arb;
                            for(var i=0; i<item.length; i++){
                                item[i].init();
                            }
                        }
                        else{
                            that.loading_done();
                        }
                    }, 0);
                },
                error:function(){
                    console.log('连接失败');
                    that.loading_done();
                    that.loading = false;
                }
            });
        },
        getCookie (name) {
            var value = '; ' + document.cookie
            var parts = value.split('; ' + name + '=')
            if (parts.length === 2) return parts.pop().split(';').shift()
        },
        change_page(arg){
            this.current_page = arg;
            this.apply_for_article_list();
            document.getElementById('amb').scrollIntoView({behavior: 'smooth', block:'start'});
        },
        refresh(arg){
            if(true){
                if(this.article.length == 1){
                    this.current_page = this.current_page==1 ? 1 : this.current_page-1;
                }
                this.apply_for_article_list();
            }
        },
        loading_done_msg(){
            this.loading_count++;
            this.loading_percentage = this.loading_first_done + (this.loading_count/this.article.length)*(100-this.loading_first_done);
            if(this.loading_count == this.article.length){
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
    .pagination{
        margin-top:30px;
        text-align: center;
        font-weight: normal;
    }

    .bottom0>>>.el-divider{
        margin: 24px 0 0 !important;
    }
</style>

