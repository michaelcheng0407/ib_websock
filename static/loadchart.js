// var barCount = 2;
// var initialDateStr = '01 Apr 2017 00:00 Z';
// var barData = getRandomData(initialDateStr, barCount);
function loadchart4() {
    window.my_table;
    var mapping, chart;
    window.my_table = anychart.data.table('d');
    // jsonstr = "[\
    //     ['2015-12-24', 511.53, 514.98, 505.79, 506.40],\
    //     ['2015-12-25', 512.53, 514.88, 505.69, 507.34],\
    //     ['2015-12-26', 511.83, 514.98, 505.59, 506.23],\
    //     ['2015-12-27', 511.22, 515.30, 505.49, 506.47],\
    //     ['2015-12-28', 510.35, 515.72, 505.23, 505.80],\
    //     ['2015-12-29', 510.53, 515.86, 505.38, 508.25],\
    //     ['2015-12-30', 511.43, 515.98, 505.66, 507.45],\
    //     ['2015-12-31', 511.50, 515.33, 505.99, 507.98],\
    //     ['2016-01-01', 511.32, 514.29, 505.99, 506.37],\
    //     ['2016-01-02', 511.70, 514.87, 506.18, 506.75],\
    //     ['2016-01-03', 512.30, 514.78, 505.87, 508.67],\
    //     ['2016-01-04', 512.50, 514.77, 505.83, 508.35],\
    //     ['2016-01-05', 511.53, 516.18, 505.91, 509.42],\
    //     ['2016-01-06', 511.13, 516.01, 506.00, 509.26],\
    //     ['2016-01-07', 510.93, 516.07, 506.00, 510.99],\
    //     ['2016-01-08', 510.88, 515.93, 505.22, 509.95],\
    //     ['2016-01-09', 509.12, 515.97, 505.15, 510.12],\
    //     ['2016-01-10', 508.53, 516.13, 505.66, 510.42],\
    //     ['2016-01-11', 508.90, 516.24, 505.73, 510.40]]"

    // table.addData([
    //     ['2015-12-24', 511.53, 514.98, 505.79, 506.40],
    //     ['2015-12-25', 512.53, 514.88, 505.69, 507.34],
    //     ['2015-12-26', 511.83, 514.98, 505.59, 506.23],
    //     ['2015-12-27', 511.22, 515.30, 505.49, 506.47],
    //     ['2015-12-28', 510.35, 515.72, 505.23, 505.80],
    //     ['2015-12-29', 510.53, 515.86, 505.38, 508.25],
    //     ['2015-12-30', 511.43, 515.98, 505.66, 507.45],
    //     ['2015-12-31', 511.50, 515.33, 505.99, 507.98],
    //     ['2016-01-01', 511.32, 514.29, 505.99, 506.37],
    //     ['2016-01-02', 511.70, 514.87, 506.18, 506.75],
    //     ['2016-01-03', 512.30, 514.78, 505.87, 508.67],
    //     ['2016-01-04', 512.50, 514.77, 505.83, 508.35],
    //     ['2016-01-05', 511.53, 516.18, 505.91, 509.42],
    //     ['2016-01-06', 511.13, 516.01, 506.00, 509.26],
    //     ['2016-01-07', 510.93, 516.07, 506.00, 510.99],
    //     ['2016-01-08', 510.88, 515.93, 505.22, 509.95],
    //     ['2016-01-09', 509.12, 515.97, 505.15, 510.12],
    //     ['2016-01-10', 508.53, 516.13, 505.66, 510.42],
    //     ['2016-01-11', 508.90, 516.24, 505.73, 510.40]	
    // ]);
    combine_data = randomData("2022-04-20T01:03:00", 1.083, 60)
    console.log(combine_data);
    bardata = combine_data[0]
    STW.newDate = combine_data[1]
    STW.lastClose = combine_data[2]
    console.log(bardata)
    console.log('test')
    window.my_table.addData(bardata)
    // mapping the data 
    mapping = my_table.mapAs({open: 'o', high: 'h', low: 'l', close: 'c'});
    window.chart_selectable = mapping.createSelectable();
    // mapping.addField('open', 1, 'first');
    // mapping.addField('high', 2, 'max');
    // mapping.addField('low', 3, 'min');
    // mapping.addField('close', 4, 'last');
    // mapping.addField('value', 4, 'last');
    chart = anychart.stock();
    chart.crosshair(true);
    // set the series type
    chart.plot(0).candlestick(mapping).name('ACME Corp.');
    
    // setting the chart title
    chart.title('AnyStock Basic Sample');
    // display the chart
    chart.container('chart2');
    chart.draw();

}


// var getRandomInt = function(max) {
// 	return Math.floor(Math.random() * Math.floor(max));
// };

// function randomNumber(min, max) {
// 	return Math.random() * (max - min) + min;
// }

// function randomBar(date, lastClose) {
// 	var open = +randomNumber(lastClose * 0.95, lastClose * 1.05).toFixed(2);
// 	var close = +randomNumber(open * 0.95, open * 1.05).toFixed(2);
// 	var high = +randomNumber(Math.max(open, close), Math.max(open, close) * 1.1).toFixed(2);
// 	var low = +randomNumber(Math.min(open, close) * 0.9, Math.min(open, close)).toFixed(2);
// 	return {
// 		x: date.valueOf(),
// 		o: open,
// 		h: high,
// 		l: low,
// 		c: close
// 	};

// }

// function randomData(dateStr, count) {
// 	var date = luxon.DateTime.fromRFC2822(dateStr);
// 	var data = [randomBar(date, 30)];
// 	while (data.length < count) {
// 		date = date.plus({days: 1});
// 		if (date.weekday <= 5) {
// 			data.push(randomBar(date, data[data.length - 1].c));
// 		}
// 	}
// 	return data;
// }