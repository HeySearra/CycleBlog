<template>
    <div class="follow_new">
        <div class="not_found" v-if="!list.length" style="height:100px;line-height:100px">
            找不到任何关注列表的动态 <i class="el-icon-milk-tea"></i>
        </div>
        <component v-for="item in list" :key="item" :is="item.aid?'arb':'rsb'" :aid="item.aid" :rid="item.rid" :cid="item.cid" ref="item" type="collection_view"></component>
        <p v-if="loading" class="not_found" style="cursor:default" @click="load">嘿咻 <i class="el-icon-loading"></i></p>
        <p v-if="!is_final&&list.length&&!loading" class="not_found more" @click="load">加载更多内容</p>
        <p v-if="is_final&&list.length" class="not_found" style="cursor:default">呀，这里就是所有的动态了 <i class="el-icon-milk-tea"></i></p>
    </div>
</template>

<script>
export default {
    data () {
        return {
            is_final:false,
            current_page:0,
            page_size:8,
            total:0,
            list:[],
            loading:true
        }
    },
    mounted(){
        this.init();
    },
    methods:{
        init(){
            if(!this.login_manager.get()){
                this.$router.push({path:'/index'});
                return;
            }
            document.documentElement.scrollTop = 0;
            $("aside").css({
                marginTop: 0
            });
            this.apply_for_info();
        },
        
        getCookie (name) {
            var value = '; ' + document.cookie
            var parts = value.split('; ' + name + '=')
            if (parts.length === 2) return parts.pop().split(';').shift()
        },
        load(){
            if(this.is_final){
                return;
            }
            this.loading = true;
            var that = this;
            setTimeout(function(){
                that.apply_for_info();
            })
        },
        apply_for_info(){
            var that = this;
            that.loading = true;
            that.current_page++;
            $.ajax({ 
                type:'get', 
                url:'/login/news?page='+that.current_page+'&each='+that.page_size,
                headers: {'X-CSRFToken': this.getCookie('csrftoken')}, 
                async:false,
                success:function (res){ 
                    let len = that.list.length;
                    that.list = that.list.concat(res.list);
                    that.total = res.amount;
                    if(that.list.length >= that.total){
                        that.is_final = true;
                    }
                    if(that.list.length){
                        setTimeout(function(){
                            let item = that.$refs.item;
                            for(var i=len; i<item.length; i++){
                                item[i].init();
                            }
                        }, 0);
                    }
                    that.loading = false;
                },
                error:function(){
                    that.current_page--;
                    that.alert_msg.error('连接失败');
                    that.loading = false;
                }
            });
        }
    }
}
</script>

<style scoped>
@import url("../assets/common.css");
</style>

