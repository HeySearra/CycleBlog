<template>
    <div class="side_block user_detail_block">
        <div class="block_edit_icon" v-if="is_me"><router-link tag="a" :to="{path:'/create/setting/myinfo'}">编辑</router-link></div>
        <h3>个人信息</h3>
        <el-divider class="across"></el-divider>
        <div v-if="!detail.length" class="not_found" style="margin-top:30px">没有可以展示的信息</div>
        <ul>
            <li v-for='item in detail' :key="item.key">{{item.key}}：{{item.value}}</li>
        </ul>
        
        <div style="clear:both;float:none"></div>
    </div>
</template>

<script>
export default {
    name: 'udb',
    props: {
        detail:{
            type:Array,
            default:[]
        },
        is_me:{
            type:Boolean,
            default:false
        }
    },
    data () {
        return {
            name
        }
    },
    methods:{
        init(){

        },
    }
}
</script>

<style scoped>
@import "../assets/side_block.css";

.user_detail_block{
    
}

.user_detail_block ul{
    padding-left:1em;
}

.user_detail_block li{
    list-style: none;
    line-height: 30px;
    font-size: 15px;
}

.block_edit_icon{
    opacity: 0;
    transition:0.1s opacity linear;
}

.user_detail_block:hover .block_edit_icon{
    opacity: 1;
}

.el-divider{
    margin:0;
}
</style>

