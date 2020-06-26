<template>
    <div style="padding:10px 30px" class="cmb" :class="!list.length||loading?'':'bottom0'">
        <div>
            <h2>{{name}} <i v-if="condition!=0" class="iconfont icon-eye-close" style="margin-left:1em;color:#aaa;font-weight:normal"></i></h2>
            <el-divider></el-divider>
            <div class="not_found" v-if="!list.length&&!loading">收藏夹空空如也</div>
            <div v-if="loading" class="not_found">加载中 <i class="el-icon-loading"></i></div>
            <component v-for="item in list" :key="item.aid?item.aid+'aid':item.rid+'rid'" :is="item.aid?'arb':'rsb'" :aid="item.aid" :rid="item.rid" :cid="item.cid" ref="item" type="collection" @open_move_window="open_move_window" @done="loading_done_msg"></component>
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
        <el-dialog title="" :visible.sync="dialogVisible">
            <div class="dialog-mid">
                <cocb :cid="cid" :aid="change_aid" :rid="change_rid" ref="cocb"></cocb>
            </div>
            <div slot="footer" class="dialog-footer">
                <el-button @click="dialogVisible = false">取 消</el-button>
                <el-button type="primary" @click="change_collection">确 定</el-button>
            </div>
        </el-dialog>
        <el-progress :percentage="loading_percentage" class="loading_bar" :show-text="false"></el-progress>
    </div>
</template>

<script>
export default {
    props: {
        current_page:{
            type:Number,
            default:1
        },
        cid:{
            type:Number,
            default:0
        },
        name:{
            type:String,
            default:'默认收藏夹'
        },
        condition:{
            type:Number,
            default:0
        }
    },
    data () {
        return {
            dialogVisible: false,
            list:[/*{aid:0},{rid:0}*/],
            total:0,
            change_aid:0,
            change_rid:0,
            page_size:7,
            loading_percentage:0,
            loading_count:0,
            loading_first_done:30,
            loading:true
        }
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
            that.list = [];
            that.loading_start();
            that.loading = true;
            $.ajax({ 
                type:'get', 
                url:"/collection/info?cid="+that.cid+'&page='+that.current_page+'&each='+that.page_size,
                headers: {'X-CSRFToken': this.getCookie('csrftoken')}, 
                processData: false,
                contentType: false,
                success:function (res){ 
                    that.list = res.dist;
                    that.total = res.amount;
                    that.loading_percentage = that.loading_first_done;
                    if(that.list.length){
                        setTimeout(function(){
                            let item = that.$refs.item;
                            for(var i=0; i<item.length; i++){
                                item[i].init();
                            }
                        }, 0);
                    }
                    else{
                        that.loading_done();
                    }
                    that.loading = false;
                },
                error:function(){
                    console.log('连接失败');
                    that.loading_done();
                    that.loading = false;
                }
            });
        },
        open_move_window(type, id){
            this.dialogVisible = true;
            if(type == 'article'){
                this.change_aid = id;
                this.change_rid = 0;
            }
            else if(type == 'resource'){
                this.change_aid = 0;
                this.change_rid = id;
            }
            var that = this;
            setTimeout(function(){
                var res = that.$refs.cocb.init();
                if(!res){
                    that.dialogVisible = false;
                }
            }, 0);
        },
        change_collection(){
            let res = this.$refs.cocb.collection_move();
            if(res){
                this.dialogVisible = false;
                this.current_page!=1&&this.list.length==1 ? this.current_page-- : '';
                this.init();
                this.$emit('refresh');
            }
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
                }, 600);
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
    body{
        scroll-behavior:smooth
    }

    .pagination{
        margin-top:30px;
        text-align: center;
        font-weight: normal;
    }

    .cmb{
        overflow: hidden;
    }

    .cmb>>>.el-dialog{
        max-width:600px;
        min-width:450px;
    }

    .bottom0>>>.el-divider--horizontal{
        margin: 24px 0 0 !important;
    }
</style>