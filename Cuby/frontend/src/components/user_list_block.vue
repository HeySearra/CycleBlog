<template>
    <div class="ulb">
        <div style="float:left;width:80%">
            <div>
                <div class="photo">
                    <el-avatar :src="src"></el-avatar>
                </div>
            </div>
            <div>
                <h5 class="name" @click="to_user_info">{{name}}</h5>
                <div class="clear_both"></div>
                <div class="intro">
                    {{introduction}}
                </div>
            </div>
            
            <div class="clear_both"></div>
        </div>
        <div class="button" :class="button=='取消关注'?'cancal':''" v-if="type=='subscribe'">
            <el-button :type="button=='取消关注'?'':'primary'" @click="follow_option">{{button}}</el-button>
        </div>
        <div class="clear_both"></div>
    </div>
</template>

<script>
export default {
    name:'ulb',
    props: {
        uid:{
            type:Number,
            default: 0
        },
        type:{
            type:String,
            default:'view'
        }
    },
    watch:{
        'is_follow'(){
            this.button = this.is_follow?'取消关注':'关 注';
        }
    },
    data () {
        return {
            button:'取消关注',
            name:'',
            introduction:'',
            is_follow:false,
            src:'',
            is_member:''
        }
    },
    methods:{
        init(){
            this.apply_for_info();
            if(this.type == 'subscribe'){
                this.is_follow = true;
            }
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
                url:'/side/user_info?uid='+that.uid,
                headers: {'X-CSRFToken': this.getCookie('csrftoken')}, 
                processData: false,
                contentType: false,
                success:function (res){ 
                    that.name = res.name;
                    that.src = res.portrait;
                    that.introduction = res.introduction;
                    that.is_member = res.is_member;
                    that.$emit('done');
                },
                error:function(){
                    console.log('连接失败');
                    that.$emit('done');
                }
            });
        },
        follow_option(){
            var that = this;
            $.ajax({ 
                type:'post', 
                url:'create/follow',
                headers: {'X-CSRFToken': this.getCookie('csrftoken')}, 
                data: JSON.stringify({uid:that.uid, condition:!that.is_follow}),
                async:false,
                success:function (res){ 
                    if(res.status == 0){
                        that.is_follow = !that.is_follow;
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
    @import url("../assets/common.css");
    .ulb{
        padding: 10px .5em 5px;
        height:65px;
        overflow: hidden;
    }

    .ulb:hover{
        background-color: #f5f5f5;
    }

    .ulb:hover .cancal{
        display: inline;
    }

    h5, .ulb div{
        float: left;
        line-height:30px;
        margin:0;
        font-size: 15px;
    }

    h5{
        margin-left:1em;
        margin-top:5px;
        cursor: pointer;
    }

    h5:hover{
        color:hsl(1, 69%, 69%);
    }

    .el-button{
        padding-left:0;
        padding-right: 0;
        width:6.5em
    }

    .button{
        float:right;
        width:20%;
        text-align:right;
        line-height:60px !important;
    }

    .cancal{
        display: none;
    }

    .photo{
        padding-top: 5px;
        height:60px;
        line-height:60px;
    }

    .photo>>>.el-avatar{
        width: 50px;
        height: 50px;
    }

    .intro{
        padding:0 1.5em !important; 
        font-size:13px !important;
        line-height:1.5em !important;
        color:#aaa;
    }
</style>
