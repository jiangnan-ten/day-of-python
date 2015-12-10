//中奖用户
require.config({
    paths: {
        echarts: 'http://tenjj.b0.upaiyun.com/echarts' 
    }
});

require(['echarts', 'echarts/chart/bar', 'echarts/chart/pie', 'echarts/chart/line'], function(ec) {
        $.ajax({
            url: 'http://139.129.92.21:8090/chart.php?parm=userrank',
            dataType: 'json',
            success: function(res) {
                if (res) {    
                    //用户top20 条形图设置
                    userrank_option = {
                        title : {
                            text: '幸运用户中奖次数Top20',
                            subtext: 'Tip:点击柱体显示奖品详情',
                            x: 'left'
                        },
                        tooltip: {
                            trigger: 'item'
                        },
                        xAxis : [
                            {
                                type : 'category',
                                axisLabel: {
                                    interval: 0,
                                },
                                data : function() {
                                    var xuser = [];
                                    for (var i in res.list) {
                                        xuser.push(i % 2 == 0 ? res['list'][i]['nickname'] : '\n'+res['list'][i]['nickname']);
                                    }
                                    return xuser;
                                }()
                            }
                        ],
                        yAxis : [
                            {
                                type : 'value'
                            }
                        ],
                        series : [
                            {
                                type: 'bar',
                                itemStyle: {
                                    normal: {
                                        label : {
                                            show: true, 
                                            position: 'inside',
                                        }
                                    }
                                },
                                data: function() {
                                    var ynum = [];
                                    for (var i in res.list) {
                                        ynum.push({
                                            value: res['list'][i]['total'],
                                            avatar_prefix: res['list'][i]['avatar_prefix']
                                        });
                                    }
                                    return ynum;
                                }()
                            },
                        ]
                    };

                    //用户奖品 饼图设置
                    userrank_pie_option = {
                        title : {
                            text: res.list[0]['nickname']+' 的奖品',
                            x: 'center'
                        },
                        tooltip: {
                            trigger: 'item',
                            formatter: "{a} <br/>{b} : {c} ({d}%)"
                        },
                        series : [
                            {
                                name:'奖品',
                                type:'pie',
                                radius : [30, 120],
                                center: ['50%', '50%'],
                                roseType : 'radius',
                                data: function() {
                                    luckyboy = [];
                                    for (var i in res.luckyboy) {
                                        luckyboy.push({
                                            name: res.luckyboy[i]['gname'],
                                            value: res.luckyboy[i]['total']
                                        });
                                    }
                                    return luckyboy
                                }()
                            }
                        ]
                    };

                    //用户中奖历史 折线图
                    userhistory_line_option = {
                        title : {
                            text: "'"+res.list[0]['nickname']+"'的中奖历史记录",
                            x: 'center'
                        },
                        tooltip : {
                            trigger: 'axis',
                            formatter: function(params) {
                                return '奖品: '+ params[0].data.gname+'<br>'+
                                        '昵称： '+params[0].data.nickname+'<br>'+
                                        '参与人次: '+params[0].data.value+'<br>'+
                                        '夺宝时间: '+params[0].data.duobao_time+'<br>'+
                                        '幸运号: '+params[0].data.luck_code
                            }
                        },
                        dataZoom : {
                            show : true,
                            realtime : true,
                        },
                        xAxis : [
                            {
                                type : 'category',
                                data : function (){
                                    var date_range = [];

                                    for (var i in res.userhistory) {
                                        date_range.push(res.userhistory[i].duobao_time.slice(0, 16));
                                    }

                                    return date_range;
                                }()
                            }
                        ],
                         yAxis : [
                            {
                                type : 'value',
                            }
                        ],
                         series : [
                            {
                                name:'参与人次',
                                type:'line',
                                data:function (){
                                    var cost = []

                                    for (var i in res.userhistory) {
                                        cost.push({
                                            value: res.userhistory[i].owner_cost,
                                            nickname: res.userhistory[i].nickname,
                                            gname: res.userhistory[i].gname,
                                            duobao_time: res.userhistory[i].duobao_time.slice(0, 16),
                                            luck_code: res.userhistory[i].luck_code
                                        })
                                    }

                                    return cost;
                                }(),
                                itemStyle: {
                                    normal: {
                                        color: '#061325',
                                        lineStyle: {
                                            color: '#87CEFA',
                                        },
                                        label : {
                                            show: true, 
                                            position: 'right',
                                            formatter: function(params) {
                                                return params.data.gname+'\n'+params.value+'人次'
                                            }
                                        },
                                    }
                                },
                            },
                        ]
                    };
                    

                    var userrank = ec.init($('#userrank')[0]); 
                    var userrank_pie = ec.init($('#userrank_pie')[0]);
                    var userhistory_line = ec.init($('#userhistory_line')[0]);
                    
                    /*某用户中奖详情*/
                    var ecConfig = require('echarts/config');
                    userrank.on(ecConfig.EVENT.CLICK, function (param){
                        var dataIndex = param.dataIndex;
                        username = param.name;
                        cid = res['list'][dataIndex]['cid'];
                        if (cid) {
                            //用户奖品 饼图
                            $.ajax({
                                url: 'http://139.129.92.21:8090/chart.php?parm=useraward&cid='+cid,
                                dataType: 'json',
                                async: false,
                                success: function(res) {
                                    if (res) {
                                        userrank_pie_data = [];
                                        for( var i in res ) {
                                            userrank_pie_data.push({
                                                name: res[i]['gname'],
                                                value: res[i]['total']
                                            });
                                        }
                                        userrank_pie_option.series[0].data = userrank_pie_data;
                                        userrank_pie_option.title.text = username;

                                        userrank_pie.setOption(userrank_pie_option, true);
                                    }
                                }
                            });
                            

                            //用户中奖历史 折线图
                            $.ajax({
                                url: 'http://139.129.92.21:8090/chart.php?parm=userhistory&cid='+cid,
                                dataType: 'json',
                                async: false,
                                success: function(res) {
                                    if (res) {
                                        var cost = [];

                                        for (var i in res) {
                                            cost.push({
                                                value: res[i].owner_cost,
                                                nickname: res[i].nickname,
                                                gname: res[i].gname,
                                                duobao_time: res[i].duobao_time.slice(0, 16),
                                                luck_code: res[i].luck_code
                                            })
                                        }

                                        userhistory_line_option.series[0].data = cost;
                                        userhistory_line_option.title.text = "'"+username+"'的中奖历史记录";
                                        userhistory_line_option.xAxis[0].data=function() {
                                            var date_range = [];
                                            for (var i in res) {
                                                date_range.push(res[i].duobao_time.slice(0, 16));
                                            }
                                            return date_range;
                                        }()

                                        userhistory_line.setOption(userhistory_line_option, true);
                                    }
                                }
                            });
                        }
                    });

                    userrank.setOption(userrank_option);
                    userrank_pie.setOption(userrank_pie_option);
                    userhistory_line.setOption(userhistory_line_option);
                }
            }
        });
});
