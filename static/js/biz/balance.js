
function splitData(rawData) {
    var categoryData = [];
    var values = [];
    var alertInfo = [];
	recs = rawData.split("\n")
    for (i=0; i<recs.length; i++) {
	    if (!recs[i] || recs[i].length==0) {
			continue;
		}
		items = recs[i].split("|");
        categoryData.push(items[0]);
        values.push(parseInt(items[1]));
        alertInfo.push(items.slice(2));
    }
    return {
        categoryData: categoryData,
        values: values,
        alertInfo: alertInfo
    };
}

function calculateMA(dayCount, data) {
    var result = [];
    for (var i = 0, len = data.values.length; i < len; i++) {
        if (i < dayCount) {
            result.push('-');
            continue;
        }
        var sum = 0;
        for (var j = 0; j < dayCount; j++) {
            sum += data.values[i - j][1];
        }
        result.push(+(sum / dayCount).toFixed(3));
    }
    return result;
}

$.get('static/data/balance.dat', function (rawData) {
	var myChart = echarts.init(document.getElementById('balance'));

    var data = splitData(rawData);

    myChart.setOption(option = {
        backgroundColor: '#eee',
        animation: false,
        legend: {
            bottom: 10,
            left: 'center',
            data: ['Balance']
        },
        grid: [
            {
                left: '10%',
                right: '8%',
                bottom: '55%'
            },
			{
                left: '10%',
                right: '8%',
                top: '55%'
            }

        ],
        xAxis: [
            {
                type: 'category',
                data: data.categoryData,
                scale: true,
                axisLine: {onZero: false},
                splitLine: {show: false},
                min: 'dataMin',
                max: 'dataMax',
                axisPointer: {
                    z: 100
                }
            }
        ],
        yAxis: [
            {
                scale: true,
                splitArea: {
                    show: true
                }
            },
            {
                scale: true,
                gridIndex: 1,
                splitArea: {
                    show: true
                }
            }
        ],
        series: [
            {
                name: 'Balance',
                type: 'bar',
                data: data.values
            },
			{
                name: 'Balance',
                type: 'bar',
                data: data.values,
				yAxisIndex: 1
            },

        ]
    }, true);
});
