<template>
<div>
  <el-container>
    <el-header>
      <navbar></navbar>
    </el-header>
    <div class="title404">4 0 4</div>
    <div class="content404">似乎打开了不存在的页面</div>
    <el-footer></el-footer>
  </el-container>
</div>
</template>

<script scoped>
export default {}
</script>

<style>
@import url("../assets/common.css");
.title404, .content404{
  font-size: 150px;
  font-weight: bold;
  clear:both;
  width:100%;
  margin-top:20vh;
  text-align: center;
  color:#aaa
}

.content404{
  font-size: 50px;  
  margin-top:50px;
}
</style>