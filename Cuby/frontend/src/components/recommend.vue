<template>
    <div class="recommend">
        <div class="not_found" v-if="!list.length" style="height:100px;line-height:100px">
            找不到任何推荐的文章 <i class="el-icon-hot-water"></i>
        </div>
        <arb v-for="item in list" :key="item" :aid="item" ref="arb" type="recommend"></arb>
        <p v-if="loading" class="not_found" style="cursor:default" @click="load">我再找找看 <i class="el-icon-loading"></i></p>
        <p v-if="!is_final&&list.length&&!loading" class="not_found more" @click="load">加载更多内容</p>
        <p v-if="is_final&&list.length" class="not_found" style="cursor:default">呀，这里就是所有的推荐内容了 <i class="el-icon-hot-water"></i></p>
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
            $(window).scroll(0);
            $("aside").css({
                marginTop: 0
            });
            this.apply_for_recommend();
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
                that.apply_for_recommend();
            }, 0);
        },
        apply_for_recommend(){
            var that = this;
            that.loading = true;
            that.current_page++;
            $.ajax({ 
                type:'get', 
                url:'/index/recommend?page='+that.current_page+'&each='+that.page_size,
                headers: {'X-CSRFToken': this.getCookie('csrftoken')}, 
                async:false,
                success:function (res){ 
                    let len = that.list.length;
                    that.list = that.list.concat(res.article);
                    that.total = res.amount;
                    if(that.list.length >= that.total){
                        that.is_final = true;
                    }
                    if(that.list.length){
                        setTimeout(function(){
                            let item = that.$refs.arb;
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

