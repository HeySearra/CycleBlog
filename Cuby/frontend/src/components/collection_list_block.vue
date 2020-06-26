<template>
    <div class="clb" :class="name=='默认收藏夹'?'':'clb_dis'">
        <i class="el-icon-menu"></i>
        <span slot="title">{{name}}</span>
        <div style="float:right">
            <span class="folder_count" :style="hover?'display:none':''">{{count}}</span>
            <span class="folder_options" :style="hover?'display:inline':''" v-if="name!='默认收藏夹'">
                <el-dropdown @visible-change="change($event, 1)" @command="handle_command">
                    <span class="el-dropdown-link">
                        <i class="el-icon-more-outline"></i>
                    </span>
                    <el-dropdown-menu slot="dropdown">
                        <el-dropdown-item :command="rename">编辑</el-dropdown-item>
                        <el-dropdown-item :command="del">删除</el-dropdown-item>
                    </el-dropdown-menu>
                </el-dropdown>
            </span>
        </div>
    </div>
</template>

<script>
export default {
    props:{
        cid:{
            type:Number,
            default:0
        },
        name:{
            type:String,
            default:'默认收藏夹'
        },
        count:{
            type:Number,
            default:0
        },
        condition:{
            type:Number,
            default:0
        }
    },
    data() {
        return {
            hover:false
        };
    },

    methods:{
        getCookie (name) {
            var value = '; ' + document.cookie
            var parts = value.split('; ' + name + '=')
            if (parts.length === 2) return parts.pop().split(';').shift()
        },
        change(callback){
            //console.log(this.hover)
            this.hover = callback;
        },
        handle_command(command){
            command();
        },
        del(){
            var that = this;
            that.alert_box.confirm_msg('删除收藏夹','你确认要删除 '+ that.name + ' 吗？', function(){
                $.ajax({ 
                    type:'post', 
                    url:"/collection/delete",
                    headers: {'X-CSRFToken': that.getCookie('csrftoken')}, 
                    data: JSON.stringify({cid:that.cid}),
                    processData: false,
                    contentType: false,
                    success:function (res){ 
                        if(res.status == 0){
                            that.alert_box.msg('提示', '删除成功', function(){
                                that.$router.go(0);
                            });
                        }
                        else{
                            switch(res){
                                case 1:
                                    that.alert_msg.error('收藏夹不存在');
                                    break;
                                default:
                                    that.alert_msg.error('删除失败');
                            }
                        }
                    },
                    error:function(){
                        that.alert_msg.error('连接失败');
                    }
                });
            })
        },
        rename(){
            this.$emit('edit', this.cid, this.name, this.condition);
        }
    }
}
</script>

<style scoped>
    .clb{
        padding:0 20px;
    }

    .clb_dis:hover .folder_count, .folder_options{
        display: none;
    }

    .clb_dis:hover .folder_options, .folader_count{
        display: inline;
    }

    .folder_options{
        vertical-align: top;
        margin-right: -.6em;
    }

    .folder_options, .folder_count{
        text-align: right;
    }

    .el-dropdown-menu, .el-dropdown{
        padding:5px 0;
        display: inline;
    }

    .el-dropdown>>>span{
        vertical-align: top;
    }
</style>