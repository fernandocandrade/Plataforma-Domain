/**
 * @class ArrayUtils
 * @description Esta classe é responsável por ter alguns métodos helpers para lidar com array
 */
class ArrayUtils{

    /**
     * 
     * @param {Array} arr lista de objetos
     * @param {Function} callback funcao chamada a cada iteração do array
     * Esta função irá receber como parâmetros <<item do array>>,<<função next>>,<<função stop>>
     * @param {Function} done funcao chamada após a ultima iteração do array
     * @description este método faz um forEach de forma assincrona para facilitar
     * a iteração em arrays cujo o processamento de cada item é obrigatoriamente assincrono
     */
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