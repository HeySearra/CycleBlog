<template>
    <div style="padding:10px 30px" class="mb">
        <h2>个人信息</h2>
        <el-divider></el-divider>
        <el-form ref="form" :model="form" label-width="80px" style="margin-top:50px;padding:0 100px">
            <el-form-item label="头像">
                <el-upload
                    class="avatar-uploader"
                    action=""
                    :http-request="upload_por"
                    :show-file-list="false">
                    <img v-if="form.src" :src="form.src" class="avatar">
                    <i v-else class="el-icon-plus avatar-uploader-icon"></i>
                </el-upload>
            </el-form-item>
            <el-form-item label="昵称" required maxLength="20">
                <el-input v-model="form.name"></el-input>
            </el-form-item>
            <el-form-item label="生日">
                <el-date-picker
                    v-model="form.birthday"
                    type="date"
                    placeholder="选择日期"
                    :picker-options="pickerOptions">
                </el-date-picker>
            </el-form-item>
            <el-form-item label="性别">
                <el-radio v-model="form.sex" :label="1">男</el-radio>
                <el-radio v-model="form.sex" :label="2">女</el-radio>
                <el-radio v-model="form.sex" :label="0">保密</el-radio>
            </el-form-item>
            <el-form-item label="学校">
                <el-input v-model="form.school" maxLength="20"></el-input>
            </el-form-item>
            <el-form-item label="公司">
                <el-input v-model="form.company" maxLength="20"></el-input>
            </el-form-item>
            <el-form-item label="职业">
                <el-input v-model="form.job" maxLength="20"></el-input>
            </el-form-item>
            <el-form-item label="简介">
                <el-input
                    type="textarea"
                    :autosize="{ minRows: 2, maxRows: 10}"
                    placeholder="请输入内容"
                    v-model="form.introduction"
                    resize="none"
                    maxlength="100"
                    show-word-limit>
                </el-input>
            </el-form-item>
            <el-button type="primary" style="float:right" @click="submit">确认</el-button>
        </el-form>
    </div>
</template>

<script>
export default {
    props: {

    },
    data () {
        return {
            form:{
                name:'',
                birthday:'',
                sex:-1,
                school:'',
                company:'',
                job:'',
                introduction:'',
                src:''
            },
            imageUrl: '',
            pickerOptions: {
                disabledDate(time) {
                    return time.getTime() > Date.now();
                }
            }
        }
    },
    mounted(){
        $(window).scroll(0);
        this.init();
    },
    methods:{
        init(){
            this.apply_for_info();
        },
        getCookie (name) {
            var value = '; ' + document.cookie
            var parts = value.split('; ' + name + '=')
            if (parts.length === 2) return parts.pop().split(';').shift()
        },
        apply_for_info(){
            var that = this;
            $.ajax({ 
                type:'get', 
                url:"/user/info",
                headers: {'X-CSRFToken': this.getCookie('csrftoken')}, 
                processData: false,
                contentType: false,
                success:function (res){ 
                    that.form.name = res.name;
                    that.form.birthday = res.birthday;
                    that.form.sex = res.sex;
                    that.form.school = res.school;
                    that.form.company = res.company;
                    //that.form.organization = res.organization;
                    that.form.job = res.job;
                    that.form.introduction = res.introduction;
                },
                error:function(){
                    console.log('连接失败');
                }
            });
            $.ajax({ 
                type:'get', 
                url:'/simple_user_info',
                headers: {'X-CSRFToken': this.getCookie('csrftoken')}, 
                processData: false,
                contentType: false,
                success:function (res){ 
                    that.form.src = res.portrait;
                },
                error:function(){
                    console.log('连接失败');
                }
            });
        },
        submit(){
            var that = this;
            if(that.form.name == ''){
                that.alert_msg.warning('昵称不得为空');
                return;
            }
            if(that.form.job == '鸽子'){
                setTimeout(function(){
                    that.alert_msg.normal('快看，这里有一只职业鸽子！');
                }, 0);
            }
            $.ajax({ 
                type:'post', 
                url:"/user/info",
                headers: {'X-CSRFToken': this.getCookie('csrftoken')}, 
                data: JSON.stringify(that.form),
                async:false,
                success:function (res){ 
                    if(res.status == 0){
                        that.alert_msg.success('修改信息成功！');
                    }
                    else{
                        switch(res.status){
                            case 1:
                                that.alert_msg.error('昵称只能包含中英文、数字和下划线');
                                break;
                            default:
                                that.alert_msg.error('修改信息失败，请检查你的信息');
                        }
                    }
                },
                error:function(){
                    console.log('连接失败');
                }
            });
        },
        upload_por(f){
            const isJPG = f.file.type === 'image/jpeg';
            if (!isJPG) {
                this.alert_msg.error('上传头像图片只能是 JPG 格式');
                return;
            }
            var that = this;
            let form = new FormData();
            form.append('profile', f.file);
            $.ajax({ 
                type:'post', 
                url:'/user/change_profile',
                headers: {'X-CSRFToken': this.getCookie('csrftoken')}, 
                data:form,
                processData: false,
                contentType: false,
                success:function (res){ 
                    if(res.status == 0){
                        //that.alert_msg.success('上传成功');
                        that.form.src = res.src;
                        f.onSuccess();
                    }
                    else{
                        switch(res){
                            case 1:
                                that.alert_msg.error('错误，图片过大');
                                break;
                            default:
                                that.alert_msg.error('上传头像失败，请重试');
                        }
                        //that.form.src = '';
                        f.onError();
                    }
                },
                error:function(){
                    that.alert_msg.error('连接失败');
                    //that.form.src = '';
                    f.onError();
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
  .avatar-uploader .el-upload {
    border: 1px dashed #d9d9d9;
    border-radius: 6px;
    cursor: pointer;
    position: relative;
    overflow: hidden;
  }
  .avatar-uploader .el-upload:hover {
    border-color: #409EFF;
  }
  .avatar-uploader-icon {
    font-size: 28px;
    color: #8c939d;
    width: 178px;
    height: 178px;
    line-height: 178px;
    text-align: center;
  }
  .avatar {
    width: 178px;
    height: 178px;
    display: block;
  }

  .mb>>>.el-input__count{
    line-height: 20px;
  }

   .mb>>>textarea::-webkit-scrollbar {
        width:6px;
        height:6px;
        padding-right:5px;
    }

    .mb>>>textarea::-webkit-scrollbar-thumb{
        border-radius: 3px;
        background-color: #ccc;
    }

    .mb>>>textarea::-webkit-scrollbar-corner{
        display: none;
    }
</style>

