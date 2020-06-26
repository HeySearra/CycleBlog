<template>
    <div class="full_article_block" v-loading="loading">
        <div class="art_head">
            <h1>{{title}}</h1>
            <ul>
                <li>浏览量：{{views}}</li>
                <li v-for='item in detail' :key="item.key">{{item.key}}：{{item.value}}</li>
            </ul>
            <div class="clear_both"></div>
            <div class="tag_div">
                <el-tag v-for='title in label_list' :key="title" class="tag" type="info" @click="click_tag(title)">{{title}}</el-tag>
                <div class="clear_both"></div>
            </div>
            <div style="text-align:right">
                <el-button @click="click_download"><span v-if="!is_buy">{{point}} 积分</span><span v-if="is_buy">已购买</span> 立即下载</el-button>
                <el-button @click="click_vip_download" type="primary">VIP免费下载</el-button>
            </div>
        </div>
        <el-divider></el-divider>
        <div class="art_mid" style="line-height:35px">
            {{introduction}}
        </div>
        <div class="art_foot">
            <div @click="click_like" class="pointer user_option" :class="like_condition?'user_option--active':'user_option--noactive'"><i slot="prefix" class="el-input__icon iconfont icon-like"></i> 点赞 {{likes}}</div>
            <div @click="click_collection" class="pointer user_option" :class="collection_condition?'user_option--active':'user_option--noactive'"><i slot="prefix" class="el-input__icon iconfont icon-star"></i> 收藏 {{collection}}</div>
            <div id="report" @click="click_report" class="pointer user_option" v-if="!self"><i slot="prefix" class="el-input__icon iconfont icon-error"></i> 举报</div>
            <div class="clear_both"></div>
        </div>
        <el-dialog title="" :visible.sync="dialogVisible">
            <div class="dialog-mid">
                <cocb :rid="rid" ref="cocb" title="请选择收藏夹"></cocb>
            </div>
            <div slot="footer" class="dialog-footer">
                <el-button @click="dialogVisible = false">取 消</el-button>
                <el-button type="primary" @click="add_collection">确 定</el-button>
            </div>
        </el-dialog>
        <el-dialog title="举报资源" :visible.sync="report_dialog">
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
    name:'full-res',
    props: {
        rid:{
            type:Number,
            default: 0
        },
    },
    data () {
        return {
            label_list: [/*'标签','标签','标签'*/],
            detail: [/*{key:'这是键', value:'这是值'}*/],
            title:'',
            introduction:'',
            views:0,
            point:0,
            is_buy:false,
            ruid:0,
            like_condition:false,
            collection_condition:false,
            likes:0,
            collection:0,
            dialogVisible:false,
            report_dialog:false,
            report:'',
            self:false,
            loading:true
        }
    },
    methods:{
        init(){
            this.$refs.vtd.close();
            this.apply_for_info();
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
                url:'/resource/all?rid='+that.rid,
                headers: {'X-CSRFToken': this.getCookie('csrftoken')}, 
                processData: false,
                contentType: false,
                success:function (res){ 
                    that.title = res.title;
                    that.introduction = res.description;
                    that.views = res.views;
                    that.collection = res.stars;
                    that.likes = res.likes;
                    that.point = res.points;
                    that.is_buy = res.user_options.is_buy;
                    that.label_list = res.tags;
                    that.ruid = res.ruid;
                    that.self = res.ruid==that.login_manager.get_uid();
                    that.like_condition = res.user_options.is_like;
                    that.collection_condition = res.user_options.is_star;
                    that.detail = res.detial;
                    document.title = res.title;
                    that.$emit('init_author_card', res.ruid);
                    that.loading = false;
                    that.$emit('done');
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
                url:"/resource/like",
                headers: {'X-CSRFToken': that.getCookie('csrftoken')}, 
                data: JSON.stringify({rid:that.rid, condition:!that.like_condition}),
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
                    url:"/collection/remove_resource",
                    headers: {'X-CSRFToken': that.getCookie('csrftoken')}, 
                    data: JSON.stringify({rid:that.rid}),
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
                    var res = that.$refs.cocb.init();
                    if(res){}
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
                url:"/resource/complain",
                headers: {'X-CSRFToken': that.getCookie('csrftoken')}, 
                data: JSON.stringify({rid:that.rid, reason:that.report}),
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
        click_download(){
            if(this.is_buy){
                this.apply_for_download();
            }
            else{
                var vip_flag = false;
                $.ajax({ 
                    type:'get', 
                    url:'/simple_user_info',
                    headers: {'X-CSRFToken': this.getCookie('csrftoken')}, 
                    async:false,
                    success:function (res){ 
                        vip_flag = res.is_member;
                    }
                });
                if(vip_flag){
                    this.alert_msg.success('尊敬的会员，您可以免费下载这个资源');
                    this.apply_for_download();
                }
                else{
                    this.alert_box.confirm_msg('提示', '你确定扣除相应的积分并下载这个资源吗？', this.apply_for_download);
                }
            }
        },
        click_vip_download(){
            var that = this;
            var vip_flag = false;
            var fail_flag = false;
            $.ajax({ 
                type:'get', 
                url:'/simple_user_info',
                headers: {'X-CSRFToken': this.getCookie('csrftoken')}, 
                async:false,
                success:function (res){ 
                    vip_flag = res.is_member;
                },
                error:function(){
                    that.alert_msg.error('连接失败');
                    fail_flag = true;
                }
            });
            if(fail_flag){
                return;
            }
            if(vip_flag){
                that.apply_for_download();
            }
            else{
                that.alert_box.msg('提示', '你还不是会员，需要充值会员才能使用 VIP 免费下载资源');
            }
        },
        apply_for_download(){
            var that = this;
            $.ajax({ 
                type:'post', 
                url:"/resource/download",
                headers: {'X-CSRFToken': that.getCookie('csrftoken')}, 
                data: JSON.stringify({rid:that.rid}),
                async:false,
                success:function (res){ 
                    if(res.status == 0){
                        window.open(res.src);
                    }
                    else{
                        switch(res.status){
                            case 1:
                                that.alert_msg.error('积分余额不足');
                                break;
                            default:
                                that.alert_msg.error('下载失败，请重试');
                        }
                    }
                },
                error:function(){
                    that.alert_msg.error('连接失败');
                }
            });
        },
        click_tag(keyword){
            this.$refs.vtd.open(keyword);
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
    margin:0 0 15px 0;
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

.art_head{
    padding:0 30px
}

.art_mid{
    font-size: 15px;;
    padding:0 1.5em;
    line-height: 27px;
}

.art_foot{
    margin-top:50px;
    padding:0 1.5em;
    font-size: 15px;
    /* background-color: #f1f1f1; */
    line-height: 39px;
}

.art_foot>div{
    float: left !important;
    margin-right:35px;
}

#report{
    float: right !important;
    margin-right:0;
}
</style>
