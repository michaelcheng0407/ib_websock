//const socket = io();

async function loadScript(url) {
    let response = await fetch(url);
    let script = await response.text();
    eval(script);
}

function subscribe(){
    console.log('subscribe data')
    window.socketio.emit("Subscribe", {contract : "AUDUSD"})
}

function unsubscribe(){
    console.log('Unsubscribe data')
    window.socketio.emit("Unsubscribe", {contract : "AUDUSD"})
}

function connectChg(ele, event){
    console.log('connect change')
    console.log(ele.checked)
    if (ele.checked) {
        window.socketio.emit("connect_ib")
    }
    else {
        window.socketio.emit("disconnect_ib")
    }
}

//function to hide and display a div
function toggleDivWithId(Id){
    div = $("#"+Id)
    console.log("show trade called")
    if (div.css("display") !== "none") {
        div.css("display", "none");
    } 
    else {
        div.css("display", "block");
    }
}

/**
  * @param {String} url - address for the HTML to fetch
  * @return {String} the resulting HTML string fragment
  */
async function fetchHtmlAsText(url) {
    const response = await fetch(url);
    return response.text();
}

async function loadPageToDiv(Id, urlLink) {
    const contentDiv = document.getElementById(Id);
    contentDiv.innerHTML = await fetchHtmlAsText(urlLink);
}



$(document).ready(function() {
    console.log('Document is ready')
    orderloaded = loadPageToDiv('order', '/static/test.html');
    settingloaded = loadPageToDiv('setting', '/static/setting.html');
    controlloaded = loadPageToDiv('control', '/static/control.html');
    chartloaded = loadPageToDiv('chart', '/static/chart.html');
    settingloaded.then(() =>{
        console.log('setting load')
    });
    controlloaded.then(() =>{
        app = new Vue({
            el: '#price',
            data: {
              close: 'Hello Vue!'
            }
        })
    });

    chartloaded.then(() => {
        // loadchart();
        // loadchart1();
        // loadchart4();
    });
    loadScript('/static/script/websocketfunc.js')
});

