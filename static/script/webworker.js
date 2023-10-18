var i = 0;

function timedCount() {
    i = i + 1;
    if (i < 10){
        postMessage(i);
        setTimeout("timedCount()",1000);
    }
    else {
        console.log('Closing web worker');
        console.log(self)
        close();
    }
}

timedCount();