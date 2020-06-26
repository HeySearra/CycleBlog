<template>
    <div style="padding:10px 30px">
        <h2>定制页面</h2>
        <el-divider></el-divider>
        <el-form ref="form" :model="form" label-width="80px" style="margin-top:50px;padding:0 50px">
            <el-form-item label="开启">
                <el-switch
                    v-model="form.open">
                </el-switch>
            </el-form-item>
            <el-form-item label="HTML代码">
                <el-input
                    type="textarea"
                    :rows="5"
                    :autosize="{ minRows: 5, maxRows: 15}"
                    placeholder="请在此输入 HTML 代码"
                    v-model="form.html"
                    resize="none"
                    :disabled="!form.open">
                </el-input>
            </el-form-item>
            <el-form-item label="CSS代码">
                <el-input
                    type="textarea"
                    :rows="5"
                    :autosize="{ minRows: 5, maxRows: 15}"
                    placeholder="请在此输入 CSS 代码"
                    v-model="form.css"
                    resize="none"
                    :disabled="!form.open">
                </el-input>
            </el-form-item>
            <el-button type="primary" style="float:right">确认</el-button>
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
                open:false,
                html:'',
                css:''
            }
        }
    }
}
</script>

<style scoped>
  .el-divider{
      margin:0;
  }
</style>

