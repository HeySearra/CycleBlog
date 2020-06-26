<template>
    <div class="side_block list_block" v-loading="loading">
        <div class="block_edit_icon" v-if="editable" @click="click_edit"><a>{{edittitle}}</a></div>
        <h3>{{title}}</h3>
        <el-divider class="across"></el-divider>
        <div v-if="!list.length" class="not_found" style="margin:20px auto 10px;font-size:15px;cursor:default">这里什么都没有</div>
        <div>
            <ul v-if="type=='collection' || type=='special'">
                <li v-for="(item, index) in list" :key="index" @click="click_item(item)">
                    <span style="margin-left: 5px">{{ item.title?item.title:item.name }}</span>
                    <span v-if="type=='special'||type=='collection'"> ({{item.count}})</span>
                    <i class="iconfont" :class="type=='collection'&&!item.condition?'' : 'icon-eye-close'" v-if="type=='collection'"></i>
                </li>
            </ul>
            <ul v-if="type=='relative_article' || type=='relative_resource'">
                <li v-for="(item, index) in list" :key="index" @click="click_item(item)">
                    <span style="margin-left: 5px">{{ item.title?item.title:item.name }}</span>
                </li>
            </ul>
        </div>
        <!-- <el-table
            :data="tableData"
            :show-header="false"
            style="width: 100%; cursor:pointer">
            <el-table-column
                prop="title"
                width="250"
                @click="item">
                <template slot-scope="scope">
                    <span style="margin-left: 10px">{{ scope.row.title }}</span>
                    <i class="iconfont" :class="scope.row.visible?'' : 'icon-eye-close'" v-if="type=='collection'"></i>
                    <span v-if="type=='special'"> ({{scope.row.count}})</span>
                </template>
            </el-table-column>
        </el-table> -->
        <div style="clear:both;float:none"></div>
        <vcd v-if="type=='collection'" ref="vcd" :title="'收藏夹：'+c_title"></vcd>
        <vsd v-if="type=='special'" ref="vsd" :title="'专栏：'+s_title"></vsd>
    </div>
</template>

<script>
export default {
    props: {
        title:{
            type:String,
            default:''
        },
        // list:{
        //     type:Array,
        //     default(){
        //         return [/*{title:'标题', count:0, visible:true},{title:'标题', count:1}*/];
        //     }
        // },
        type:{
            type:String,
            default:'list'
        },
        editable:{
            type:Boolean,
            default:false
        },
        edittitle:{
            type:String,
            default:'编辑'
        },
        uid:{
            type:Number,
            default:0
        }
    },
    data () {
        return {
            c_title:'',
            s_title:'',
            loading:true,
            list:[]
        }
    },
    methods:{
        click_item(item){
            if(this.type == 'collection'){
                this.click_collection(item.cid, item.title);
            }
            else if(this.type == 'special'){
                this.click_special(item.sid, item.name);
            }
            else if(this.type == 'relative_article'){
                this.click_article(item.aid);
            }
            else if(this.type == 'relative_resource'){
                this.click_resource(item.rid);
            }
        },

        click_collection(cid, cname){
            this.c_title = cname;
            var that = this;
            setTimeout(function(){
                that.$refs.vcd.open(cid);
            }, 0);
        },

        click_special(sid, sname){
            this.s_title = sname;
            var that = this;
            setTimeout(function(){
                that.$refs.vsd.open(sid);
            }, 0);
        },

        click_article(aid){
            this.$router.push({path:'/article/'+aid});
        },

        click_resource(rid){
            this.$router.push({path:'/resource/'+rid});
        },

        init(aid, rid){
            this.$refs.vsd && this.$refs.vsd.close();
            this.$refs.vcd && this.$refs.vcd.close();
            if(this.type == 'collection'){
                this.apply_for_collection_info();
            }
            else if(this.type == 'special'){
                this.apply_for_special_info();
            }
            else if(this.type=='relative_article' || this.type=='relative_resource'){
                this.apply_for_relative_info(aid, rid);
            }
            else{
                this.loading = false;
            }
        },

        getCookie (name) {
            var value = '; ' + document.cookie
            var parts = value.split('; ' + name + '=')
            if (parts.length === 2) return parts.pop().split(';').shift()
        },

        apply_for_collection_info(){
            var that = this;
            that.loading = true;
            that.list = [];
            $.ajax({ 
                type:'get', 
                url:"/collection/list?uid="+that.uid,
                headers: {'X-CSRFToken': this.getCookie('csrftoken')}, 
                processData: false,
                contentType: false,
                success:function (res){ 
                    that.list = res.collections;
                    setTimeout(function(){
                        that.loading = false;
                    }, 0);
                },
                error:function(){
                    console.log('连接失败');
                }
            });
        },

        apply_for_special_info(){
            var that = this;
            that.loading = true;
            that.list = [];
            $.ajax({ 
                type:'get', 
                url:"/create/special/list?uid="+that.uid,
                headers: {'X-CSRFToken': this.getCookie('csrftoken')}, 
                processData: false,
                contentType: false,
                success:function (res){ 
                    that.list = res.list;
                    setTimeout(function(){
                        that.loading = false;
                    }, 0);
                },
                error:function(){
                    console.log('连接失败');
                }
            });
        },

        apply_for_relative_info(aid, rid){
            var url = (aid ? '/article' : '/resource') + '/relative?count=10&' + (aid ? 'aid='+aid : 'rid='+rid);
            var that = this;
            that.loading = true;
            that.list = [];
            $.ajax({ 
                type:'get', 
                url:url,
                headers: {'X-CSRFToken': this.getCookie('csrftoken')}, 
                processData: false,
                contentType: false,
                success:function (res){
                    if(aid){
                        that.list = res.article;
                    }
                    else{
                        that.list = res.resource;
                    }
                    setTimeout(function(){
                        that.loading = false;
                    }, 0);
                },
                error:function(){
                    console.log('连接失败');
                }
            });
        },

        click_edit(){
            if(this.type == 'collection'){
                this.$router.push({path:'/collection', query:{from:this.$route.path}});
            }
            else if(this.type == 'special'){
                this.$router.push({path:'/create/special', query:{from:this.$route.path}});
            }
        }
    }
}
</script>

<style scoped>
@import url("../assets/common.css");
@import "../assets/side_block.css";

.list_block{
    
}

.list_block ul{
    padding:0 5px;
    margin: 5px 0 0;
    line-height:2em
}

.list_block li{
    list-style: none;
    text-align: left;
    font-size:15px;
    display: -webkit-box;
    -webkit-box-orient: vertical;
    -webkit-line-clamp: 1;
    overflow: hidden;
    height:32px
}

.list_block li:hover{
    color:hsl(1, 69%, 69%);
}

.icon-eye-close{
    margin-left:.6em
}

.list_block>div{
    width:100%;
    text-align: center;
    float: left;
    cursor: pointer;
}

.list_block .data_num{
    font-size: 35px;
    font-weight: bold;
}

.el-divider{
    margin:3px 0 10px;
}

.iconfont{
    font-size: 110%;
}
</style>

