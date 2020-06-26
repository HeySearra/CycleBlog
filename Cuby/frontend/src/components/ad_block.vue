<template>
    <div style="padding:10px 30px">
        <h2>{{title}}</h2>
        <el-divider></el-divider>
        <div style="padding:0 10px">
            <el-table
            :data="msg_data"
            style="width: 100%;margin-top:10px"
            height="250">
            <el-table-column
                fixed
                prop="date"
                label="日期"
                width="150">
            </el-table-column>
            <el-table-column
                prop="content"
                label="内容">
            </el-table-column>
            <el-table-column
                prop="options"
                label="操作">
            </el-table-column>
        </el-table>
        </div>
        <div class="pagination">
        <el-pagination
            background
            layout="total, prev, pager, next, jumper"
            :page-size="20"
            :total="90"
            :current-page="current_page"
            v-show="!no_article">
        </el-pagination>
        </div>
    </div>
</template>

<script>
export default {
    props: {
        title:{
            type:String,
            default:'用户管理'
        }
    },
    data () {
        return {
            msg_data:[
                {date:'2020-1-1',msg:'草 ...... 是一种植物'}
            ]
        }
    }
}
</script>

<style scoped>
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

