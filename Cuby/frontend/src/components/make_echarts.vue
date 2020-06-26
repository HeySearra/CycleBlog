<template>
    <div class="echarts">
        <div id="main" :style="'height:800px;width:100%'"></div>
    </div>
</template>

<script>
import echarts from 'echarts'
export default {
  name: 'Echarts',
  props:{

  },
  data(){
      return {
          screenWidth: 0,
          view:[],
          like:[],
          comment:[]
      }
  },
  methods:{
	myEcharts(){
		var posList = [
            'left', 'right', 'top', 'bottom',
            'inside',
            'insideTop', 'insideLeft', 'insideRight', 'insideBottom',
            'insideTopLeft', 'insideTopRight', 'insideBottomLeft', 'insideBottomRight'
        ];

        var app = {};

        app.configParameters = {
            rotate: {
                min: -90,
                max: 90
            },
            align: {
                options: {
                    left: 'left',
                    center: 'center',
                    right: 'right'
                }
            },
            verticalAlign: {
                options: {
                    top: 'top',
                    middle: 'middle',
                    bottom: 'bottom'
                }
            },
            position: {
                options: this.$echarts.util.reduce(posList, function (map, pos) {
                    map[pos] = pos;
                    return map;
                }, {})
            },
            distance: {
                min: 0,
                max: 100
            }
        };

        app.config = {
            rotate: 90,
            align: 'left',
            verticalAlign: 'middle',
            position: 'insideBottom',
            distance: 15,
            onChange: function () {
                var labelOption = {
                    normal: {
                        rotate: app.config.rotate,
                        align: app.config.align,
                        verticalAlign: app.config.verticalAlign,
                        position: app.config.position,
                        distance: app.config.distance
                    }
                };
                myChart.setOption({
                    series: [{
                        label: labelOption
                    }, {
                        label: labelOption
                    }, {
                        label: labelOption
                    }, {
                        label: labelOption
                    }]
                });
            }
        };


        var labelOption = {
            show: true,
            position: app.config.position,
            distance: app.config.distance,
            align: app.config.align,
            verticalAlign: app.config.verticalAlign,
            rotate: app.config.rotate,
            formatter: '{c}  {name|{a}}',
            fontSize: 16,
            rich: {
                name: {
                    textBorderColor: '#fff'
                }
            }
        };

        var option = {
            color: ['hsl(1, 69%, 56%)', 'hsl(1, 69%, 69%)', 'hsl(1, 69%, 78%)'],
            tooltip: {
                trigger: 'axis',
                axisPointer: {
                    type: 'shadow'
                }
            },
            legend: {
                data: ['浏览', '点赞', '评论']
            },
            toolbox: {
                show: false,
                orient: 'vertical',
                left: 'right',
                top: 'center',
                feature: {
                    mark: {show: true},
                    dataView: {show: true, readOnly: false},
                    magicType: {show: true, type: ['line', 'bar', 'stack', 'tiled']},
                    restore: {show: true},
                    saveAsImage: {show: true}
                }
            },
            xAxis: [
                {
                    type: 'category',
                    axisTick: {show: false},
                    data: ['昨日新增', '总数']
                }
            ],
            yAxis: [
                {
                    type: 'value'
                }
            ],
            series: [
                {
                    name: '浏览',
                    type: 'bar',
                    barGap: 0,
                    label: labelOption,
                    data: this.view
                },
                {
                    name: '点赞',
                    type: 'bar',
                    label: labelOption,
                    data: this.like
                },
                {
                    name: '评论',
                    type: 'bar',
                    label: labelOption,
                    data: this.comment
                },
            ]
        }; 

        var myChart = this.$echarts.init(document.getElementById('main'));
        myChart.setOption(option);
    },
    apply_for_info(){
        var that = this;
        $.ajax({ 
            type:'get', 
            url:'/create/data/all',
            headers: {'X-CSRFToken': this.getCookie('csrftoken')}, 
            async:false,
            success:function (res){ 
                that.view = [res.views_inc, res.views];
                that.like = [res.likes_inc, res.likes];
                that.comment = [res.comments_inc, res.comments];
            },
            error:function(){
                that.alert_msg.error('连接失败');
            }
        });
    },
    getCookie (name) {
        var value = '; ' + document.cookie
        var parts = value.split('; ' + name + '=')
        if (parts.length === 2) return parts.pop().split(';').shift()
    }
  },
  mounted() {
    this.apply_for_info();
    this.myEcharts();
    var that = this;
    setInterval(function(){
        that.screenWidth = document.body.clientWidth;
    }, 50);
  },
  watch:{
    screenWidth(val){
        // console.log('hello')
        var myChart = this.$echarts.init(document.getElementById('main'));
        myChart.resize();
    }
}
}
</script>

<style scoped>
</style>