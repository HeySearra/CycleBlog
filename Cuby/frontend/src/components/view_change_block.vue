<template>
    <div class="side_block view_change_block">
        <el-table
            :data="tableData"
            :cell-style="row_style"
            :show-header="false"
            style="width: 100%; cursor:pointer">
            <el-table-column
                prop="title"
                width="180">
            </el-table-column>
            <el-table-column
                prop="num"
                width="70"
                class="tar"
            >
            </el-table-column>
        </el-table>
        <div style="clear:both;float:none"></div>
    </div>
</template>

<script>
export default {
    props: {
        tableData:{
            type:Array,
            default() {
                return [/*{title:'标题',num:10000},{title:'标题',num:10000}*/];
            }
        }
    },
    data () {
        return {
        }
    },
    methods: {
        row_style(obj){
            if(obj.columnIndex == 1){
                return 'text-align:right';
            }
            else{
                return '';
            }
        }
    }
}
</script>

<style scoped>
@import "../assets/side_block.css";

.view_change_block{
    padding-top:10px;
    padding-bottom:10px;
}

.view_change_block>div{
    width:100%;
    text-align: center;
    cursor: pointer;
}

.view_change_block .data_num{
    font-size: 35px;
    font-weight: bold;
}

.el-divider{
    margin:0;
}

.view_change_block>>>.el-table--enable-row-transition .el-table__body td{
    border:0;
}

.view_change_block>>>.el-table td, 
.view_change_block>>>.el-table th{
    padding:3px 0
}

.el-table--border::after, .el-table--group::after, .el-table::before{
    height:0;
}
</style>

