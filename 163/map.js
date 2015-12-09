/*全国数据分布*/
$.ajax({
    url: 'http://ten.com/163/chart.php?parm=map',
    dataType: 'json', 
    success: function(res) {
        if(res) {
            map_city = [];
            max_city = [];
            for( var i in res.list ) {
                map_city.push({name: res.list[i][1], value: res.list[i][0]})
            }

            for( var i in res.max ) {
                max_city.push({name: res.max[i]['gname'], value: res.max[i]['total']})
            }

            var map = echarts.init($('#map')[0]); 
            map_option = {
                title : {
                    text: '全国中奖数据分布',
                    x:'center'
                },
                tooltip : {
                    trigger: 'item'
                },
                dataRange: {
                    splitList: [
                        {start:2000, end: res.max},
                        {start:1000, end: 2000},
                        {start:800, end: 1000},
                        {start:500, end: 800},
                        {start:200, end: 500},
                        {start:100, end: 200},
                        {start:10, end: 100},
                        {start:0, end: 10},
                        {end: 0}
                    ],
                    color: ['#E0022B', '#E09107', '#A3E00B']
                },
                series : [
                    {
                        name: '中奖总数',
                        type: 'map',
                        mapType: 'china',
                        selectedMode : 'single',
                        itemStyle:{
                            normal:{
                                label:{
                                    show:true,
                                    textStyle: {
                                       color: "rgb(249, 249, 249)"
                                    }
                                }
                            },
                            emphasis:{label:{show:true}}
                        },
                        mapLocation: {
                            x: 50,
                            width: '50%'
                        },
                        data: map_city
                    },
                    {
                        name: '各地区中奖详情',
                        type: 'pie',
                        roseType : 'area',
                        tooltip: {
                            trigger: 'item',
                            formatter: "{a} <br/>{b} : {c} ({d}%)"
                        },
                        center: [document.getElementById('map').offsetWidth-400, 225],
                        radius: [30, 120],
                        data:max_city
                    }
                ],
            };
            
            /*各省中奖详情 start*/
            map.on(echarts.config.EVENT.MAP_SELECTED, function (param){
                var selected = param.selected;
                var selectedProvince;
                var name;
                var mappie_data = [];

                for (var i = 0, l = map_option.series[0].data.length; i < l; i++) {
                    name = map_option.series[0].data[i].name;
                    map_option.series[0].data[i].selected = selected[name];
                    if (selected[name]) {
                        selectedProvince = name;
                    }
                }

                if (selectedProvince) {
                    $.ajax({
                        dataType:'json',
                        url: 'http://ten.com/163/chart.php?parm=mappie&province='+selectedProvince,
                        success: function(res) {
                            if (res) {
                                for (var i in res) {
                                    mappie_data.push({
                                        name: res[i]['gname'],
                                        value: res[i]['total']
                                    })
                                }
                            }
                        },
                        async: false,
                    });
                    map_option.series[1].data = mappie_data;
                }

                map.setOption(map_option, true);
            }); 
            /*各省中奖详情 end*/

            map.setOption(map_option);
        }
    }
});