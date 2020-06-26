<template>
    <div style="padding:10px 30px">
        <h2>消息中心</h2>
        <el-divider></el-divider>
        <div v-if="!msg_data.length" style="height:30px"></div>
        <div v-if="!msg_data.length&&!loading" class="not_found">你还没有任何消息</div>
        <div v-if="loading" class="not_found">加载中 <i class="el-icon-loading"></i></div>
        <div style="padding:0 10px" v-if="msg_data.length">
            <el-table
                :data="msg_data"
                style="width: 100%;margin-top:10px;\"
                @row-click="row_click"
                :cell-style="row_style"
                >
                <el-table-column
                    fixed
                    prop="time"
                    label="日期"
                    width="200">
                </el-table-column>
                <el-table-column
                    prop="content"
                    label="消息">
                </el-table-column>
            </el-table>
        </div>
        <div class="pagination" v-if="msg_data.length&&total>page_size">
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
        
    },
    data () {
        return {
            msg_data:[
                // {time:'2020-1-1',content:'草 ...... 是一种植物'}
            ],
            page_size:20,
            total:0,
            current_page:1,
            loading:false,
            loading_percentage:0,
            loading_count:0,
        }
    },
    mounted(){
        $(window).scroll(0);
        this.init();
    },
    methods:{
        init(){
            this.apply_for_info();
        },
        getCookie (name) {
            var value = '; ' + document.cookie
            var parts = value.split('; ' + name + '=')
            if (parts.length === 2) return parts.pop().split(';').shift()
        },
        apply_for_info(){
            var that = this;
            that.loading_percentage = 10;
            that.loading = true;
            $.ajax({ 
                type:'get', 
                url:'/login/message?page='+that.current_page+'&each='+that.page_size,
                headers: {'X-CSRFToken': this.getCookie('csrftoken')}, 
                processData: false,
                contentType: false,
                success:function (res){ 
                    that.msg_data = res.message;
                    that.total = res.amount;
                    that.loading = false;
                    that.loading_percentage = 100;
                    setTimeout(function(){
                        $('.loading_bar').addClass('loading_bar_done');
                        setTimeout(function(){
                            that.loading_percentage = 0;
                            that.loading_count = 0;
                        }, 690);
                    }, 600);
                },
                error:function(){
                    console.log('连接失败');
                    that.loading = false;
                    that.loading_percentage = 100;
                    setTimeout(function(){
                        $('.loading_bar').addClass('loading_bar_done');
                        setTimeout(function(){
                            that.loading_percentage = 0;
                            that.loading_count = 0;
                        }, 690);
                    }, 600);
                }
            });
        },
        change_page(arg){
            this.current_page = arg;
            this.apply_for_info();
            document.documentElement.scrollTop = 0;
        },
        row_click(row){
            if(row.aid){
                this.$router.push({path:'/article/'+row.aid});
            }
            else if(row.rid){
                this.$router.push({path:'/resource/'+row.rid});
            }
        },
        row_style(e){
            return e.row.aid||e.row.rid ? 'cursor:pointer' : '';
        }
    }
}
</script>

<style scoped>
    body{
        scroll-behavior:smooth
    }

    .el-divider{
        margin:0;
    }
  
    .el-form{
        margin-top:50px;
        padding: 0 150px
    }

    .el-form-item{
        margin-bottom:30px;
    }

    .pagination{
        margin-top:30px;
        text-align: center;
        font-weight: normal;
    }
</style>

