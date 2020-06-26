<template>
    <div style="margin-top:-30px" class="cocb" v-loading="loading">
        <h2>{{title}}</h2>
        <el-divider></el-divider>
        <div style="height:20px"></div>
        <div v-if="loading" class="not_found">加载中 <i class="el-icon-loading"></i></div>
        <div style="padding:0 20px">
            <div v-for="item in list" :key="item">
                <el-radio v-model="radio" :label="item.cid">
                {{item.title}} ({{item.count}})
            </el-radio>
            </div>
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
        aid:{
            type:Number,
            default:0
        },
        rid:{
            type:Number,
            default:0
        },
        title:{
            type:String,
            default:'你要移动到哪个收藏夹？'
        }
    },
    data() {
        return {
            radio:this.cid,
            list:[/*{title:'1',cid:0,hide:false,count:0}*/],
            loading:true
        };
    },

    methods:{
        init(){
            return this.apply_for_info();
        },
        getCookie (name) {
            var value = '; ' + document.cookie
            var parts = value.split('; ' + name + '=')
            if (parts.length === 2) return parts.pop().split(';').shift()
        },
        apply_for_info(){
            var that = this;
            that.loading = true;
            var ret = false;
            $.ajax({ 
                type:'get', 
                url:"/collection/list",
                headers: {'X-CSRFToken': this.getCookie('csrftoken')}, 
                async:false,
                success:function (res){ 
                    that.list = res.collections;
                    ret = true;
                    that.loading = false;
                },
                error:function(){
                    console.log('连接失败');
                }
            });
            return ret;
        },
        clear_chosen(){
            this.radio = 0;
        },
        collection_move(){
            var that = this;
            var ret = false;
            if(this.radio == this.cid){
                return;
            }
            if(that.aid != 0){
                $.ajax({ 
                    type:'post', 
                    url:"/collection/move_article",
                    headers: {'X-CSRFToken': this.getCookie('csrftoken')}, 
                    data: JSON.stringify({src:that.cid, dst:that.radio, aid:that.aid}),
                    async:false,
                    success:function (res){ 
                        if(res.status == 0){
                            that.alert_msg.success('移动成功');
                            ret = true;
                        }
                        else{
                            that.alert_msg.error('移动失败');
                        }
                    },
                    error:function(){
                        that.alert_msg.error('连接失败');
                    }
                });
            }
            else if(that.rid != 0){
                $.ajax({ 
                    type:'post', 
                    url:"/collection/move_resource",
                    headers: {'X-CSRFToken': this.getCookie('csrftoken')}, 
                    data: JSON.stringify({src:that.cid, dst:that.radio, rid:that.rid}),
                    async:false,
                    success:function (res){ 
                        if(res.status == 0){
                            that.alert_msg.success('移动成功');
                            ret = true;
                        }
                        else{
                            that.alert_msg.error('移动失败');
                        }
                    },
                    error:function(){
                        that.alert_msg.error('连接失败');
                    }
                });
            }
            return ret;
        },
        add_collection(){
            var that = this;
            var ret = false;
            if(that.radio == that.cid){
                return;
            }
            if(that.radio == 0){
                that.alert_msg.warning('请选择收藏夹');
                return;
            }
            if(that.aid != 0){
                $.ajax({ 
                    type:'post', 
                    url:"/collection/add_article",
                    headers: {'X-CSRFToken': this.getCookie('csrftoken')}, 
                    data: JSON.stringify({cid:that.radio, aid:that.aid}),
                    async:false,
                    success:function (res){ 
                        if(res.status == 0){
                            that.alert_msg.success('收藏成功');
                            ret = true;
                        }
                        else{
                            that.alert_msg.error('收藏失败');
                        }
                    },
                    error:function(){
                        that.alert_msg.error('连接失败');
                    }
                });
            }
            else if(that.rid != 0){
                $.ajax({ 
                    type:'post', 
                    url:"/collection/add_resource",
                    headers: {'X-CSRFToken': this.getCookie('csrftoken')}, 
                    data: JSON.stringify({cid:that.radio, rid:that.rid}),
                    async:false,
                    success:function (res){ 
                        if(res.status == 0){
                            ret = true;
                        }
                        else{
                            that.alert_msg.error('收藏失败');
                        }
                    },
                    error:function(){
                        that.alert_msg.error('连接失败');
                    }
                });
            }
            return ret;
        }
    }
}
</script>

<style scoped>
    .cocb>>>.el-radio{
        width:100%;
        margin-right:0 !important;
        padding:10px 0;
        margin-bottom:5px;
    }

    .el-divider{
        margin: 24px 0 !important;
    }
</style>