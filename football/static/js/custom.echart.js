$(function () {
    // var dom = document.getElementById("container");
    // var myChart = echarts.init(dom);

    var dom2 = document.getElementById("container2");
    var myChart2 = echarts.init(dom2);

    option_kelly = {
        tooltip: {
            trigger: 'axis',
            formatter: function (dd) {
                var arr = {};
                for (var i = 0; i < dd.length; i++) {
                    arr[dd[i].data + ""] = i;
                }

                function sortj(a, b) {
                    return a.data - b.data;
                }

                var result = dd.sort(sortj);
                var str = dd[0]['name'] + "<br/>";
                for (var j = result.length - 1; j >= 0; j--) {
                    str += result[j]['marker'] + result[j].data + '<br/>';
                }
                return str;
            }
        },
        legend: {
            data: ['胜', '负', '平']
        },
        grid: {
            left: '3%',
            right: '4%',
            bottom: '3%',
            containLabel: true
        },
        xAxis: {
            type: 'category',
            boundaryGap: false,
            data: insertDateTimes
        },
        yAxis: {
            type: 'value'
        },
        series: [
            {
                showSymbol: false,
                name: '胜',
                type: 'line',
                data: kellyWinNums
            },
            {
                showSymbol: false,
                name: '平',
                type: 'line',
                data: kellyAvgNums,
                itemStyle: {
                    normal: {
                        color: '#cebd4e',
                        lineStyle: {
                            color: '#cebd4e'
                        }
                    }
                }
            },
            {
                showSymbol: false,
                name: '负',
                type: 'line',
                data: kellyLostNums,
                itemStyle: {
                    normal: {
                        color: '#190e12',
                        lineStyle: {
                            color: '#190e12'
                        }
                    }
                }
            }
        ]
    };
    var dom_bifen = document.getElementById("container_bifen");
    var myChart_bifen = echarts.init(dom_bifen);
    option_bifen = {
        tooltip: {
            trigger: 'axis'
        },
        legend: {
            data: ['胜','平','负']
        },
        grid: {
            left: '3%',
            right: '4%',
            bottom: '3%',
            containLabel: true
        },
        xAxis: {
            type: 'category',
            boundaryGap: false,
            data: bodan_std[3]
        },
        yAxis: {
            type: 'value'
        },
        series: [
            {
                showSymbol: false,
                name: '胜',
                type: 'line',
                data: bodan_std[0],
                itemStyle: {
                    normal: {
                        color: '#FF4500',
                        lineStyle: {
                            color: '#FF4500'
                        }
                    }
                }
            },
            {
                showSymbol: false,
                name: '平',
                type: 'line',
                data: bodan_std[1],
                itemStyle: {
                    normal: {
                        color: '#cebd4e',
                        lineStyle: {
                            color: '#cebd4e'
                        }
                    }
                }
            },
            {
                showSymbol: false,
                name: '负',
                type: 'line',
                data: bodan_std[2],
                itemStyle: {
                    normal: {
                        color: '#190e12',
                        lineStyle: {
                            color: '#190e12'
                        }
                    }
                }
            }
        ]
    };

    if (option_kelly && typeof option_kelly === "object") {
        myChart2.setOption(option_kelly, true);
    }
    if (option_bifen && typeof option_bifen === "object") {
        myChart_bifen.setOption(option_bifen, true);
    }
});
