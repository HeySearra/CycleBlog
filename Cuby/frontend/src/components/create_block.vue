<template>
    <div class="create_block side_block" :class="is_login?'':'no_login'">
        <div class="to_login" v-if="!is_login" @click="$router.push({path:'/login', query:{from:$route.path}})">登录开启你的创作之旅</div>
        <div class="blur">
            <el-button type="primary" icon="el-icon-edit" @click="to_write" circle></el-button>
            <h4>写文章</h4>
        </div>
        <div class="blur">
            <el-button type="primary" icon="el-icon-upload2" @click="to_upload" circle></el-button>
            <h4>上传资源</h4>
        </div>
        <div class="blur">
            <el-button type="primary" icon="el-icon-magic-stick" @click="to_create" circle></el-button>
            <h4>创作中心</h4>
        </div>
    </div>
</template>

<script>
export default {
    props: {
        
    },
    data () {
        return {
            is_login:true
        }
    },
    mounted(){
        this.is_login = this.login_manager.get();
    },
    methods:{
        to_write(){
            this.$router.push({path:'/edit',query:{from:this.$route.path}});
        },
        to_upload(){
            this.$router.push({path:'/create/resource/upload'});
        },
        to_create(){
            this.$router.push({path:'/create/article'});
        }
    }
}
</script>

<style scoped>
@import "../assets/side_block.css";

.create_block{
    height: 85px;
}

.create_block>div{
    width:85px;
    text-align: center;
    float: left;
}

.no_login:hover .to_login{
    opacity: 1;
}

.to_login{
    position:absolute;
    background-color: rgba(0, 0, 0, 0.6);
    top:0;
    left:0;
    width:100% !important;
    height:100%;
    color:#fff;
    line-height: 125px;
    opacity: 0;
    cursor:pointer;
    transition:0.1s linear opacity;
}
</style>

