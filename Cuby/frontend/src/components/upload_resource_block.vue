<template>
    <div :style="type=='upload'?'padding:10px 30px':'padding:0 30px;margin-top:-30px'">
        <h2 v-if="type=='upload'">上传资源</h2>
        <h2 v-if="type=='edit'">编辑资源</h2>
        <el-divider></el-divider>
        <div style="height:30px;width:100%" v-if="type=='edit'"></div>
        <div :style="type=='upload'?'padding:30px 70px':'padding:0 30px 0 15px'">
            <el-form ref="form" :rules="rules" :model="form" label-width="80px" class="form">
                <el-form-item v-if="type=='upload'">
                    <el-upload
                        drag
                        action=""
                        :on-remove="handle_file_change"
                        :http-request="upload_file"
                        :multiple="false"
                        :limit="1"
                        :on-exceed="file_exceed">
                        <i class="el-icon-upload"></i>
                        <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
                        <div class="el-upload__tip" slot="tip">大小限制：{{limit}}</div>
                    </el-upload>
                </el-form-item>
                <el-form-item label="资源名称" prop="title" ref="form_title">
                    <el-input v-model="form.title" @keyup.enter.native="$refs.form_intro.focus()"></el-input>
                </el-form-item>
                <el-form-item label="资源介绍" class="intro">
                    <el-input
                        type="textarea"
                        :rows="2"
                        v-model="form.introduction"
                        :autosize="{ minRows:2, maxRows: 6}"
                        resize="none"
                        maxlength="250"
                        show-word-limit
                        ref="form_intro">
                    </el-input>
                </el-form-item>
                <el-form-item label="下载积分" required>
                    <el-select v-model="form.points" placeholder="请选择">
                        <el-option
                        v-for="item in options"
                        :key="item.value"
                        :label="item.label"
                        :value="item.value">
                        </el-option>
                    </el-select>
                </el-form-item>
                <el-form-item label="标签" class="tags">
                    <el-tag
                        :key="tag"
                        v-for="tag in form.tags"
                        closable
                        :disable-transitions="true"
                        @close="handleClose(tag)">
                        {{tag}}
                    </el-tag>
                    <el-input
                        class="input-new-tag"
                        v-if="inputVisible"
                        v-model="tag_input"
                        ref="saveTagInput"
                        size="small"
                        @keyup.enter.native="handleInputConfirm"
                        @blur="handleInputConfirm"
                        >
                    </el-input>
                    <el-button v-else class="button-new-tag" size="small" @click="showInput">+ 添加标签</el-button>
                </el-form-item>
                <el-form-item v-show="type=='upload'">
                    <el-button type="primary" @click="submitForm('form')" class="submit">上传</el-button>
                </el-form-item>
            </el-form>
        </div>
    </div>
</template>

<script>
export default {
    props: {
        type:{
            type:String,
            default:'upload'
        },
        rid:{
            type:String,
            default:'-1'
        }
    },
    data () {
        return {
            limit:'',
            limit_byte:0,
            form:{
                title:'',
                introduction:'',
                rid:0,
                points:0,
                tags:[],
                src:''
            },
            rules: {
                title: [
                    { required: true, message: '请输入资源名称', trigger: 'blur' },
                    { max: 20, message: '长度不能超过 20 个字符', trigger: 'blur' }
                ],
            },
            options: [{
                    value: 0,
                    label: '0'
                }, {
                    value: 5,
                    label: '5'
                }, {
                    value: 10,
                    label: '10'
                }, {
                    value: 20,
                    label: '20'
                }, {
                    value: 50,
                    label: '50'
                }, {
                    value: 100,
                    label: '100'
                }
            ],
            tag_input:'',
            inputVisible: false
        }
    },
    mounted(){
        $(window).scroll(0);
        this.init();
    },
    methods: {
        init(){
            if(!this.login_manager.get()){
                this.$router.push({path:'/index'});
                return;
            }
            if(this.type == 'edit'){
                this.apply_for_edit_info();
            }
            else{
                this.apply_for_info();
            }
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
                url:'/create/resource/upload_limit',
                headers: {'X-CSRFToken': this.getCookie('csrftoken')}, 
                processData: false,
                contentType: false,
                success:function (res){ 
                    that.limit = res.size;
                    that.limit_byte = res.byte;
                },
                error:function(){
                    that.alert_msg.error('信息加载失败');
                }
            });
        },

        apply_for_edit_info(){
            var that = this;
            if(that.rid == 0){
                return;
            }
            $.ajax({ 
                type:'get', 
                url:'/resource/all?rid='+that.rid,
                headers: {'X-CSRFToken': this.getCookie('csrftoken')}, 
                processData: false,
                contentType: false,
                success:function (res){ 
                    that.form.title = res.title;
                    that.form.introduction = res.description;
                    that.form.points = res.points;
                    that.form.tags = res.tags;
                    //that.$emit('open');
                },
                error:function(){
                    that.alert_msg.error('信息加载失败');
                    that.$emit('close');
                }
            });
        },

        handle_file_change(file){
            this.form.src = '';
        },

        file_exceed(){
            this.alert_msg.warning('一次只能上传一个文件');
        },

        upload_file(f){
            if(this.limit == ''){
                this.alert_msg.error('信息加载失败，请刷新页面');
                f.onError();
                return;
            }
            var that = this;
            if(f.file.size > that.limit_byte){
                this.alert_msg.error('上传资源超过大小限制');
                f.onError();
                return;
            }
            let form = new FormData();
            form.append('file', f.file);
            $.ajax({ 
                type:'post', 
                url:'/create/resource/upload_file',
                headers: {'X-CSRFToken': this.getCookie('csrftoken')}, 
                data:form,
                processData: false,
                contentType: false,
                success:function (res){ 
                    if(res.status == 0){
                        that.alert_msg.success('上传成功');
                        that.form.src = res.src;
                        f.onSuccess();
                    }
                    else{
                        switch(res){
                            case 1:
                                that.alert_msg.error('上传资源超过大小限制');
                                break;
                            default:
                                that.alert_msg.error('上传资源失败，请重试');
                        }
                        that.form.src = '';
                        f.onError();
                    }
                },
                error:function(){
                    that.alert_msg.error('连接失败');
                    that.form.src = '';
                    f.onError();
                }
            });
        },

        handleClose(tag) {
            this.form.tags.splice(this.form.tags.indexOf(tag), 1);
        },

        showInput() {
                if(this.form.tags.length >= 10){
                    this.$message.error('标签数量不能超过10个');
                    return;
                }
                this.inputVisible = true;
                this.$nextTick(_ => {
                this.$refs.saveTagInput.$refs.input.focus();
                });
        },

        handleInputConfirm() {
            let inputValue = this.tag_input;
            inputValue = inputValue.replace(/\s*/g,"");
            if (inputValue) {
                if(inputValue.length > 10){
                    this.inputVisible = false;
                    this.tag_input = '';
                    this.$message.error('标签不允许超过10个字');
                    return;
                }
                for(var i=0; i<this.form.tags.length; i++){
                    if(this.form.tags[i] == inputValue){
                        this.inputVisible = false;
                        this.tag_input = '';
                        this.$message.error('标签不允许重复');
                        return;
                    }
                }
                this.form.tags.push(inputValue);
            }
            this.inputVisible = false;
            this.tag_input = '';
        },

        submitForm(formName) {
            if(this.limit == ''){
                this.alert_msg.error('信息加载失败，请刷新页面');
                return;
            }
            var that = this;
            if(that.form.src==''){
                that.alert_msg.warning('请上传资源');
                return;
            }
            this.$refs[formName].validate((valid) => {
                if (valid) {
                    if(that.form.tags.length == 0){
                        that.alert_msg.warning('标签不能少于一个');
                        return;
                    }
                    $.ajax({ 
                        type:'post', 
                        url:'/create/resource/new',
                        headers: {'X-CSRFToken': this.getCookie('csrftoken')}, 
                        data: JSON.stringify(that.form),
                        processData: false,
                        contentType: false,
                        success:function (res){ 
                            if(res.status == 0){
                                that.alert_msg.success('上传成功');
                                that.$router.push({path:'/create/resource/upload_list'});
                            }
                            else{
                                switch(res){
                                    case 1:
                                        that.alert_box.msg('上传失败', '资源不能使用外部链接');
                                        break;
                                    case 2:
                                        that.alert_box.msg('上传失败', '资源标签不得为空');
                                        break;
                                    case 3:
                                        that.alert_box.msg('上传失败', '资源名称不得为空');
                                        break;
                                    case 4:
                                        that.alert_box.msg('上传失败', '资源名称不得过长');
                                        break;
                                    default:
                                        that.alert_box.msg('上传失败', '请检查你的内容，并重试');
                                }
                            }
                        },
                        error:function(){
                            that.alert_msg.error('连接失败');
                        }
                    });
                } 
                else {
                    return false;
                }
            });
        },
        submit_edit(){
            var that = this;
            this.$refs.form.validate((valid) => {
                if (valid) {
                    if(that.form.tags.length == 0){
                        that.alert_msg.warning('标签不能少于一个');
                        return;
                    }
                    var msg = that.form;
                    msg.rid = that.rid;
                    $.ajax({ 
                        type:'post', 
                        url:'/create/resource/new',
                        headers: {'X-CSRFToken': this.getCookie('csrftoken')}, 
                        data: JSON.stringify(msg),
                        processData: false,
                        contentType: false,
                        success:function (res){ 
                            if(res.status == 0){
                                that.alert_msg.success('编辑成功');
                                that.$emit('close');
                                that.$emit('edit_success');
                            }
                            else{
                                switch(res){
                                    case 1:
                                        that.alert_box.msg('上传失败', '资源不能使用外部链接');
                                        break;
                                    case 2:
                                        that.alert_box.msg('上传失败', '资源标签不得为空');
                                        break;
                                    case 3:
                                        that.alert_box.msg('上传失败', '资源名称不得为空');
                                        break;
                                    case 4:
                                        that.alert_box.msg('上传失败', '资源名称不得过长');
                                        break;
                                    default:
                                        that.alert_box.msg('上传失败', '请检查你的内容，并重试');
                                }
                            }
                        },
                        error:function(){
                            that.alert_msg.error('连接失败');
                        }
                    });
                } 
                else {
                    return false;
                }
            });
        }
    }
}
</script>

<style scoped>
    .intro>>>textarea::-webkit-scrollbar {
        width:6px;
        height:6px;
        padding-right:5px;
    }

    .intro>>>textarea::-webkit-scrollbar-thumb{
        border-radius: 3px;
        background-color: #ccc;
    }

    .intro>>>textarea::-webkit-scrollbar-corner{
        display: none;
    }

    .form>>>.el-input__inner, .form>>>.el-form-item__content{
        line-height: 21px;
    }

    .el-tag {
        margin-left: 10px;
    }

    .button-new-tag {
        margin-left: 10px;
        height: 32px;
        line-height: 30px;
        padding-top: 0;
        padding-bottom: 0;
    }

    .input-new-tag {
        width: 90px;
        margin-left: 10px;
        vertical-align: bottom;
    }

    .tags>>>.el-form-item__content{
        line-height: 40px;
    }

    .form>>>.el-upload{
        width:100%;
    }

    .form>>>.el-upload-dragger{
        width:auto;
    }

    .submit{
        display: inherit;
        margin: 20px auto;
        width:90%;
        letter-spacing:2em;
    }
</style>
