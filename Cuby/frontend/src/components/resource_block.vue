<template>
    <div class="info_block" v-loading="loading">
        <h1 @click="to_resource">
            <el-tag class="label top" type="info" v-if="top">置顶</el-tag>
            <el-tag class="label" type="warning" v-if="type=='collection'||type=='collection_view'||type=='search'">资源</el-tag>
            <el-tag class="label">{{tag}}</el-tag>
            <span style="display:inline-block;width:3px"></span>
            <a v-if="type!='search'">{{title}}</a>
            <a v-if="type=='search'" v-html="title"></a>
        </h1>
        <div class="intro" v-if="type!='search'">{{intro}}</div>
        <div class="intro" v-if="type=='search'" v-html="intro"></div>
        <div class="ft">
            <div class="op">
                <ul>
                    <li><i slot="prefix" class="el-input__icon iconfont icon-like"></i> {{like}}</li>
                    <li><i slot="prefix" class="el-input__icon iconfont icon-message"></i> {{comment_cnt}}</li>
                    <li><i slot="prefix" class="el-input__icon iconfont icon-star"></i> {{collect}}</li>
                    <li><i slot="prefix" class="el-input__icon iconfont icon-eye"></i> {{view}}</li>
                </ul>
            </div>
            <div class="detail">
                <li v-for="label in detail" :key="label">{{label.key}}：{{label.value}}</li>
                <div class="clear_both"></div>
            </div>
            <div class="author" v-if="type=='search' || type=='collection_view'" @click="to_userinfo">
                <span style="line-height: 28px;vertical-align: middle;display: inline-block;height: 28px; margin-right:3px" :class="is_member?'member_color':''">{{author_name}}</span>
                <el-avatar :src="author_p_src" size="small" style="vertical-align: middle;"></el-avatar>
            </div>
            <div class="edit" v-if="type=='edit'">
                <el-popconfirm
                    title="你确定要删除吗？"
                    @onConfirm="del()">
                    <el-button slot="reference">删除</el-button>
                </el-popconfirm>
                <el-button @click="click_edit">编辑</el-button>
            </div>
            <div class="collection" v-if="type=='collection'">
                <el-button @click="cancel_collect">{{cancel_text}}</el-button>
                <el-button @click="move">移动</el-button>
            </div>
        </div>
        <div class="clear_both"></div>
    </div>
</template>

<script>
export default {
    props: {
        type: {
            type:String,
            default: 'view'
        },
        rid: {
            type:Number,
            default:0
        },
        top:{
            type:Boolean,
            default:false
        }
    },
    data () {
        return {
            title:'',
            tag:'',
            url:'/',
            intro:'',
            like:0,
            collect:0,
            comment_cnt:0,
            view:0,
            detail:[],
            ruid:0,
            author_p_src:'',
            author_name:'',
            cancel_text:'取消收藏',
            is_member:false,
            loading:true
        }
    },
    methods:{
        init(args){
            this.apply_for_info(args);
        },
        getCookie (name) {
            var value = '; ' + document.cookie
            var parts = value.split('; ' + name + '=')
            if (parts.length === 2) return parts.pop().split(';').shift()
        },
        apply_for_info(args){
            var that = this;
            that.loading = true;
            $.ajax({ 
                type:'get', 
                url:"/base/resource_view?rid="+that.rid,
                headers: {'X-CSRFToken': this.getCookie('csrftoken')}, 
                processData: false,
                contentType: false,
                success:function (res){ 
                    if(that.type=='search' && args && args.length){
                        res.title = that.checkData(res.title);
                        res.simple_content = that.checkData(res.simple_content);
                        for(let i=0; i<args.length; i++){
                            args[i] = that.checkData(args[i]);
                            let reg = new RegExp(args[i], 'g');
                            res.title = res.title.replace(reg, '<hl>'+args[i]+'</hl>');
                            res.simple_content = res.simple_content.replace(reg, '<hl>'+args[i]+'</hl>');
                        }
                    }
                    that.title = res.title;
                    that.tag = res.tag;
                    that.intro = res.simple_content;
                    that.url = '/resource/'+that.rid;
                    that.view = res.views;
                    that.like = res.likes;
                    that.collect = res.stars;
                    that.comment_cnt = res.comments;
                    that.author_p_src = res.author_portrait_url;
                    that.author_name = res.author_name;
                    that.ruid = res.ruid;
                    that.is_member = res.author_is_member;
                    that.loading = false;
                    that.$emit('done');
                },
                error:function(){
                    console.log('连接失败');
                    that.$emit('done');
                }
            });
        },
        click_edit(){
            this.$emit('edit_resource', this.rid);
        },
        del(){
            var that = this;
            $.ajax({ 
                type:'post', 
                url:"/create/resource/delete",
                headers: {'X-CSRFToken': this.getCookie('csrftoken')}, 
                data: JSON.stringify({rid:that.rid}),
                processData: false,
                contentType: false,
                success:function (res){ 
                    if(res.status == 0){
                        that.alert_msg.success('删除成功');
                        that.$emit('refresh', 'delete');
                    }
                    else{
                        that.alert_msg.error('删除失败');
                    }
                },
                error:function(){
                    that.alert_msg.error('连接失败');
                }
            });
        },
        to_resource(){
            if(this.$route.name=='resource' && this.$route.params.id==this.aid){
                this.alert_msg.warning('你已经在浏览这个资源啦');
                return;
            }
            this.$router.push({path:'/resource/'+this.rid});
        },
        cancel_collect(){
            var that = this;
            if(that.cancel_text == '取消收藏'){
                $.ajax({ 
                    type:'post', 
                    url:"/collection/remove_article",
                    headers: {'X-CSRFToken': this.getCookie('csrftoken')}, 
                    data: JSON.stringify({aid:that.aid,cid:that.cid}),
                    processData: false,
                    contentType: false,
                    success:function (res){ 
                        if(res.status == 0){
                            that.cancel_text = '收藏';
                        }
                        else{
                            that.alert_msg.error('取消失败');
                        }
                    },
                    error:function(){
                        that.alert_msg.error('连接失败');
                    }
                });
            }
            else{
                $.ajax({ 
                    type:'post', 
                    url:"/collection/remove_resource",
                    headers: {'X-CSRFToken': this.getCookie('csrftoken')}, 
                    data: JSON.stringify({rid:that.rid,cid:that.cid}),
                    processData: false,
                    contentType: false,
                    success:function (res){ 
                        if(res.status == 0){
                            that.cancel_text = '取消收藏';
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
        },
        move(){
            this.$emit('open_move_window', 'resource', this.rid);
        },
        checkData(v) {
            return v.replace(/[<>"&]/g, function(match, pos, originalText){
                    switch(match){
                    case "<": return "&lt;"; 
                    case ">":return "&gt;";
                    case "&":return "&amp;"; 
                    case "\"":return "&quot;"; 
                } 
            }); 
        },
        to_userinfo(){
            if(this.$route.name=='userInfo' && this.$route.params.id==this.ruid){
                this.alert_msg.warning('你已经在作者的个人空间里啦');
                return;
            }
            this.$router.push({path:'/userInfo/'+this.ruid});
        }
    }
}
</script>

<style scoped>
@import "../assets/list_button.css";
@import url("../assets/common.css");

.info_block{
    border-bottom:1px solid #ddd;
    padding:10px 15px 6px 15px;
}

.info_block:hover{
    background-color: #fafafa;
}

.info_block>h1{
    margin:0 0 5px 0;
    padding-right:.5em;
    /* height:40px; */
    line-height: 40px;
    font-size:25px;
    width: fit-content;
    cursor: pointer;
}

.author{
    float: right;
    font-size:15px;
}

h1:hover, .author:hover{
    color:hsl(1, 69%, 69%);
}

.detail{
    float: left;
}

.detail li{
    list-style: none;
    float: left;
    font-size: 13px;
    color: #bbb;
    margin: 0 1em;
    line-height: 28px;
}

.info_block>.intro{
    padding-left: 2em;
    margin:20px 0;
    font-size:15px;
}

.op{
    margin-top:15px;
    font-size:15px;
}

.op ul{
    padding-left:15px;
    line-height: 28px;
}

.op li{
    list-style: none;
    float:left;
    margin-right:25px;
    font-size: 13px;
}

.op>>>.el-input__icon{
    line-height:18px;
}

.edit{
    float: right;
    font-size:15px;
}

.info_block>h1>.label{
    font-size:13px;
    height:23px;
    margin:0 3px 5px 3px;
    font-weight: normal;
    cursor: default;
    vertical-align: middle;
    line-height: 23px;
}

.info_block>h1>.top{
    margin-right:-5px;
}

.el-popover{
    background: #fafafa;
}

.intro{
    display: -webkit-box;
    -webkit-box-orient: vertical;
    -webkit-line-clamp: 2;
    overflow: hidden;
    text-align: left;
}

.collection{
    float: right;
    font-size:15px;
    opacity: 0;
}

.info_block:hover .collection{
    opacity: 1;
}

.info_block>>>hl{
    color:hsl(1, 69%, 69%) !important;
    /* text-decoration: underline; */
}

.author{
    cursor: pointer;
    color:#aaa;
}
</style>

