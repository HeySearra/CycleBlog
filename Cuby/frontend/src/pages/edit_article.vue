<template>
<div>
  <el-container>
    <el-header>
      <navbar></navbar>
    </el-header>
    <el-container class="mid">
      <el-container>
        <el-main>
            <el-page-header @back="back" title="返回" style="line-height:50px">
            </el-page-header>
            <div>
                <div style="float:left;width:calc(100% - 100px)"><el-input v-model="form.title" placeholder="请输入标题"></el-input></div>
                <div><el-button type="primary" style="margin-left:10px" @click="submitForm(form)">发布</el-button></div>
            </div>
            <div class="tags">
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
                    @blur="handleInputConfirm">
                </el-input>
                <el-button v-else class="button-new-tag" size="small" @click="showInput">+ 添加标签</el-button>
            </div>
            <mavon-editor 
              v-model="form.content" 
              ref="md" 
              @imgAdd="imgAdd"
              :style="full?'z-index:3000':''"
              ></mavon-editor>
        </el-main>
      </el-container>
    </el-container>
  </el-container>
</div>
</template>

<script scoped>
export default {
  data () {
    return {
      form:{
          content:'',
          tags:[],
          title:''
      },
      tag_input:'',
      inputVisible: false,
      aid:0,
      init_flag:false,
      full:false
    }
  },
  mounted(){
    this.init();
    document.documentElement.scrollTop = 0;
    $(window).off('scroll');
  },
  methods: {
        init(){
          if(!this.login_manager.get()){
            this.$router.push({path:'/index'});
            return;
          }
          this.aid = this.$route.params ? this.$route.params.id : undefined;
          if(!this.aid){
            this.aid = 0;
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
              url:"/article/all?aid="+that.aid,
              headers: {'X-CSRFToken': this.getCookie('csrftoken')}, 
              processData: false,
              contentType: false,
              success:function (res){ 
                  that.form.title = res.title;
                  that.form.tags = res.tags;
                  that.form.content = res.content;
              },
              error:function(){
                  that.alert_msg.error('连接失败');
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
          var that = this;
          if(that.form.title == ''){
            that.alert_msg.warning('你的文章还没有标题呢');
            return;
          }
          if(that.form.title.length > 50){
            that.alert_msg.warning('标题最多只能有 50 个字');
            return;
          }
          if(that.form.content == ''){
            that.alert_msg.warning('你的文章还没有内容呢');
            return;
          }
          if(that.form.tags.length == 0){
            that.alert_msg.warning('文章至少要有一个标签');
            return;
          }
          var msg = that.form;
          msg.aid = that.aid;
          $.ajax({ 
              type:'post', 
              url:"/edit/submit",
              headers: {'X-CSRFToken': that.getCookie('csrftoken')}, 
              data: JSON.stringify(msg),
              async:false,
              success:function (res){ 
                if(res.status == 0){
                  function _ok(that){
                    that.$router.push({path:'/create/article'});
                  }
                  that.alert_box.msg('提示', '文章发布成功！', _ok(that));
                }
                else{
                  that.alert_box.msg('提示', '文章发布失败，请检查你的文章内容');
                }
              },
              error:function(){
                  that.alert_msg.error('连接失败');
              }
          }); 
        },

        back(){
          var from = this.$route.query.from;
          console.log(from);
          if(from){
            this.$router.push({path:from});
          }
          else{
            this.$router.push({path:'/index'});
          }
        },

        imgAdd(pos, file){
          var that = this;
          var form = new FormData();
          form.append('image', file);
          $.ajax({ 
              type:'post', 
              url:"/edit/image",
              headers: {'X-CSRFToken': that.getCookie('csrftoken')}, 
              data: form,
              processData: false,
              contentType: false,
              success:function (res){ 
                if(res.status == 0){
                  that.$refs.md.$img2Url(pos, res.url);
                }
                else{
                  that.alert_msg.error('图片上传失败');
                }
              },
              error:function(){
                  that.alert_msg.error('连接失败');
              }
          }); 
        },
    }
}
</script>


<style scoped>
@import url("../assets/common.css");

  .mid {
    margin:50px auto !important;
    width:87%;
  }

  @media(max-width:1500px){
    .mid {
      width:96%;
    }
  }
  
  .el-container:nth-child(5) .el-aside,
  .el-container:nth-child(6) .el-aside {
    line-height: 260px;
  }
  
  .el-container:nth-child(7) .el-aside {
    line-height: 320px;
  }

  .v-note-wrapper.shadow{
      height: 1000px;
  }

  .el-main{
      padding-top:30px !important;
      background-color: rgba(0, 0, 0, 0);
      box-shadow: none;
      margin-top:0 !important;
  }

  .el-tag {
        margin: 0 6px;
    }

    .input-new-tag {
        width: 90px;
        margin-left: 10px;
        vertical-align: bottom;
    }

    .tags{
        height:50px;
        line-height: 50px;
    }

    .mid>>>.v-note-wrapper .v-note-panel .v-note-show .v-show-content, .v-note-wrapper .v-note-panel .v-note-show .v-show-content-html{
      background-color: #fff !important;
    }

    .mid>>>.v-show-content-html{
      background-color: rgba(0, 0, 0, 0) !important;
    }

    .mid>>>.v-note-wrapper .v-note-panel .v-note-navigation-wrapper .v-note-navigation-content h1, .mid>>>.v-note-wrapper .v-note-panel .v-note-navigation-wrapper .v-note-navigation-content h2, .mid>>>.v-note-wrapper .v-note-panel .v-note-navigation-wrapper .v-note-navigation-content h3, .mid>>>.v-note-wrapper .v-note-panel .v-note-navigation-wrapper .v-note-navigation-content h4, .mid>>>.v-note-wrapper .v-note-panel .v-note-navigation-wrapper .v-note-navigation-content h5, .mid>>>.v-note-wrapper .v-note-panel .v-note-navigation-wrapper .v-note-navigation-content h6{
          color: #EA8C8B
    }

    .mid>>>.fullscreen{
      z-index: 3000;
    }

    .mid>>>.markdown-body{
      overflow: hidden;
    }

    .mid>>>.v-show-content p{
      line-height: 30px;
      margin-bottom:18px
    }

    .art_mid>>>.markdown-body .hljs{
    overflow: unset !important;
}

    .mid>>>.markdown-body pre::-webkit-scrollbar, .mid>>>table::-webkit-scrollbar {
        width:6px;
        height:6px;
        padding-right:5px;
    }

    .mid>>>.markdown-body pre::-webkit-scrollbar-thumb, .mid>>>table::-webkit-scrollbar{
        border-radius: 3px;
        background-color: #ccc;
    }

    .mid>>>.markdown-body pre::-webkit-scrollbar-corner, .mid>>>table::-webkit-scrollbar-corner::-webkit-scrollbar{
        display: none;
    }

    .mid>>>table{
      overflow-y: hidden;
    }

    .mid>>>pre code{
        font-size: 100%;
        line-height:21px;
    }
</style>