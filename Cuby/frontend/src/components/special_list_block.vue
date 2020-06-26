<template>
    <div class="splb">
        <h3 v-show="!in_edit">{{title}} ({{count}}) <i class="el-icon-edit" @click="edit_title"></i></h3>
        <div class="edit_title" v-if="in_edit"><el-input v-model="input" placeholder="请输入内容" @blur="submit_title()" :disabled="disabled" ref="input"></el-input></div>
        <div style="float:right"><el-button @click="click_edit">编辑</el-button></div>
        <div style="float:right"><el-button @click="click_delete">删除</el-button></div>
        <div class="clear_both"></div>
    </div>
</template>

<script>
export default {
    name: 'splb',
    props: {
        sid:{
            type:Number,
            default:0
        },
        count:{
            type:Number,
            default:0
        },
        title:{
            type:String,
            default:''
        },
    },
    data () {
        return {
            input:'',
            in_edit:false,
            disabled:false,
        }
    },
    methods:{
        init(){

        },
        getCookie (name) {
            var value = '; ' + document.cookie
            var parts = value.split('; ' + name + '=')
            if (parts.length === 2) return parts.pop().split(';').shift()
        },
        edit_title(){
            var that = this;
            this.input = this.title;
            this.in_edit = true;
            this.disabled = false;
            setTimeout(function(){that.$refs.input.$el.children[0].focus();}, 0);
        },
        submit_title(){
            var that = this;
            if(this.input==this.title || this.input==''){
                this.in_edit = false;
                return;
            }
            else{
                that.disabled = true;
                $.ajax({ 
                    type:'post', 
                    url:"/create/special/rename",
                    headers: {'X-CSRFToken': that.getCookie('csrftoken')}, 
                    data: JSON.stringify({title:that.input, sid:that.sid}),
                    async:false,
                    success:function (res){ 
                        if(res.status == 0){
                            that.title = that.input;
                            that.in_edit = false;
                            that.disabled = false;
                            that.alert_msg.success('修改成功');
                        }
                        else{
                            switch(res.status){
                                case 1:
                                    that.alert_msg.error('修改失败，存在同名专栏');
                                    break;
                                case 2:
                                    that.alert_msg.error('修改失败，专栏字数不得超过 20 字');
                                    break;
                                default:
                                    that.alert_msg.error('修改失败，请重试');
                            }
                            that.in_edit = false;
                            that.disabled = false;
                        }
                    },
                    error:function(){
                        that.alert_msg.error('连接失败');
                        that.in_edit = false;
                        that.disabled = false;
                    }
                });
            }
        },
        click_edit(){
            this.$emit('edit', this.sid, this.title);
        },
        click_delete(){
            var that = this;
            that.alert_box.confirm_msg('提示', '你确定删除专栏：' + that.title + ' 吗？', function(){
                that.submit_delete();
            });
        },
        submit_delete(){
            var that = this;
            $.ajax({ 
                type:'post', 
                url:"/create/special/delete",
                headers: {'X-CSRFToken': that.getCookie('csrftoken')}, 
                data: JSON.stringify({sid:that.sid}),
                async:false,
                success:function (res){ 
                    if(res.status == 0){
                        that.alert_msg.success('删除成功');
                        that.$emit('refresh');
                    }
                    else{
                        that.alert_msg.success('删除失败');
                    }
                },
                error:function(){
                    that.alert_msg.error('连接失败');
                }
            });
        }
    }
}
</script>

<style scoped>
    @import "../assets/list_button.css";

    .splb{
        padding:10px 10px;
        height:30px;
    }

    .splb:hover{
        background-color: #f5f5f5;
    }

    h3{
        margin:0;
        float: left;
        font-size: 17px;
        line-height: 30px;
    }

    .pagination{
        margin-top:30px;
        text-align: center;
        font-weight: normal;
    }

    .edit_title{
        width:23em;
        height:15px;
        float: left;
    }

    .edit_title>>>.el-input__inner{
        line-height:30px;
        height:30px;
    }

    i{
        color: #bbb;
        cursor: pointer;
        margin-left:.5em;
        display: none;
    }

    .splb:hover i, .splb:hover .el-button{
        display: inline;
    }

    i:hover{
        color:#777;
    }

    .el-button{
        margin-right:.5em;
        display: none;
    }
</style>
