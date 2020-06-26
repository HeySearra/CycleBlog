<template>
    <div class="data_block side_block" :class="pointer_flag?'pointer':'curdef'" @click="_click" v-loading="loading">
        <div v-if="type=='default'">
            <div class="data_num">{{view}}</div>
            <h4>昨日阅读量</h4>
        </div>
        <div v-if="type=='default'">
            <div class="data_num">{{point}}</div>
            <h4>积分</h4>
        </div>
        <div v-if="type=='default'">
            <div class="data_num">{{collection}}</div>
            <h4>收藏</h4>
        </div>
        <div v-if="type=='default'">
            <div class="data_num">{{like}}</div>
            <h4>点赞</h4>
        </div>
        <div v-if="type=='only_fans'" :class="(pointer_flag?'':'hover_pink ')+(is_follow?'pink':'')" @click="submit_follow">
            <div class="data_num">{{fans}}</div>
            <h4>粉丝数</h4>
        </div>
        <div v-if="type=='only_fans'">
            <div class="data_num">{{follow}}</div>
            <h4>关注数</h4>
        </div>
        <div style="clear:both;float:none"></div>
    </div>
</template>

<script>
export default {
    props: {
        type:{
            type:String,
            default:'default'
        },
        uid:{
            type:Number || String,
            default:0
        }
    },
    data () {
        return {
            view:'',
            point:'',
            collection:'',
            like:'',
            follow:'',
            fans:'',
            pointer_flag:false,
            is_follow:false,
            loading:false
        }
    },
    methods:{
        init(){
            this.apply_for_info();
            if(this.type=='default' || this.type=='only_fans'&&this.login_manager.get_uid()==this.uid){
                this.pointer_flag = true;
            }
        },
        getCookie (name) {
            var value = '; ' + document.cookie
            var parts = value.split('; ' + name + '=')
            if (parts.length === 2) return parts.pop().split(';').shift()
        },
        apply_for_info(){
            var that = this;
            that.loading = true;
            if(that.type == 'default'){
                $.ajax({ 
                    type:'get', 
                    url:'/index/statistics_card',
                    headers: {'X-CSRFToken': this.getCookie('csrftoken')}, 
                    processData: false,
                    contentType: false,
                    success:function (res){ 
                        that.view = parseInt(res.views)>9999 ? '9999+' : res.views;
                        that.point = parseInt(res.points)>9999 ? '9999+' : res.points;
                        that.collection = parseInt(res.stars)>9999 ? '9999+' : res.stars;
                        that.like = parseInt(res.likes)>9999 ? '9999+' : res.likes;
                        that.loading = false;
                    },
                    error:function(){
                        console.log('连接失败');
                    }
                });
            }
            else if(that.type == 'only_fans'){
                $.ajax({ 
                    type:'get', 
                    url:'/data/fans_and_follows?uid='+that.uid,
                    headers: {'X-CSRFToken': this.getCookie('csrftoken')}, 
                    async:false,
                    success:function (res){ 
                        that.follow = parseInt(res.follows)>9999 ? '9999+' : res.follows;
                        that.fans = parseInt(res.fans)>9999 ? '9999+' : res.fans;
                    },
                    error:function(){
                        console.log('连接失败');
                    }
                });
                $.ajax({ 
                    type:'get', 
                    url:"/side/user_info?uid="+that.uid,
                    headers: {'X-CSRFToken': this.getCookie('csrftoken')}, 
                    processData: false,
                    contentType: false,
                    success:function (res){ 
                        that.is_follow = res.condition == 1;
                        that.loading = false;
                    },
                    error:function(){
                        console.log('连接失败');
                    }
                });
            }
        },
        to_data(){
            this.$router.push({path:'/create/data'});
        },
        _click(){
            if(this.type == 'default'){
                this.to_data();
            }
            else if(this.type == 'only_fans'){
                if(this.login_manager.get_uid() == this.$route.params.id){
                    this.$router.push({path:'/create/follows'});
                }
            }
        },
        submit_follow(){
            if(this.pointer_flag){
                return;
            }
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
                        that.fans += that.is_follow ? -1 : 1;
                        that.is_follow = !that.is_follow;
                        if(that.is_follow){
                            that.alert_msg.success('关注成功');
                        }
                        else{
                            that.alert_msg.success('已取消关注');
                        }
                    }
                    else{
                        switch(res.status){
                            default:
                                that.alert_msg.error('操作失败，请重试');
                        }
                    }
                },
                error:function(){
                    that.alert_msg.error('操作失败，请重试');
                }
            });
        }
    }

}
</script>

<style scoped>
@import "../assets/side_block.css";

.data_block{
    padding-bottom:10px;
}

.data_block h4{
    margin:18px 0;
}

.data_block>div{
    width:50%;
    text-align: center;
    float: left;
}

.data_block .data_num{
    font-size: 35px;
    font-weight: bold;
}

.hover_pink{
    cursor: pointer;
}

.hover_pink:hover, .pink{
    color:hsl(1, 69%, 69%);
}
</style>

