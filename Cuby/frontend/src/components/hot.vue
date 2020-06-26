<template>
    <div class="hot">
        <div class="not_found" v-if="!list.length" style="height:100px;line-height:100px">
            没有任何热门文章 <i class="el-icon-ice-cream-square"></i>
        </div>
        <arb v-for="item in list" :key="item" :aid="item" ref="arb" type="collection_view"></arb>
        <p v-if="loading" class="not_found" style="cursor:default" @click="load">在找啦 <i class="el-icon-loading"></i></p>
        <p v-if="!is_final&&list.length&&!loading" class="not_found more" @click="load">加载更多内容</p>
        <p v-if="is_final&&list.length" class="not_found" style="cursor:default">难不成，这就是所有的热门文章了 <i class="el-icon-ice-cream-square"></i></p>
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
        document.documentElement.scrollTop = 0;
        $("aside").css({
            marginTop: 0
        });
        this.init();
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
                url:'/index/hot?page='+that.current_page+'&each='+that.page_size,
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

