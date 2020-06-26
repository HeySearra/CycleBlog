<template>
    <div class="comment_block" v-loading="loading">
        <div class="comment_input" id="comment_input">
            <el-input
                type="textarea"
                ref="textarea"
                :rows="2"
                :autosize="{ minRows: 2, maxRows: 5}"
                :placeholder="replying?reply_placeholder:default_placeholder"
                v-model="comment"
                resize="none"
                :disabled="!login_manager.get()"
                maxlength="200"
                show-word-limit>
            </el-input>
            <el-button type="primary" :disabled="comment==''" @click="submit">发表</el-button>
            <el-button v-show="replying" @click="cancel_reply">取消回复 {{reply_who}}</el-button>
            <div class="clear_both"></div>
        </div>
        <div class="others_comment" id="other_comment">
            <div v-if="qid_list.length==0" style="text-align:center;margin:50px 0;color:#aaa">
                这里还没有人评论呢
            </div>
            <div style="height:10px;width:100%" v-if="qid_list.length"></div>
            <h2 v-if="qid_list.length">评论</h2>
            <el-divider v-if="qid_list.length"></el-divider>
            <div>
                <div v-for="item in qid_list" :key="item">
                    <ccb :qid="item" ref="comment_list" :type="aid?'article':'resource'" @reply="reply" @report="click_report" @refresh="init"></ccb>
                    <el-divider></el-divider>
                </div>
            </div>
            <div class="pagination" v-if="qid_list.length&&total>page_size">
                <el-pagination
                    background
                    layout="total, prev, pager, next, jumper"
                    :page-size="page_size"
                    :total="total"
                    :current-page="current_page"
                    @current-change="change_page">
                </el-pagination>
            </div>
        </div>
        <el-dialog :title="'举报 '+report_name+' 的评论'" :visible.sync="report_dialog">
            <div class="dialog-mid">
                <el-input
                    type="textarea"
                    :rows="5"
                    placeholder="请输入举报理由"
                    v-model="report_content"
                    resize="none">
                </el-input>
            </div>
            <div slot="footer" class="dialog-footer">
                <el-button @click="report_dialog = false">取 消</el-button>
                <el-button type="primary" @click="submit_report">确 定</el-button>
            </div>
        </el-dialog>
    </div>
</template>

<script>
export default {
    props: {
        aid:{
            type:Number,
            default: 0
        },
        rid:{
            type:Number,
            default: 0
        }
    },
    data () {
        return {
            comment:'',
            replying:false,
            default_placeholder:'请在此输入评论',
            reply_placeholder:'回复',
            pqid:-1,
            qid_list:[],
            page_size:10,
            total:0,
            current_page:1,
            reply_who:'',
            loading:true,
            report_qid:0,
            report_name:0,
            report_content:'',
            report_dialog:false,
        }
    },
    methods:{
        getCookie (name) {
            var value = '; ' + document.cookie
            var parts = value.split('; ' + name + '=')
            if (parts.length === 2) return parts.pop().split(';').shift()
        },
        init(){
            if(!this.login_manager.get()){
                this.default_placeholder = '请先登录再评论';
            }
            this.comment = '';
            this.current_page = 1;
            this.apply_for_info();
        },
        apply_for_info(){
            var that = this;
            that.loading = true;
            var url = (that.aid?'/article/comment?aid='+that.aid:'/resource/comment?rid='+that.rid)+'&page='+that.current_page+'&each='+that.page_size;
            $.ajax({ 
                type:'get', 
                url:url,
                headers: {'X-CSRFToken': this.getCookie('csrftoken')}, 
                processData: false,
                contentType: false,
                success:function (res){ 
                    that.qid_list = res.comment;
                    that.total = res.amount;
                    setTimeout(function(){
                        if(that.qid_list.length){
                            let item = that.$refs.comment_list;
                            for(var i=0; i<item.length; i++){
                                item[i].init();
                            }
                        }
                    }, 0);
                    that.$emit('done');
                    that.loading = false;
                },
                error:function(){
                    console.log('连接失败');
                }
            });
        },
        reply(pqid, uname){
            this.comment = '';
            this.replying = true;
            this.reply_placeholder = '回复：'+uname;
            this.reply_who = uname;
            this.pqid = pqid;
            this.$refs.textarea.focus();
            document.getElementById('comment_input').scrollIntoView({behavior: "smooth"});
        },
        cancel_reply(){
            this.replying = false;
            this.comment = '';
            this.pqid = -1;
        },
        submit(){
            var that = this;
            if(this.comment == ''){
                return;
            }
            var msg = {};
            msg.content = that.comment;
            msg.pqid = that.replying?that.pqid:-1;
            if(this.aid){
                msg.aid = that.aid;
                $.ajax({ 
                    type:'post', 
                    url:"/article/comment/submit",
                    headers: {'X-CSRFToken': that.getCookie('csrftoken')}, 
                    data: JSON.stringify(msg),
                    async:false,
                    success:function (res){ 
                        if(res.status == 0){
                            that.alert_msg.success('评论成功');
                            that.init();
                            that.cancel_reply();
                        }
                        else{
                            switch(res){
                                case 1:
                                    that.alert_msg.error('文章不存在');
                                    break;
                                case 2:
                                    that.alert_msg.error('回复失败');
                                    break;
                                default:
                                    that.alert_msg.error('评论失败');
                            }
                        }
                    },
                    error:function(){
                        that.alert_msg.error('连接失败');
                    }
                });
            }
            else if(this.rid){
                msg.rid = that.rid;
                $.ajax({ 
                    type:'post', 
                    url:"/resource/comment/submit",
                    headers: {'X-CSRFToken': that.getCookie('csrftoken')}, 
                    data: JSON.stringify(msg),
                    async:false,
                    success:function (res){ 
                        if(res.status == 0){
                            that.alert_msg.success('评论成功');
                            that.init();
                            document.getElementById('comment_input').scrollIntoView();
                            that.cancel_reply();
                        }
                        else{
                            switch(res){
                                case 1:
                                    that.alert_msg.error('文章不存在');
                                    break;
                                case 2:
                                    that.alert_msg.error('回复失败');
                                    break;
                                default:
                                    that.alert_msg.error('评论失败');
                            }
                        }
                    },
                    error:function(){
                        that.alert_msg.error('连接失败');
                    }
                });
            }
        },
        change_page(arg){
            document.getElementById('comment_input').scrollIntoView({behavior: 'smooth', block:'start'});
            this.current_page = arg;
            this.apply_for_info();
        },
        click_report(qid, name){
            this.report_qid = qid;
            this.report_name = name;
            this.report_content = '';
            this.report_dialog = true;
        },
        submit_report(){
            var that = this;
            if(that.report == ''){
                that.alert_msg.warning('请填写举报理由');
                return;
            }
            var url = (this.aid ? '/article' : '/resource') + '/comment/complain';
            $.ajax({ 
                type:'post', 
                url:url,
                headers: {'X-CSRFToken': that.getCookie('csrftoken')}, 
                data: JSON.stringify({qid:that.report_qid, reason:that.report_content}),
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
        }
    }
}
</script>

<style scoped>
@import url("../assets/common.css");

.comment_block{
    padding:10px 20px !important;
}

h1{
    margin-bottom:10px
}

.comment_input{
    padding:0 10px;
}

.comment_input>>>textarea{
    border-radius: 3px;
    transition:0.1s all ease;
}

.comment_input>>>textarea::-webkit-scrollbar {
	width:6px;
	height:6px;
	padding-right:5px;
}

.comment_input>>>textarea::-webkit-scrollbar-thumb{
    border-radius: 3px;
	background-color: #ccc;
}

.comment_input>>>textarea::-webkit-scrollbar-corner{
    display: none;
}

.comment_input>>>.el-button{
    line-height: 18px;
    padding:5px 15px;
    border-radius: 3px;
    float: right;
    margin-top:10px;
    margin-left:10px;
}

.el-divider{
    margin:0;
}

.pagination{
    margin-top:30px;
    text-align: center;
    font-weight: normal;
}

.others_comment{
    padding:0 30px;
}
</style>
