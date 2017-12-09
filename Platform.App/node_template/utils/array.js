class ArrayUtils{

    asyncEach(arr, callback,done) {
        var current = 0;        
        function next(){
            current++;
            if(current < arr.length){
               typeof callback === "function" && callback(arr[current],next,stop);
            }else{
               typeof done === "function" && done();
            }
        }
        var stoped = false;
        function stop(status, error){        
            stoped = true;
        }
        if(stoped) return;
        
        if(arr.length === 0) {
            typeof done === "function" && done();
            return;
        }
        
        typeof callback === "function" && callback(arr[current],next,stop);
    };

}

module.exports = ArrayUtils;