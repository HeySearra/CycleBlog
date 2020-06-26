<template>
    <div style="padding:10px 30px" :class="list.length==0?'':'bottom0'">
        <div>
            <h2>上传明细</h2>
            <el-divider></el-divider>
            <div class="not_found" v-if="!list.length&&!loading">找不到任何的资源</div>
            <div v-if="loading" class="not_found">加载中 <i class="el-icon-loading"></i></div>
            <rsb v-for="item in list" :key="item" :rid="item" type="edit" ref="rsb" @edit_resource="click_edit" @refresh="refresh" @done="loading_done_msg"></rsb>
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
                <urb type="edit" :rid="editing_rid" ref="urb" @close="close_dialog" @open="open_dialog" @edit_success="apply_for_info"></urb>
            </div>
            <div slot="footer" class="dialog-footer">
                <el-button @click="close_dialog">取 消</el-button>
                <el-button type="primary" @click="submit_edit">确 定</el-button>
            </div>
        </el-dialog>
        <el-progress :percentage="loading_percentage" class="loading_bar" :show-text="false"></el-progress>
    </div>
</template>

<script>
export default {
    name: 'urmb',
    data () {
        return {
            list:[],
            page_size:7,
            current_page:1,
            total:0,
            dialogVisible: false,
            editing_rid:0,
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
            that.loading = true;
            that.loading_start();
            $.ajax({ 
                type:'get', 
                url:"/create/resource/upload_list?page="+that.current_page+'&each='+that.page_size,
                headers: {'X-CSRFToken': this.getCookie('csrftoken')}, 
                processData: false,
                contentType: false,
                success:function (res){ 
                    that.list = res.rid;
                    that.total = res.amount;
                    that.loading_percentage = that.loading_first_done;
                    setTimeout(function(){
                        if(that.list.length != 0){
                            var item = that.$refs.rsb;
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
                    that.alert_msg.error('连接失败');
                    that.loading_done();
                    that.loading = false;
                }
            });
        },
        change_page(arg){
            this.current_page = arg;
            this.apply_for_article_list();
            document.documentElement.scrollTop = 0;
        },
        click_edit(rid){
            var that = this;
            this.editing_rid = rid;
            this.open_dialog();
            setTimeout(function(){
                that.$refs.urb.init();
            }, 0);
        },
        close_dialog(){
            this.dialogVisible = false;
        },
        open_dialog(){
            this.dialogVisible = true;
        },
        submit_edit(){
            this.$refs.urb.submit_edit();
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

    .pagination{
        margin-top:30px;
        text-align: center;
        font-weight: normal;
    }

    .bottom0>>>.el-divider{
        margin: 24px 0 0 !important;
    }
</style>

