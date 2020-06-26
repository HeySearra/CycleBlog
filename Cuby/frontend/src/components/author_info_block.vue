<template>
    <div class="side_block author_info_block" v-loading="loading">
        <div @click="to_user_info">
            <el-avatar :src="circleUrl"></el-avatar>
            <h3 :class="is_member?'member_color':''">{{name}}
            </h3>
            <div class="clear_both"></div>
        </div>
        <div class="author_intro">{{intro}}</div>
        <div style="text-align:center;margin-top:25px" v-if="login_manager.get()">
            <el-button :type="is_follow?'primary':'default'" class="subscribe_button ls1" @click="follow_option">{{button_title}}</el-button>
        </div>
        <div style="text-align:center;margin-top:10px" v-if="login_manager.get_uid()==uid&&aid"><el-button type="primary" class="subscribe_button ls1" @click="to_edit">编辑文章</el-button></div>
    </div>
</template>

<script>
export default {
    props: {
        uid:{
            type:Number,
            default:0
        },
        aid:{
            type:Number,
            default:0
        }
    },
    data () {
        return {
            button_title:'关注',
            circleUrl: "",
            name:'',
            intro:'',
            is_follow:false,
            is_member:false,
            loading:true
        }
    },
    methods:{
        init(){
            this.apply_for_data();
        },
        apply_for_data(){
            var that = this;
            that.loading = true;
            $.ajax({ 
                type:'get', 
                url:"/side/user_info?uid="+that.uid,
                headers: {'X-CSRFToken': this.getCookie('csrftoken')}, 
                processData: false,
                contentType: false,
                success:function (res){ 
                    that.name = res.name;
                    that.circleUrl = res.portrait;
                    that.intro = res.introduction;
                    that.is_follow = res.condition == 1;
                    that.is_follow ? that.button_title='已关注' : '关注';
                    that.is_member = res.is_member;
                    that.loading = false;
                },
                error:function(){
                    that.alert_msg.normal('连接失败');
                }
            });
        },
        getCookie (name) {
            var value = '; ' + document.cookie
            var parts = value.split('; ' + name + '=')
            if (parts.length === 2) return parts.pop().split(';').shift()
        },
        to_edit(){
            this.aid ? this.$router.push({path:'/edit/'+this.aid}) : ''
        },
        follow_option(){
            if(!this.login_manager.get()){
                this.alert_msg.warning('你需要登录才能关注');
                return;
            }
            var that = this;
            $.ajax({ 
                type:'post', 
                url:'/create/follow',
                headers: {'X-CSRFToken': this.getCookie('csrftoken')}, 
                data: JSON.stringify({uid:that.uid, condition:!that.is_follow}),
                async:false,
                success:function (res){ 
                    if(res.status == 0){
                        that.is_follow = !that.is_follow;
                        that.button_title = that.is_follow ? '已关注' : '关注';
                        that.is_follow ? that.alert_msg.success('关注成功') : that.alert_msg.success('已取消关注');
                    }
                    else{
                        switch(res.status){
                            case 2:
                                that.alert_msg.warning('不能关注你自己');
                                break;
                            default:
                                that.alert_msg.error('操作失败，请重试');
                        }
                    }
                },
                error:function(){
                    that.alert_msg.error('操作失败，请重试');
                }
            });
        },
        to_user_info(){
            this.$router.push({path:'/userInfo/'+this.uid});
        }
    }
}
</script>

<style scoped>
@import "../assets/side_block.css";
@import "../assets/icon_store/iconfont.css";

.author_info_block>div{
    margin:5px 0 0;
}

.author_info_block>div>h3{
    float: right;
    width:75%;
    margin:0;
    line-height:45px;
    font-size: 21px;
    cursor: pointer;
    overflow: hidden;
}

h3:hover{
    color:hsl(1, 69%, 69%);
}

.author_intro{
    font-size: 13px;
    padding:10px 15px;
    line-height: 20px;
}

.subscribe_button{
    width:250px;
    text-align: center;
    padding:8px 0;
}

.el-avatar{
    display: inline-block;
    width: 45px;
    height: 45px;
}

.el-avatar>img{
    display:block;
    height:100%;
}

.el-divider{
    margin:0;
}

.ls1{
    letter-spacing: 1em;
    text-indent: 1em;
}

.icon{
    width: 21px !important;
}
</style>

