<template>
    <el-dialog 
        :visible.sync="dialogVisible" 
        v-infinite-scroll="load" 
        class="infinite-list vcd" 
        style="overflow:auto">
        <h1><i class="el-icon-star-off"></i> {{title}}</h1>
        <el-divider></el-divider>
        <p v-if="!list.length" class="not_found" style="margin-top:30px">什么？这个收藏夹竟然啥都没有</p>
        <component v-for="item in list" :key="item.aid?item.aid:item.rid" :is="item.aid?'arb':'rsb'" :aid="item.aid" :rid="item.rid" :cid="item.cid" ref="item" type="collection_view"></component>
        <p v-if="!is_final" class="not_found">加载中 <i class="el-icon-loading"></i></p>
        <p v-if="is_final&&list.length" class="not_found">啊，这里就是尽头了 <i class="el-icon-cold-drink"></i></p>
    </el-dialog>
</template>

<script>
export default {
    props:{
        title:{
            type:String,
            default:'收藏夹'
        }
    },
    data() {
        return {
            cid:0,
            dialogVisible:false,
            list:[],
            current_page:1,
            page_size:6,
            is_final:false,
            loading:false,
        };
    },

    methods:{
        open(cid){
            this.dialogVisible = true;
            this.list = [];
            this.cid = cid;
            this.current_page = 0;
            this.is_final = false;
            this.loading = false;
            this.apply_for_info();
        },
        getCookie (name) {
            var value = '; ' + document.cookie
            var parts = value.split('; ' + name + '=')
            if (parts.length === 2) return parts.pop().split(';').shift()
        },
        apply_for_info(){
            var that = this;
            that.current_page++;
            $.ajax({ 
                type:'get', 
                url:"/collection/info?cid="+that.cid+'&page='+that.current_page+'&each='+that.page_size,
                headers: {'X-CSRFToken': this.getCookie('csrftoken')}, 
                async:false,
                success:function (res){ 
                    let len = that.list.length;
                    that.list = that.list.concat(res.dist);
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
                },
                error:function(){
                    that.current_page--;
                    that.dialogVisible = false;
                    that.alert_msg.error('连接失败');
                }
            });
        },
        load(){
            if(this.is_final){
                return;
            }
            var that = this;
            setTimeout(function(){
                that.apply_for_info();
            })
        },
        close(){
            this.dialogVisible = false;
        }
    }
}
</script>

<style scoped>
    @import url("../assets/common.css");

    h1{
        font-size:23px;
        margin:0 1em;
        text-align: left;
    }

    .vcd>>>.el-divider{
        margin-bottom:0;
    }

    .vcd>>>.el-dialog{
        min-width:800px;
    }

    .vcd>>>.el-dialog__body{
        padding-left:0;
        padding-right:0;
        padding-top:11px;
    }
</style>