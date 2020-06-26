<template>
    <div style="padding:10px 30px" class="vmb">
        <div>
            <h2>{{vip_title}}</h2>
            <div style="font-size:13px" v-if="!is_member">你还不是会员，快加入会员吧！</div>
            <div style="font-size:13px" v-if="is_member">你的会员将于 {{date}} 到期</div>
            <el-divider></el-divider>
        </div>
        <div style="width:fit-content;margin:100px auto">
            <div class="vip_div" @click="dialogVisible = true"></div>
        </div>
        <el-dialog title="" :visible.sync="dialogVisible" style="text-align:center;">
            <div class="dialog-mid">
                <!-- <h2>打钱</h2> -->
                <img src="../assets/vip_group.jpg" style="width:100%"/>
            </div>
        </el-dialog>
    </div>
</template>

<script>
export default {
    props: {
        current_page:{
            type:Number,
            default:1
        },
    },
    data () {
        return {
            vip_title:'加入会员',
            dialogVisible:false,
            is_member:false
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
        apply_for_info(){
            var that = this;
            $.ajax({ 
                type:'get', 
                url:"/member/apply",
                headers: {'X-CSRFToken': that.getCookie('csrftoken')}, 
                processData: false,
                contentType: false,
                success:function (res){ 
                    that.is_member = res.is_member;
                    that.date = res.date;
                    that.is_member ? that.vip_title='尊敬的会员，您好' : '';
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
@import "../assets/side_block.css";
    .el-divider{
        margin:1em 0;
    }

    .vip_div{
        width:350px;
        background-image: url('../assets/member.jpg');
        background-position: center;
        background-size: 350px;
        height:350px;
        margin:0 30px;
        cursor: pointer;
        float: left;
        border-radius: 10px;
        transition: 0.3s ease-in-out all;
        border:3px solid hsl(1, 69%, 78%);
        opacity: 0.9;
    }
    
    .vip_div:hover{
        opacity: 0.8;
        background-size: 400px;
    }

    .dialog-mid{
        margin-top:-30px
    }

    .vmb>>>.el-dialog{
        width:500px
    }
</style>

