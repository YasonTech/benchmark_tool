var count = 8000
var mem_readings = []
var func
function readMem(){
    // seconds = window.localStorage.getItem('seconds');
    // if (seconds)
    //     count = seconds;
    if (count >= 0){
        mem = window.performance.memory;
        heap_data = [mem.usedJSHeapSize,mem.totalJSHeapSize,mem.jsHeapSizeLimit];
        console.log("heap data=" + heap_data.join(','));
        count --;
    }

    else{
        clearInterval(func);
    }
}

func = setInterval(readMem, 1);