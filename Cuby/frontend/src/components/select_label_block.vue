<template>
    <div class="side_block label_block">
        <h3>{{title}}</h3>
        <el-divider></el-divider>
        <div style="height:20px" v-if="!list.length"></div>
        <div class="not_found" v-if="!list.length">没有任何的标签</div>
        <div style="height:5px" v-if="!list.length"></div>
        <div v-if="list.length"><el-tag class="tag" type="info" v-for='title in list' :key="title" @click="click_tag(title)" :effect="type=='choose'&&chosen_list.indexOf(title)!=-1 ? 'dark' : 'light'">{{title}}</el-tag></div>
        <vtd v-if="type=='hot'" ref="vtd"></vtd>
        <div style="clear:both"></div>
    </div>
</template>

<script>
export default {
    props: {
        // key_word:{
        //     type:String,
        //     default:''
        // },
        title:{
            type:String,
            default:'标签窗口'
        },
        type:{
            type:String,
            default:'choose'
        }
    },
    data () {
        return {
            list:[],
            chosen_list:[]
        }
    },
    methods:{
        init(tags){
            if(this.type == 'choose'){
                this.list = tags;
                this.chosen_list = [];
            }
            else if(this.type == 'hot'){
                this.apply_for_hot_tags();
            }
        },

        getCookie (name) {
            var value = '; ' + document.cookie
            var parts = value.split('; ' + name + '=')
            if (parts.length === 2) return parts.pop().split(';').shift()
        },

        click_tag(title){
            if(this.type == 'choose'){
                this.change_tags(title);
            }
            else if(this.type == 'hot'){
                this.$refs.vtd.open(title);
            }
        },

        change_tags(title){
            if(this.chosen_list.indexOf(title) == -1){
                this.chosen_list.push(title);
                this.$emit('change_tags', this.chosen_list);
            }
            else{
                var that = this;
                this.chosen_list.forEach((item,index,arr) => {
                    if(item == title){
                        that.chosen_list.splice(index,1);
                    }
                });
                this.$emit('change_tags', this.chosen_list);
            }
        },
        
        apply_for_hot_tags(){
            var that = this;
            $.ajax({ 
                type:'get', 
                url:"/side/hot_tags",
                headers: {'X-CSRFToken': this.getCookie('csrftoken')}, 
                processData: false,
                contentType: false,
                success:function (res){ 
                    that.list = res.tags;
                },
                error:function(){
                    console.log('连接失败');
                }
            });
        },

        click_hot_tag(title){
            this.$refs.vtd.open(title);
        }
    }
}
</script>

<style scoped>
@import "../assets/side_block.css";
@import "../assets/tag.css";

.label_block_block{
    height:auto;
}

.el-divider{
    margin:0;
    margin-bottom:6px;
}

.not_found{
    font-size: 15px;
}
</style>

