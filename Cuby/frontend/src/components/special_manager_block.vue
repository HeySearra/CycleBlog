<template>
    <div style="padding:10px 30px" class="spmb" :class="special_list.length!=0?'mb0':''">
        <div>
            <h2>我的专栏
                <div style="float:right">
                    <el-button type="primary" @click="click_add">新建专栏</el-button>
                </div>
            </h2>
            <el-divider class="margin_bottom0"></el-divider>
            <div v-if="!special_list.length&&!loading" class="not_found">你还没有任何专栏</div>
            <div v-if="loading" class="not_found">加载中 <i class="el-icon-loading"></i></div>
            <div v-for="item in special_list" :key="item.sid">
                <splb @edit="edit" :title="item.name" :sid="item.sid" :count="item.count" @refresh="delete_refresh"></splb>
                <el-divider class="margin0"></el-divider>
            </div>
        </div>
        <div class="pagination" v-if="special_list.length&&total>page_size">
            <el-pagination
                background
                layout="total, prev, pager, next, jumper"
                :page-size="page_size"
                :total="total"
                :current-page="current_page"
                @current-change="change_page">
            </el-pagination>
        </div>
        <!--<el-button type="text" @click="dialogVisible = true">打开嵌套表单的 Dialog</el-button>-->
        <el-dialog :title="'编辑 ' + edit_special_title + ' 专栏'" :visible.sync="dialogVisible">
            <div class="dialog-mid">
                <el-transfer
                    style="text-align: left; display: inline-block"
                    v-model="chosen"
                    filterable
                    :titles="['文章列表', '专栏文章']"
                    :format="{
                        noChecked: '${total}',
                        hasChecked: '${checked}/${total}'
                    }"
                    target-order="original"
                    :data="transfer_data">
                    <span slot-scope="{ option }">{{ option.title }}</span>
                </el-transfer>
            </div>
            <div slot="footer" class="dialog-footer">
                <el-button @click="dialogVisible = false">取 消</el-button>
                <el-button type="primary" @click="edit_submit">确 定</el-button>
            </div>
        </el-dialog>
        <el-dialog title="新建一个专栏" :visible.sync="add">
            <div class="dialog-mid" style="width:23em">
                <el-input v-model="add_form.title" maxlength="20" placeholder="请输入专栏名称"></el-input>
            </div>
            <div slot="footer" class="dialog-footer">
                <el-button @click="add = false">取 消</el-button>
                <el-button type="primary" @click="new_special">确 定</el-button>
            </div>
        </el-dialog>
        <el-progress :percentage="loading_percentage" class="loading_bar" :show-text="false"></el-progress>
    </div>
</template>

<script>
export default {
    data () {
        return {
            special_list:[],
            dialogVisible: false,
            formLabelWidth: '120px',
            edit_special_title:'',
            editing_sid:0,
            chosen:[1],
            transfer_data:[
                {key:1, title:'hi', disabled:false}
            ],
            current_page:1,
            total:0,
            page_size:15,
            flag:false,
            add:false,
            add_form:{
                title:''
            },
            loading_percentage:0,
            loading_count:0,
            loading:true
        }
    },
    mounted(){
        $(window).scroll(0);
        this.init();
    },
    methods:{
        init(){
            if(!this.login_manager.get()){
                this.$router.push({path:'/index'});
                return;
            }
            this.apply_for_info();
        },
        getCookie (name) {
            var value = '; ' + document.cookie
            var parts = value.split('; ' + name + '=')
            if (parts.length === 2) return parts.pop().split(';').shift()
        },
        edit(sid, title){
            this.init_edit_dialog(sid);
            var that = this;
            if(!that.flag){
                that.alert_msg.error('加载专栏信息失败，请重试');
                return;
            }
            that.chosen = [];
            that.flag = false;
            that.editing_sid = sid;
            $.ajax({ 
                type:'get', 
                url:"/create/special/info?sid="+sid,
                headers: {'X-CSRFToken': that.getCookie('csrftoken')}, 
                async:false,
                success:function (res){ 
                    for(var i=0; i<res.article_list.length; i++){
                        that.chosen.push(res.article_list[i].aid);
                    }
                    that.flag = true;
                },
                error:function(){
                    console.log('连接失败');
                }
            });
            if(!that.flag){
                that.alert_msg.error('加载专栏信息失败，请重试');
                return;
            }
            this.dialogVisible = true;
            this.edit_special_title = title;
        },
        apply_for_info(){
            var that = this;
            that.loading_percentage = 10;
            that.loading = true;
            that.special_list = [];
            $.ajax({ 
                type:'get', 
                url:"/create/special/list?page="+that.current_page+"&each="+that.page_size,
                headers: {'X-CSRFToken': this.getCookie('csrftoken')}, 
                processData: false,
                contentType: false,
                success:function (res){ 
                    that.special_list = res.list;
                    that.total = res.amount;
                    that.loading_percentage = 100;
                    setTimeout(function(){
                        $('.loading_bar').addClass('loading_bar_done');
                        setTimeout(function(){
                            that.loading_percentage = 0;
                            that.loading_count = 0;
                        }, 690);
                    }, 600);
                    that.loading = false;
                },
                error:function(){
                    console.log('连接失败');
                    that.loading_percentage = 100;
                    setTimeout(function(){
                        $('.loading_bar').addClass('loading_bar_done');
                        setTimeout(function(){
                            that.loading_percentage = 0;
                            that.loading_count = 0;
                        }, 690);
                    }, 600);
                    that.loading = false;
                }
            });
        },
        change_page(arg){
            this.current_page = arg;
            this.apply_for_info();
            document.documentElement.scrollTop = 0;
        },
        init_edit_dialog(sid){
            var that = this;
            that.transfer_data = [];
            that.flag = false;
            $.ajax({ 
                type:'get', 
                url:"/create/special/info_for_edit",
                headers: {'X-CSRFToken': that.getCookie('csrftoken')}, 
                async:false,
                success:function (res){ 
                    for(var i=0; i<res.article_list.length; i++){
                        that.transfer_data.push({key:res.article_list[i].aid, title:res.article_list[i].title, disabled:res.article_list[i].sid!=sid&&res.article_list[i].sid!=''})
                    }
                    that.flag = true;
                },
                error:function(){
                    console.log('连接失败');
                }
            });
        },
        edit_submit(){
            var that = this;
            $.ajax({ 
                type:'post', 
                url:"/create/special/edit",
                headers: {'X-CSRFToken': that.getCookie('csrftoken')}, 
                data: JSON.stringify({sid:that.editing_sid, article:that.chosen}),
                async:false,
                success:function (res){ 
                    if(res.status == 0){
                        that.alert_msg.success('修改专栏成功');
                        that.dialogVisible = false;
                        that.init();
                    }
                    else{
                        that.alert_msg.error('修改专栏失败，请重试');
                    }
                },
                error:function(){
                    that.alert_msg.error('连接失败');
                }
            });
        },
        click_add(){
            this.add_form.title = '';
            this.add = true;
        },
        new_special(){
            var that = this;
            if(that.add_form.title == ''){
                that.alert_msg.warning('专栏名称不得为空');
                return;
            }
            $.ajax({ 
                type:'post', 
                url:"/create/special/new",
                headers: {'X-CSRFToken': that.getCookie('csrftoken')}, 
                data: JSON.stringify(that.add_form),
                async:false,
                success:function (res){ 
                    if(res.status == 0){
                        that.alert_msg.success('新建专栏成功');
                        that.add = false;
                        that.init();
                    }
                    else{
                        switch(res.status){
                            case 1:
                                that.alert_msg.error('已经存在同名的专栏');
                                break;
                            case 2:
                                that.alert_msg.error('专栏名称不得超过 20 个字');
                                break;
                            default:
                                that.alert_msg.error('新建专栏失败，请重试');
                        }
                    }
                },
                error:function(){
                    that.alert_msg.error('连接失败');
                }
            });
        },
        delete_refresh(){
            if(this.current_page!=1 && this.list.length==1){
                this.current_page--;
            }
            this.apply_for_info();
            document.documentElement.scrollTop = 0;
        }
    }
}
</script>

<style scoped>
@import url("../assets/common.css");
    body{
        scroll-behavior:smooth
    }

  .pagination{
    margin-top:30px;
    text-align: center;
    font-weight: normal;
  }

  .dialog-mid{
      margin:0 auto;
      width:fit-content
  }

  .spmb>>>.el-dialog{
      width:720px;
  }

  .spmb>>>.el-checkbox-group::-webkit-scrollbar {
        width:6px;
        height:6px;
        padding-right:5px;
    }

    .spmb>>>.el-checkbox-group::-webkit-scrollbar-thumb{
        border-radius: 3px;
        background-color: #ccc;
    }

    .spmb>>>.el-checkbox-group::-webkit-scrollbar-corner{
        display: none;
    }

  /* .el-transfer>>>.el-button--primary.is-disabled, .el-transfer>>>.el-button--primary.is-disabled:active, .el-transfer>>>.el-button--primary.is-disabled:focus, .el-transfer>>>.el-button--primary.is-disabled:hover{
    background-color: hsl(1, 69%, 90%) !important;
    border-color: hsl(1, 69%, 90%) !important;
    color:#fff !important;
    }

    .el-dialog>>>.el-dialog__headerbtn:focus .el-dialog__close, .el-dialog>>>.el-dialog__headerbtn:hover .el-dialog__close{
        color:#ea8c8b !important;
    } */

    .margin0{
        margin:0 !important;
    }

    .mb0 .margin_bottom0{
        margin-bottom:0 !important;
    }
</style>

