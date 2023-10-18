console.log('Websocker js loading')
socketio = io('ws://localhost:5000', {
    path: '/ws/socket.io'
});

socketio.on('connect', function(arg1) {
    socketio.emit('my event', {data: 'I\'m connected!'});
    console.log('On connect event:' + socketio.id)
    console.log('arg1: ' + arg1)
    //socket.emit('my event', 'Test');
});

socketio.on('update', function(bars_json){
    console.log('Update Recieve')
    bars = JSON.parse(bars_json)
    console.log("Update Data")
    console.log(bars_json)
    console.log(bars)
    last_bar = bars.at(-1).BarData
    //console.log('bars_json: ' + JSON.parse(bars_json).at(-1).BarData.date)
    console.log("last close:", last_bar.close)
    
    if (typeof app !== 'undefined') {
        app.close = last_bar.close
    }
});

socketio.on('message', function(arg1){
    console.log('message recieve:' + arg1)
});

socketio.on('init 1m bar', function(bars_json){
    console.log('init 1m bar')
    bars = JSON.parse(bars_json)
    console.log(bars_json)
    console.log(bars)
    loadChart('chart2', bars)
});

socketio.on('new 1m bar', function(bars_json){
    console.log('new 1m bar')
    bars = JSON.parse(bars_json)
    console.log(bars_json)
    console.log(bars.slice(-1))
    updateChart(bars.slice(-1))
});

socketio.on('1m bar changed', function(bars_json){
    console.log('1m bar changed')
    bars = JSON.parse(bars_json)
    console.log(bars_json)
    console.log(bars.slice(-1))
    updateChart(bars.slice(-1))
    //console.log(bars)
});

// socketio.onAny((event, ...args) => {
//     console.log(`Got uncaught websocket event: ${event}`);
// });

function loadDataToChart(data, chartEleId) {
    var mapping, chart, table;
    table = anychart.data.table('d');
    bardata = data
    console.log(bardata)
    table.addData(bardata)
    // mapping the data 
    mapping = table.mapAs({open: 'o', high: 'h', low: 'l', close: 'c'});
    chart = anychart.stock();
    chart.crosshair(true);
    // set the series type
    chart.plot(0).candlestick(mapping).name('ACME Corp.');
    
    // setting the chart title
    chart.title('AnyStock Basic Sample');
    // display the chart
    chart.container(chartEleId);
    chart.draw();
    //return a table for later update
    return table
}