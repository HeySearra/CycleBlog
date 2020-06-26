<template>
    <div style="padding:10px 30px">
        <h2>个人信息</h2>
        <el-divider></el-divider>
        <el-tabs v-model="activeName" style="margin-top:30px;padding:0 50px">
            <el-tab-pane label="账号更换" name="account">
                <el-form ref="form_account" :model="form_account" label-width="80px" :rules="account_rules">
                    <el-form-item label="新账号" prop="account" required="required">
                        <el-input v-model="form_account.account" placeholder="请输入新的手机号或邮箱"></el-input>
                    </el-form-item>
                    <el-form-item label="密码验证" prop="password">
                        <el-input type="password" v-model="form_account.password" placeholder="请输入密码验证你的身份" show-password></el-input>
                    </el-form-item>
                    <el-button type="primary" style="float:right" @click="change_account">确认</el-button>
                </el-form>
            </el-tab-pane>
            <el-tab-pane label="密码设置" name="password">
                <el-form ref="form_pas" :model="form_pas" label-width="8em" :rules="pas_rules">
                    <el-form-item label="旧密码" prop="old">
                        <el-input type="password" v-model="form_pas.old" placeholder="请输入你的旧密码"></el-input>
                    </el-form-item>
                    <el-form-item label="新密码" prop="new">
                        <el-input type="password" v-model="form_pas.new" placeholder="请输入你的新密码" show-password></el-input>
                    </el-form-item>
                    <el-form-item label="重复新密码" prop="new2">
                        <el-input type="password" v-model="form_pas.new2" placeholder="请再次输入你的新密码" show-password></el-input>
                    </el-form-item>
                    <el-button type="primary" style="float:right" @click="change_password">确认</el-button>
                </el-form>
            </el-tab-pane>
        </el-tabs>
    </div>
</template>

<script>
export default {
    props: {

    },
    data () {
        return {
            form_account:{
                account:'',
                password:''
            },
            form_pas:{
                old:'',
                new:'',
                new2:''
            },
            activeName: 'account',
            account_rules:{
                password:[
                    {required:true,message:'请输入密码',trigger:'blur'},
                ],
                account:[                
                    { validator: this.check_account, trigger: 'blur'}
                ]
            },
            pas_rules:{
                old:[
                    {required:true,message:'请输入旧密码',trigger:'blur'},
                ],
                new:[
                    {required:true,message:'请输入新密码',trigger:'blur'},
                    {min:6,max:16,message:'长度在 6 到 16 个字符',trigger:'blur'}
                ],
                new2:[
                    {required:true,message:'请再次输入新密码',trigger:'blur'},
                    {validator: this.check_pas2, trigger: 'blur'}
                ],
            }
        }
    },
    mounted(){
        $(window).scroll(0);
    },
    methods:{
        init(){
            this.form_account.new_account = '';
            this.form_account.password = '';
            this.form_pas.old = '';
            this.form_pas.new = '';
            this.form_pas.new2 = '';
        },
        getCookie (name) {
            var value = '; ' + document.cookie
            var parts = value.split('; ' + name + '=')
            if (parts.length === 2) return parts.pop().split(';').shift()
        },
        check_account(rule, value, callback){
            const mailReg = /^([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+\.([a-zA-Z0-9_-])+/;
            const phoneReg = /^1[3|4|5|7|8][0-9]{9}$/;
            if (!value) {
                return callback(new Error('请输入手机号或邮箱'))
            }
            setTimeout(() => {
                if (mailReg.test(value)) {
                    callback();
                } 
                else if(phoneReg.test(value)){
                    callback();
                }
                else{
                    callback(new Error('请输入正确的手机号或邮箱'));
                }
            }, 30)
        },
        check_pas2(rule, value, callback){
            if (!value) {
                return callback(new Error('请再次输入新密码'))
            }
            var that = this;
            setTimeout(() => {
                if (value != that.form_pas.new) {
                    callback(new Error('两次密码输入不一致'));
                } 
                else{
                    callback();
                }
            }, 30)
        },
        change_account(){
            var that = this;
            this.$refs['form_account'].validate((valid) => {
                if (valid) {
                    $.ajax({ 
                        type:'post', 
                        url:"/user/change_account",
                        headers: {'X-CSRFToken': that.getCookie('csrftoken')}, 
                        data: JSON.stringify({old_password:that.form_pas.old, new_password:that.form_pas.new}),
                        async:false,
                        success:function (res){ 
                            function _ok(that){
                                that.init();
                            }
                            if(res.status == 0){
                                that.alert_box.msg('提示', '成功修改账号', _ok(that));
                            }
                            else{
                                switch(res.status){
                                    case 1:
                                        that.alert_box.msg('修改失败', '密码验证错误');
                                        break;
                                    case 2:
                                        that.alert_box.msg('修改失败', '该邮箱或手机号有非法字符');
                                        break;
                                    case 3:
                                        that.alert_box.msg('修改失败', '该邮箱或手机号已被注册');
                                        break;
                                    default:
                                        that.alert_msg.error('修改账号失败，请检查你的填写内容');
                                }
                            }
                        },
                        error:function(){
                            that.alert_msg.error('连接失败');
                        }
                    });
                } 
            });
        },
        change_password(){
            var that = this;
            this.$refs['form_pas'].validate((valid) => {
                if (valid) {
                    $.ajax({ 
                        type:'post', 
                        url:"/user/change_password",
                        headers: {'X-CSRFToken': that.getCookie('csrftoken')}, 
                        data: JSON.stringify({old_password:that.form_pas.old, new_password:that.form_pas.new}),
                        async:false,
                        success:function (res){ 
                            function _ok(that){
                                that.init();
                            }
                            if(res.status == 0){
                                that.alert_box.msg('提示', '成功修改密码！', _ok(that));
                            }
                            else{
                                switch(res.status){
                                    case 1:
                                        that.alert_box.msg('修改失败', '旧密码错误');
                                        break;
                                    case 2:
                                        that.alert_box.msg('修改失败', '两次密码输入不一致');
                                        break;
                                    case 3:
                                        that.alert_box.msg('修改失败', '密码不合法');
                                        break;
                                    default:
                                        that.alert_msg.error('修改密码失败，请检查你的填写内容');
                                }
                            }
                        },
                        error:function(){
                            that.alert_msg.error('连接失败');
                        }
                    });
                } 
            });
        }
    }
}
</script>

<style scoped>
  .el-divider{
      margin:0;
  }
  
  .el-form{
      margin-top:50px;
      padding: 0 150px
  }

  .el-form-item{
      margin-bottom:30px;
  }
</style>

