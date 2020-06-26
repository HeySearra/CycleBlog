<template>
    <div class="ccb" v-loading="loading">
        <div style="padding-left:18px 0 10px">
            <div style="height:40px">
                <el-avatar :src="porsrc"></el-avatar>
            </div>
            <h5 class="name" :class="is_member?'member_color':''" @click="to_user_info">{{name}}</h5>
            <span class="time no_choose">{{time}}</span>
        </div>
        <div class="clear_both"></div>
        <div style="padding:0 3.5em;line-height:20px">
            <span class="header no_choose" v-if="header.length">{{header}}</span>{{content}}
        </div>
        <div class="clear_both"></div>
        <div style="float:none">
            <el-button :class="like_condition?'user_option--active':'user_option--noactive'" @click="click_like"><i class="el-input__icon iconfont icon-like"></i> {{likes}}</el-button>
            <el-button class="hover_ccb_show" v-if="!self && login_manager.get()" @click="click_report">举报</el-button>
            <el-button class="hover_ccb_show" v-if="self" @click="click_delete">删除</el-button>
            <el-button class="hover_ccb_show" v-if="login_manager.get()" @click="click_reply">回复</el-button>
        </div>
        <div class="clear_both"></div>
    </div>
</template>

<script>
export default {
    props: {
        qid:{
            type:Number,
            default: 0
        },
        type:{
            type:String,
            default:'article'
        },
    },
    data () {
        return {
            likes:0,
            porsrc:'',
            name:'',
            content:'',
            like_condition:false,
            self:false,
            time:'',
            uid:0,
            header:'',
            is_member:false,
            loading:true
        }
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
            that.loading = true;
            var url = (that.type=='article'?'/article':'/resource') + '/comment/all?qid=' + that.qid;
            $.ajax({ 
                type:'get', 
                url:url,
                headers: {'X-CSRFToken': that.getCookie('csrftoken')}, 
                processData: false,
                contentType: false,
                success:function (res){ 
                    that.likes = res.likes;
                    that.content = res.content;
                    that.like_condition = res.user_options.is_like==1;
                    that.self = res.user_options.is_its==1;
                    that.name = res.name;
                    that.porsrc = res.portrait;
                    that.uid = res.ruid;
                    that.time = res.time;
                    that.header = res.header;
                    that.is_member = res.is_member;
                    that.loading = false;
                },
                error:function(){
                    console.log('连接失败');
                }
            });
        },
        click_reply(){
            if(!this.login_manager.get()){
                this.alert_msg.warning('请先登录才能回复');
                return;
            }
            this.$emit('reply', this.qid, this.name);
        },
        click_like(){
            if(!this.login_manager.get()){
                this.alert_msg.warning('请先登录才能点赞');
                return;
            }
            var that = this;
            var url = (that.type=='article'?'/article':'/resource') + '/comment/like?qid=' + that.qid + '&condition=' + !that.is_like;
            $.ajax({ 
                type:'post', 
                url:url,
                headers: {'X-CSRFToken': this.getCookie('csrftoken')}, 
                data: JSON.stringify({qid:that.qid, condition:!that.like_condition}),
                async:false,
                success:function (res){ 
                    if(res.status == 0){
                        that.likes += that.like_condition?-1:1;
                        that.like_condition = !that.like_condition;
                    }
                    else{
                        that.alert_msg.error('操作失败，请重试');
                    }
                },
                error:function(){
                    that.alert_msg.error('连接失败');
                }
            });
        },
        to_user_info(){
            this.$router.push({path:'/userInfo/'+this.uid});
        },
        click_report(){
            if(!this.login_manager.get()){
                this.alert_msg.warning('请先登录才能举报');
                return;
            }
            this.$emit('report', this.qid, this.name);
        },
        click_delete(){
            var that = this;
            that.alert_box.confirm_msg('提示', '你确定删除这条评论吗？', function(){
                var url = (that.type=='article'?'/article':'/resource') + '/comment/delete';
                $.ajax({ 
                    type:'post', 
                    url:url,
                    headers: {'X-CSRFToken': that.getCookie('csrftoken')}, 
                    data: JSON.stringify({qid:that.qid}),
                    async:false,
                    success:function (res){ 
                        if(res.status == 0){
                            that.alert_msg.success('评论删除成功');
                            that.$emit('refresh');
                        }
                        else{
                            that.alert_msg.error('删除失败，请重试');
                        }
                    },
                    error:function(){
                        that.alert_msg.error('连接失败');
                    }
                });
            });
        }
    }
}
</script>

<style scoped>
    @import "../assets/list_button.css";
    @import url("../assets/common.css");
    .ccb{
        padding: 15px 10px 5px;
        min-height:69px;
        overflow: hidden;
    }

    .ccb:hover{
        background-color: #fafafa;
    }

    h5, .ccb div{
        float: left;
        line-height:30px;
        margin:0;
        font-size: 15px;
    }

    h5{
        margin-left:1em;
        cursor: pointer;
    }

    h5:hover{
        color:hsl(1, 69%, 69%);
    }

    .time{
        margin-left:1em;
        color:#aaa;
        font-size: 13px;
    }

    .header{
        color:#aaa;
        display: inline-block;
        padding-right:0;
    }

    .el-button{
        float: right;
    }

    .hover_ccb_show{
        display: none;
    }

    .ccb:hover .hover_ccb_show{
        display: inline-block;
    }

    .ccb>>>.el-input__icon{
        line-height: 0;
    }
</style>
