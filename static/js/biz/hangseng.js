function formatTip(params, datas) {
	// prepare head
	let head=[];
	head.push('Key: ' + params[0].axisValue + '<hr size=1 style="margin: 3px 0">');

	// prepare body
	let body=[];
	body.push(params[0].seriesName + ': ' + params[0].data+ '<br/>');
	body.push(params[1].seriesName + ': ' + params[1].data+ '<br/>');

	dataIndex = params[0].dataIndex;
	// prepare WARN
	let warns = [];
	warns.push(params[2].seriesName + ': ' + params[2].data+ '<br/>');
	for(j=0; j<datas.ruleWarn[dataIndex].length; j++) {
		v=datas.ruleWarn[dataIndex][j];
		if (v && v.length>0) {
			warns.push('&emsp;' + (j+1) + '.&ensp;' + datas.ruleWarn[dataIndex][j] + '<br/>');
		}
	}
	// prepare EMERG
	let emergs = [];
	emergs.push('<font color="red"><b>');
	emergs.push(params[3].seriesName + ': ' + params[3].data+ '<br/>');
	for(k=0; k<datas.ruleEmerg[dataIndex].length; k++) {
		v=datas.ruleEmerg[dataIndex][k];
		if (v && v.length>0) {
			emergs.push('&emsp;' + (k+1) +'.&ensp;' + datas.ruleEmerg[dataIndex][k] + '<br/>');
		}
	}
	emergs.push('</b></font>');

	return head.concat(body).join('')+warns.join('')+emergs.join('');
}


$.get('getBalanceHsiYahoo', function (datas) {
	var myChart = echarts.init(document.getElementById('hangseng'));

    var colors = ['#5793f3', '#675bba', '#EB8E55', '#d14a61'];
    
    myChart.setOption(option = { 
        color: colors,
    
		tooltip: {
			trigger: 'axis',
			axisPointer: {
				type: 'cross'
			},
			backgroundColor: 'rgba(245, 245, 245, 0.8)',
            borderWidth: 1,
            borderColor: '#ccc',
            padding: 10,
            textStyle: {
                color: '#000'
            },
            position: function (pos, params, el, elRect, size) {
                var obj = {top: 10};
                obj[['left', 'right'][+(pos[0] < size.viewSize[0] / 2)]] = 30;
                return obj;
            },
            formatter: function (param) {
				console.log(param);
				return formatTip(param, datas);
			},
            extraCssText: 'width: 170px'
		},
        grid: {
            right: '20%'
        },
        toolbox: {
            feature: {
                dataView: {show: true, readOnly: false},
                restore: {show: true},
                saveAsImage: {show: true}
            }
        },
        legend: {
            data:['蒸发量','降水量', 'WARN', 'EMERG']
        },
        xAxis: [
            {
                type: 'category',
                axisTick: {
                    alignWithLabel: true
                },
                data: datas.dates
            }
        ],
        yAxis: [
            {
                type: 'value',
                name: '蒸发量',
                min: 'dataMin',
                max: 'dataMax',
                position: 'right',
                axisLine: {
                    lineStyle: {
                        color: colors[0]
                    }
                },
                axisLabel: {
                    formatter: '{value} ml'
                }
            },
            {
                type: 'value',
                name: '降水量',
                min: 'dataMin',
                max: 'dataMax',
                position: 'right',
                offset: 80,
                axisLine: {
                    lineStyle: {
                        color: colors[1]
                    }
                },
                axisLabel: {
                    formatter: '{value} ml'
                }
            },
			{
                type: 'value',
                name: 'WARN',
                min: 0,
                max: 20,
                position: 'left',
                axisLine: {
                    lineStyle: {
                        color: colors[2]
                    }
                },
                axisLabel: {
                    formatter: '{value}'
                }
            },
			{
                type: 'value',
                name: 'EMERG',
                min: 0,
                max: 20,
                position: 'left',
                offset: 60,
                axisLine: {
                    lineStyle: {
                        color: colors[3]
                    }
                },
                axisLabel: {
                    formatter: '{value}'
                }
            },
        ],
        series: [
            {
                name:'蒸发量',
                type:'bar',
                data:datas.balances
            },
            {
                name:'降水量',
                type:'bar',
                yAxisIndex: 1,
                data:datas.hongsengIndex
            },
            {
                name:'WARN',
                type:'line',
                yAxisIndex: 2,
                data:datas.ruleWarnCount
            },
            {
                name:'EMERG',
                type:'line',
                yAxisIndex: 3,
                data:datas.ruleEmergCount
            },
        ]
    });
});
