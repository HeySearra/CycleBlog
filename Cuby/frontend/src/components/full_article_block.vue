<template>
    <div class="full_article_block" v-loading="loading">
        <div class="art_head">
            <h1>{{title}}</h1>
            <ul>
                <li>阅读量：{{views}}</li>
                <li v-for='item in art_detail' :key="item.key">{{item.key}}：{{item.value}}</li>
            </ul>
            <div class="clear_both"></div>
            <div class="tag_div">
                <el-tag v-for='title in label_list' :key="title" class="tag" type="info" @click="click_tag(title)">{{title}}</el-tag>
                <div class="clear_both"></div>
            </div>
        </div>
        <el-divider></el-divider>
        <div class="art_mid" id="art_mid">
            <mavon-editor
                class="md"
                :value="code"
                :subfield="false"
                :defaultOpen="'preview'"
                :toolbarsFlag="false"
                :editable="false"
                :scrollStyle="true"
                :ishljs="true"
            />
        </div>
        <div class="art_foot">
            <div @click="click_like" class="pointer user_option" :class="like_condition?'user_option--active':'user_option--noactive'"><i slot="prefix" class="el-input__icon iconfont icon-like"></i> 点赞 {{likes}}</div>
            <div @click="click_collection" class="pointer user_option" :class="collection_condition?'user_option--active':'user_option--noactive'"><i slot="prefix" class="el-input__icon iconfont icon-star"></i> 收藏 {{collection}}</div>
            <div id="report" @click="click_report" class="pointer user_option" v-if="!self"><i slot="prefix" class="el-input__icon iconfont icon-error"></i> 举报</div>
            <div class="clear_both"></div>
        </div>
        <el-dialog title="" :visible.sync="dialogVisible">
            <div class="dialog-mid">
                <cocb :aid="aid" ref="cocb" title="请选择收藏夹"></cocb>
            </div>
            <div slot="footer" class="dialog-footer">
                <el-button @click="dialogVisible = false">取 消</el-button>
                <el-button type="primary" @click="add_collection">确 定</el-button>
            </div>
        </el-dialog>
        <el-dialog title="举报文章" :visible.sync="report_dialog">
            <div class="dialog-mid">
                <el-input
                    type="textarea"
                    :rows="5"
                    placeholder="请输入举报理由"
                    v-model="report"
                    resize="none"
                    maxlength="200"
                    show-word-limit>
                </el-input>
            </div>
            <div slot="footer" class="dialog-footer">
                <el-button @click="report_dialog = false">取 消</el-button>
                <el-button type="primary" @click="submit_report">确 定</el-button>
            </div>
        </el-dialog>
        <vtd ref="vtd"></vtd>
    </div>
</template>

<script>
export default {
    name:'full-art',
    props: {
        aid:{
            type:Number,
            default: 0
        },
    },
    data () {
        return {
            label_list: [/*'标签','标签','标签'*/],
            art_detail: [/*{k:'这是键', v:'这是值'}*/],
            title:'',
            code:'',
            views:0,
            likes:0,
            collection:0,
            like_condition:false,
            collection_condition:false,
            dialogVisible:false,
            report_dialog:false,
            report:'',
            self:false,
            loading:true
        }
    },
    mounted(){
        //this.init();
    },
    methods:{
        init(){
            this.$refs.vtd.close();
            this.apply_for_info();
            this.init_copy();
        },
        getCookie (name) {
            var value = '; ' + document.cookie
            var parts = value.split('; ' + name + '=')
            if (parts.length === 2) return parts.pop().split(';').shift()
        },
        apply_for_info(){
            var that = this;
            that.loading = true;
            $.ajax({ 
                type:'get', 
                url:"/article/all?aid="+that.aid,
                headers: {'X-CSRFToken': this.getCookie('csrftoken')}, 
                processData: false,
                contentType: false,
                success:function (res){ 
                    if(res.title && res.title!=""){
                        that.title = res.title;
                        that.code = res.content;
                        that.views = res.views;
                        that.collection = res.stars;
                        that.likes = res.likes;
                        that.label_list = res.tags;
                        that.art_detail = res.detail;
                        document.title = res.title;
                        that.like_condition = res.user_options.is_like==1;
                        that.collection_condition = res.user_options.is_star==1;
                        that.self = that.login_manager.get_uid()==res.auid;
                        that.$emit('init_author_card', res.auid);
                        that.loading = false;
                        that.$emit('done');
                    }
                },
                error:function(){
                    console.log('连接失败');
                    that.$emit('done');
                }
            });
        },
        click_like(){
            if(!this.login_manager.get()){
                this.alert_msg.warning('请先登录才能点赞');
                return;
            }
            var that = this;
            $.ajax({ 
                type:'post', 
                url:"/article/like",
                headers: {'X-CSRFToken': that.getCookie('csrftoken')}, 
                data: JSON.stringify({aid:that.aid, condition:!that.like_condition}),
                async:false,
                success:function (res){ 
                    if(res.status == 0){
                        that.likes += that.like_condition?-1:1;
                        that.like_condition = !that.like_condition;
                    }
                    else{
                        that.alert_msg.error(that.likes?'取消点赞失败':'点赞失败');
                    }
                },
                error:function(){
                    that.alert_msg.error('连接失败');
                }
            });
        },
        click_collection(){
            if(!this.login_manager.get()){
                this.alert_msg.warning('请先登录才能收藏');
                return;
            }
            var that = this;
            if(that.collection_condition){
                $.ajax({ 
                    type:'post', 
                    url:"/collection/remove_article",
                    headers: {'X-CSRFToken': that.getCookie('csrftoken')}, 
                    data: JSON.stringify({aid:that.aid}),
                    async:false,
                    success:function (res){ 
                        if(res.status == 0){
                            that.collection -= 1;
                            that.collection_condition = false;
                        }
                        else{
                            that.alert_msg.error('取消收藏失败');
                        }
                    },
                    error:function(){
                        that.alert_msg.error('连接失败');
                    }
                });
            }
            else{
                that.dialogVisible = true;
                setTimeout(function(){
                    that.$refs.cocb.clear_chosen();
                    if(that.$refs.cocb.init()){}
                    else{
                        that.dialogVisible = false;
                        that.alert_msg.error('加载信息失败');
                    }
                }, 0);
            }
        },
        add_collection(){
            if(this.$refs.cocb.add_collection()){
                this.dialogVisible = false;
                this.collection += 1;
                this.collection_condition = true;
            }
        },
        click_report(){
            if(!this.login_manager.get()){
                this.alert_msg.warning('请先登录才能举报');
                return;
            }
            this.report = '',
            this.report_dialog = true;
        },
        submit_report(){
            var that = this;
            if(that.report == ''){
                that.alert_msg.warning('请填写举报理由');
                return;
            }
            $.ajax({ 
                type:'post', 
                url:"/article/complain",
                headers: {'X-CSRFToken': that.getCookie('csrftoken')}, 
                data: JSON.stringify({aid:that.aid, reason:that.report}),
                async:false,
                success:function (res){ 
                    if(res.status == 0){
                        that.alert_msg.success('举报成功');
                        that.report_dialog = false;
                    }
                    else{
                        that.alert_msg.error('举报失败');
                    }
                },
                error:function(){
                    that.alert_msg.error('连接失败');
                }
            });
        },
        click_tag(keyword){
            this.$refs.vtd.open(keyword);
        },
        init_copy(){
            $("#art_mid").off('bind');
            $("#art_mid").bind('copy', function (e) {
                if (typeof window.getSelection == "undefined") return; //IE8 及更老的版本不兼容
                
                var body_element = document.getElementsByTagName('body')[0];
                var selection = window.getSelection();
                
                if (("" + selection).length < 30) return;

                if(("" + selection).indexOf('文章来源于 Cuby，链接为')!=-1) return;
            
                //创建一个DIV的可见区域之外
                //并填写选定的文本
                var newdiv = document.createElement('div');
                newdiv.style.position = 'absolute';
                newdiv.style.left = '-99999px';
                body_element.appendChild(newdiv);
                newdiv.appendChild(selection.getRangeAt(0).cloneContents());
                
                //我们需要<pre>标签解决方案
                //其他的文本在<pre>失去了所有的行符！
                if (selection.getRangeAt(0).commonAncestorContainer.nodeName == "PRE") {
                    newdiv.innerHTML = "<pre>" + newdiv.innerHTML + "</pre>";
                }
                
                newdiv.innerHTML += "<br /><br />文章来源于 Cuby，链接为："+location.href;
                selection.selectAllChildren(newdiv);
                window.setTimeout(function () { body_element.removeChild(newdiv);}, 200);
            });
        }
    }
}
</script>

<style scoped>
@import "../assets/tag.css";
@import url("../assets/common.css");

.full_article_block{
    padding:0;
}

h1{
    margin:0 0 15px .5em;
    font-size: 30px;
}

ul{
    padding-left: 15px;
    font-size: 13px;
}

ul li{
    list-style: none;
    float: left;
    margin-right:50px;
}

.tag_div{
    margin: 20px 0 0 0;
    padding-left: 10px;
}

.art_head, .art_mid{
    padding:0 20px;
}

.art_mid{
    font-size: 15px;;
    line-height: 27px;
    padding:0 35px;
}

.art_foot{
    margin-top:50px;
    padding:0 1.5em;
    font-size: 15px;
    border-bottom: #ddd 1px solid;
    line-height: 39px;
}

.art_foot>div{
    float: left;
    margin-right:35px;
}

#report{
    float: right;
    margin-right:0;
}

.md{
    background-color: rgba(0, 0, 0, 0) !important;
    box-shadow: none !important;
}

.md>>>.v-show-content{
    background-color: rgba(0, 0, 0, 0) !important;
    padding:0 !important;
}


.art_mid>>>.markdown-body .hljs{
    overflow: unset !important;
}

.art_mid>>>.v-show-content p{
    line-height: 30px;
    margin-bottom:18px
}

.art_mid>>>pre code{
    font-size: 100%;
    line-height:21px;
}

.art_mid>>>.markdown-body pre::-webkit-scrollbar, .art_mid>>>table::-webkit-scrollbar {
    width:6px;
    height:6px;
    padding-right:5px;
}

.art_mid>>>.markdown-body pre::-webkit-scrollbar-thumb, .art_mid>>>table::-webkit-scrollbar{
    border-radius: 3px;
    background-color: #ccc;
}

.art_mid>>>.markdown-body pre::-webkit-scrollbar-corner, .art_mid>>>table::-webkit-scrollbar-corner::-webkit-scrollbar{
    display: none;
}

.art_mid>>>table{
    overflow-y: hidden;
}
</style>
