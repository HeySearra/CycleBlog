<template>
    <div class="info_block" v-loading="loading" :class="nh?'not_hover':''">
        <h1 @click="to_article" :style="opa01?'filter:blur(5px)':''">
            <el-tag class="label top" type="info" v-if="top">置顶</el-tag>
            <el-tag class="label" type="success" v-if="type=='collection'||type=='collection_view'||type=='search'||type=='collection'||type=='collection_view'||type=='recommend'">文章</el-tag>
            <el-tag class="label">{{tag}}</el-tag>
            <span style="display:inline-block;width:3px"></span>
            <a v-if="type!='search'">{{title}}</a>
            <a v-if="type=='search'" v-html="title"></a>
        </h1>
        <div class="intro" v-if="type!='search'" :style="opa01?'filter:blur(5px)':''">{{intro}}</div>
        <div class="intro" v-if="type=='search'" v-html="intro"></div>
        <div class="ft" :style="opa01?'filter:blur(5px)':''">
            <div class="op cur_def" v-if="type!='recycle'">
                <ul>
                    <li><i slot="prefix" class="el-input__icon iconfont icon-like"></i> {{like}}</li>
                    <li><i slot="prefix" class="el-input__icon iconfont icon-message"></i> {{comment_cnt}}</li>
                    <li><i slot="prefix" class="el-input__icon iconfont icon-star"></i> {{collect}}</li>
                    <li><i slot="prefix" class="el-input__icon iconfont icon-eye"></i> {{view}}</li>
                </ul>
            </div>
            <div class="detail">
                <li v-for="label in detail" :key="label.key">{{label.key}}：{{label.value}}</li>
                <div class="clear_both"></div>
            </div>
            <div class="author" v-if="type=='recommend'|| type=='search' || type=='collection_view'" @click="to_userinfo" :style="opa01?'filter:blur(5px)':''">
                <span style="line-height: 28px;vertical-align: middle;display: inline-block;height: 28px; margin-right:3px" :class="is_member?'member_color':''">{{author_name}}</span>
                <el-avatar :src="author_p_src" size="small" style="vertical-align: middle;"></el-avatar>
            </div>
            <div class="edit" v-if="type=='edit'">
                <el-popconfirm
                    title="你确定要删除吗？"
                    @onConfirm="del">
                    <el-button slot="reference">删除</el-button>
                </el-popconfirm>
                <el-button @click="edit">编辑</el-button>
                <el-popconfirm
                    title="你确定要置顶吗？"
                    @onConfirm="click_top">
                    <el-button slot="reference">{{top?'取消置顶':'置顶'}}</el-button>
                </el-popconfirm>
            </div>
            <div class="recycle" v-if="type=='recycle'">
                <el-popconfirm
                    title="你确定要彻底删除吗？"
                    @onConfirm="del_forever">
                    <el-button slot="reference">彻底删除</el-button>
                </el-popconfirm>
                <el-button @click="recover">恢复</el-button>
            </div>
            <div class="collection" v-if="type=='collection'">
                <el-button @click="cancel_collect">{{cancel_text}}</el-button>
                <el-button @click="move">移动</el-button>
            </div>
        </div>
        <div class="close_icon" v-if="!not_like && type=='recommend' && login_manager.get()" @click="dislike">
            <div><i class="el-icon-close"></i></div>
        </div>
        <div class="dark" :style="opa01?'opacity:0.11;filter:blur(0)':''" v-if="not_like"></div>
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
        aid:{
            type:Number,
            default:0
        },
        top:{
            type:Boolean,
            default:false
        },
        cid:{
            type:Number,
            default:0
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
            auid:0,
            author_p_src:'',
            author_name:'',
            detail:[/*{key:'发布时间',value:'2020-1-1'}*/],
            cancel_text:'取消收藏',
            loading:true,
            not_like:false,
            opa01:false,
            nh:false,
            is_member:false
        }
    },
    watch:{
        'not_like'(){
            var that = this;
            setTimeout(function(){
                that.opa01 = true;
            }, 0);
            setTimeout(function(){
                that.nh = true;
            }, 200);
        }
    },
    methods:{
        getCookie (name) {
            var value = '; ' + document.cookie
            var parts = value.split('; ' + name + '=')
            if (parts.length === 2) return parts.pop().split(';').shift()
        },
        init(args){
            if(this.aid == 0){
                return;
            }
            var that = this;
            that.loading = true;
            if(this.type == 'view' || this.type == 'collection' || this.type == 'collection_view' || this.type == 'search' || this.type == 'recommend'){
                $.ajax({ 
                    type:'get', 
                    url:"/base/article_view?aid="+that.aid,
                    headers: {'X-CSRFToken': this.getCookie('csrftoken')}, 
                    processData: false,
                    contentType: false,
                    success:function (res){
                        if(that.type=='search' && args && args.length){
                            res.title = that.checkData(res.title);
                            res.simple_content = that.checkData(res.simple_content);
                            for(let i=0; i<args.length; i++){
                                args[i] = that.checkData(args[i]);
                                let reg = new RegExp(args[i].replace(/[-\/\\^$*+?.()|[\]{}]/g, '\\$&'), 'ig');
                                res.title = res.title.replace(reg, function(word){
                                    return '<hl>'+word+'</hl>';
                                });
                                res.simple_content = res.simple_content.replace(reg, function(word){
                                    return '<hl>'+word+'</hl>';
                                });
                            }
                        }
                        that.title = res.title;
                        that.tag = res.tag;
                        that.intro = res.simple_content;
                        that.url = '/article/'+that.aid;
                        that.view = res.views;
                        that.like = res.likes;
                        that.collect = res.stars;
                        that.comment_cnt = res.comments;
                        that.author_p_src = res.author_portrait_url;
                        that.author_name = res.author_name;
                        that.is_member = res.author_is_member;
                        that.auid = res.auid;
                        that.loading = false;
                        that.$emit('done');
                    },
                    error:function(){
                        console.log('连接失败');
                        that.$emit('done');
                    }
                });
            }
            else if(this.type == 'edit'){
                $.ajax({ 
                    type:'get', 
                    url:"/create/article/article_edit?aid="+that.aid,
                    headers: {'X-CSRFToken': this.getCookie('csrftoken')}, 
                    processData: false,
                    contentType: false,
                    success:function (res){ 
                        that.title = res.title;
                        that.tag = res.tag;
                        that.intro = res.simple_content;
                        that.url = '/article/'+that.aid;
                        that.view = res.views;
                        that.like = res.likes;
                        that.collect = res.stars;
                        that.comment_cnt = res.comments;
                        that.detail = res.detail;
                        that.loading = false;
                        that.$emit('done');
                    },
                    error:function(){
                        console.log('连接失败');
                        that.$emit('done');
                    }
                });
            }
            else if(this.type == 'recycle'){
                $.ajax({ 
                    type:'get', 
                    url:"/create/recycle/article_recycle?aid="+that.aid,
                    headers: {'X-CSRFToken': this.getCookie('csrftoken')}, 
                    processData: false,
                    contentType: false,
                    success:function (res){ 
                        that.title = res.title;
                        that.tag = res.tag;
                        that.intro = res.simple_content;
                        that.detail = res.detail;
                        that.loading = false;
                        that.$emit('done');
                    },
                    error:function(){
                        console.log('连接失败');
                        that.$emit('done');
                    }
                });
            }
        },
        to_article(){
            if(this.type == 'recommend'){
                this.like_it();
            }
            if(this.$route.name=='article' && this.$route.params.id==this.aid){
                this.alert_msg.warning('你已经在这篇文章里啦');
                return;
            }
            if(this.type != 'recycle'){
                this.$router.push({path:'/article/'+this.aid});
            }
        },
        del(){
            var that = this;
            $.ajax({ 
                type:'post', 
                url:"/create/article/delete",
                headers: {'X-CSRFToken': this.getCookie('csrftoken')}, 
                data: JSON.stringify({aid:that.aid}),
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
        edit(){
            this.$router.push({path:'/edit/'+this.aid,query:{from:this.$route.path}});
        },
        click_top(){
            var that = this;
            $.ajax({ 
                type:'post', 
                url:"/create/article/top",
                headers: {'X-CSRFToken': this.getCookie('csrftoken')}, 
                data: JSON.stringify({aid:that.aid}),
                processData: false,
                contentType: false,
                success:function (res){ 
                    if(res.status == 0){
                        if(that.top){
                            that.alert_msg.success('已取消置顶');
                        }
                        else{
                            that.alert_msg.success('置顶成功');
                        }
                        that.$emit('refresh', 'top');
                    }
                    else{
                        that.alert_msg.error('置顶失败');
                    }
                },
                error:function(){
                    that.alert_msg.error('连接失败');
                }
            });
        },
        del_forever(){
            var that = this;
            $.ajax({ 
                type:'post', 
                url:"/create/recycle/delete",
                headers: {'X-CSRFToken': this.getCookie('csrftoken')}, 
                data: JSON.stringify({aid:that.aid}),
                processData: false,
                contentType: false,
                success:function (res){ 
                    if(res.status == 0){
                        that.alert_msg.success('删除成功');
                        that.$emit('refresh', 'delete_forever');
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
        recover(){
            var that = this;
            $.ajax({ 
                type:'post', 
                url:"/create/recycle/recover",
                headers: {'X-CSRFToken': this.getCookie('csrftoken')}, 
                data: JSON.stringify({aid:that.aid}),
                processData: false,
                contentType: false,
                success:function (res){ 
                    if(res.status == 0){
                        that.alert_msg.success('恢复成功');
                        that.$emit('refresh', 'delete_forever');
                    }
                    else{
                        that.alert_msg.error('恢复失败');
                    }
                },
                error:function(){
                    that.alert_msg.error('连接失败');
                }
            });
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
                    url:"/collection/add_article",
                    headers: {'X-CSRFToken': this.getCookie('csrftoken')}, 
                    data: JSON.stringify({aid:that.aid,cid:that.cid}),
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
            this.$emit('open_move_window', 'article', this.aid);
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
        dislike(){
            if(this.type != 'recommend'){
                return;
            }
            var that = this;
            $.ajax({ 
                type:'post', 
                url:"/index/recommend/dislike",
                headers: {'X-CSRFToken': this.getCookie('csrftoken')}, 
                data: JSON.stringify({aid:that.aid}),
                processData: false,
                contentType: false,
                success:function (res){ 
                    that.not_like = true;
                    that.alert_msg.success('我们会减少此类文章的推荐');
                },
                error:function(){
                    that.alert_msg.error('连接失败');
                }
            });
        },
        like_it(){
            var that = this;
            $.ajax({ 
                type:'post', 
                url:"/index/recommend/like",
                headers: {'X-CSRFToken': this.getCookie('csrftoken')}, 
                data: JSON.stringify({aid:that.aid}),
                processData: false,
                contentType: false,
                success:function (){},
                error:function(){}
            });
        },
        to_userinfo(){
            if(this.$route.name=='userInfo' && this.$route.params.id==this.auid){
                this.alert_msg.warning('你已经在作者的个人空间里啦');
                return;
            }
            this.$router.push({path:'/userInfo/'+this.auid});
        }
    }
}
</script>

<style scoped>
@import "../assets/list_button.css";
@import url("../assets/common.css");

.info_block{
    background-color: #fff;
    border-bottom:1px solid #ddd;
    padding:10px 15px 6px 15px;
    position: relative;
    transition:0.2s linear opacity;
}

.info_block:hover{
    background-color: #fafafa;
}

.not_hover:hover{
    background-color: #fff;
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

h1:hover{
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
    padding: 0 2em;
    margin:10px 0;
    font-size:15px;
    color:#888;
    line-height: 1.5em;
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

.author, .edit, .recycle, .collection{
    float: right;
    font-size:15px;
}

.collection{
    opacity: 0;
    /* transition:0.1s opacity linear; */
}

.info_block:hover .collection{
    opacity: 1;
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

.el-tag.el-tag--info{
    color: hsl(203, 100%, 63%);
    background-color: hsl(203, 100%, 96%);
    border-color: hsl(203, 100%, 93%);
}

.info_block>>>hl{
    color:hsl(1, 69%, 69%) !important;
    /* text-decoration: underline; */
}

.close_icon{
    position: absolute;
    top:10px;
    right:10px;
    cursor: pointer;
    display: none;
    color:#aaa;
}

.close_icon:hover, .author:hover{
    color:hsl(1, 69%, 69%);
}

.author{
    cursor: pointer;
    color:#aaa;
}

.info_block:hover .close_icon{
    display: block;
}

.disabled{
    opacity: 0.5;
    cursor: default !important;
}

.dark{
    width:100%;
    height:100%;
    background-color: #000;
    position: absolute;
    top:0;
    left:0;
    opacity: 0;
    transition:0.2s linear opacity;
}
</style>