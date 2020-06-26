<template>
    <div style="padding:10px 30px">
        <h2>积分管理</h2>
        <el-divider></el-divider>
            <div v-if="!list.length" class="not_found">你还没有任何积分变化</div>
            <div style="padding:0 10px" v-if="list.length">
                <el-table
                :data="list"
                style="width: 100%;margin-top:10px"
                height="250">
                <el-table-column
                    fixed
                    prop="point"
                    label=""
                    width="100">
                </el-table-column>
                <el-table-column
                    prop="time"
                    label="时间"
                    width="150">
                </el-table-column>
                <el-table-column
                    prop="content"
                    label="操作">
                </el-table-column>
            </el-table>
        </div>
        <div class="pagination" v-if="list.length&&total>page_size">
            <el-pagination
                background
                layout="total, prev, pager, next, jumper"
                :page-size="page_size"
                :total="total"
                :current-page="current_page">
            </el-pagination>
        </div>
    </div>
</template>

<script>
export default {
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

