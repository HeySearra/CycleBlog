<template>
    <div style="padding:10px 30px" id="resize">
        <h2>数据中心</h2>
        <el-divider></el-divider>
        <div style="height:70px"></div>
        <div style="width:90%;margin:0 auto">
            <mec></mec>
        </div>
    </div>
</template>

<script>
import echarts from 'echarts'
export default {
    
    name: 'mb',
    props: {

    },
    data () {
        return {
            list:[],
            page_size:20,
            total:0,
            current_page:1

        }
    },
    mounted(){
        $(window).scroll(0);
        // this.init();
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
            $.ajax({ 
                type:'get', 
                url:"/create/point/list?page="+that.current_page+"&each="+that.page_size,
                headers: {'X-CSRFToken': that.getCookie('csrftoken')}, 
                async:false,
                success:function (res){ 
                    that.list = res.list;
                    that.total = res.amount;
                },
                error:function(){
                    console.log('连接失败');
                }
            });
        }
    }
}
</script>

<style scoped>
 
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

    .not_found{
        margin-top:25px
    }
</style>

