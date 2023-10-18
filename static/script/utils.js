
// var vegastat = document.createElement("script");
// vegastat.type = 'text/javascript';
// vegastat.src = './script/vega.min.js';
// document.head.appendChild(vegastat);


async function loadScript(url) {
    let response = await fetch(url);
    let script = await response.text();
    eval(script);
}
  
// promise = loadScript('/script/vega.min.js');
// (async () => {
//     await promise
// })();

var STW = {}
STW.round = function(x, dp=0){
    let factor = 10**dp
    return Math.round(x*factor)/factor
}

function randomNumber(min, max) {
    return Math.random() * (max - min) + min;
}

function randomBar(inputdate, lastClose, mean, stdev, useCloseAsOpen = true) {
    // console.log(inputdate)
    if(useCloseAsOpen){
        var open = STW.round(lastClose, 5);
    }
    else {
        var open = lastClose * (1 + vega.sampleNormal(0, 0.0024));
        open = STW.round(open, 5);
    }

    var high = STW.round(open * (1+Math.abs(vega.sampleNormal(0, 0.0038))), 5)
    var low = STW.round(open * (1-Math.abs(vega.sampleNormal(0, 0.0038))), 5)
    var close = STW.round(randomNumber(high, low), 5)
    // var high = +randomNumber(Math.max(open, close), Math.max(open, close) * 1.1).toFixed(5);
    // var low = +randomNumber(Math.min(open, close) * 0.9, Math.min(open, close)).toFixed(5);
    return {
        'd': new Date(inputdate),
        'o': open,
        'h': high,
        'l': low,
        'c': close
    };
}
  
function randomData(dateStr, close, count) {
    var date = new Date(dateStr);
    var data = [randomBar(date, close)];
    while (data.length < count) {
        date.setDate(date.getDate() + 1)
        if (date.getDay() <= 5 && date.getDay() > 0) {
            let bar = randomBar(date, data[data.length - 1].c, 0, 0.0024);
            data.push(bar);
        }
    }
    return [data, new Date(date.setDate(date.getDate() + 1)), data[data.length - 1].c];
}

var count = 0
var testId
function repeatfunc(){
    console.log(testId)
    
    if (typeof testId == 'undefined'){
        console.log('intervalId not defined')
        return
    }
    else if (count > 10){
        console.log('stopinterval')
        clearInterval(testId)
    }
    else{
        count++
        console.log('count: ' + count)
    }
}

// testId = setInterval(repeatfunc,500);
// var testdate = new Date("2022-04-20T01:03:00")
// console.log(testdate.toISOString())
// generateTenNormal(10)
// randomBar("2022-04-20T01:03:00", 1.072, 0 , 0.0024, false)
// data = randomData("2022-04-20T01:03:00", 1.083, 10)
// console.log(data)

function startWebWorker() {
    if (typeof(Worker) !== "undefined") {
        if (typeof(window.my_worker) == "undefined") {
            window.my_worker = new Worker("/static/script/webworker.js");
            window.my_worker.onmessage = function(event) {
                console.log(event)
                console.log(event.data);
                addNewBar();
            };
        }
    } 
    else {
        console.log('Webworker not support')
    }
}

function stopWebWorker() {
    if (typeof(window.my_worker) != "undefined"){
        window.my_worker.terminate();
        window.my_worker = undefined;
    }
}

function addNewBar(){
    console.log('Add new data bar')
    console.log(window.my_table)
    bar = randomBar(STW.newDate, STW.lastClose, 0, 0.0024)
    window.my_table.addData([bar])
    STW.newDate.setDate(STW.newDate.getDate() + 1)
    STW.lastClose = bar.c
}

function loadChart(eleName, dataBars, instName){
    STW.my_table = anychart.data.table('date');
    var mapping, chart;
    bardata = dataBars
    STW.my_table.addData(bardata)
    // mapping the data 
    mapping = STW.my_table.mapAs({open: 'open', high: 'high', low: 'low', close: 'close'});
    STW.chart_selectable = mapping.createSelectable();
    // mapping.addField('open', 1, 'first');
    // mapping.addField('high', 2, 'max');
    // mapping.addField('low', 3, 'min');
    // mapping.addField('close', 4, 'last');
    // mapping.addField('value', 4, 'last');
    chart = anychart.stock();
    //chart.plot(0).yAxis(1).orientation("right");
    chart.plot(0).yAxis(0, {title: 'Y-Axis'});
    chart.plot(0).yAxis(1, {orientation: 'right', title: 'Y-Axis'});
    // chart.crosshair(true);
    chart.plot(0).priceIndicator({value:'last-visible'});
    // set the series type
    var candleSeries = chart.plot(0).candlestick(mapping).name('EURUSD');
    // chart.yAxis(1, {orientation: 'right', title: 'Y-Axis'});

    // lastPriceIndicator.series(candleSeries)
    // lastPriceIndicator.valueField('close')
    // setting the chart title
    chart.title('1M Data');
    // display the chart
    chart.container(eleName);
    chart.draw();
}

function updateChart(dataBars){
    STW.my_table.addData(dataBars)
}
// startWebWorker()
