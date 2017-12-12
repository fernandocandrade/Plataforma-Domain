var fs = require('fs');
var yaml = require('js-yaml');
module.exports = (function(){
    var self = {};
    /**
     * 
     * @param {String} path path de origem da aplicação de Dominio do Usuario
     * @description Recupera o nome dos arquivos de dominio do usuario
     * @returns {Array<String>} Array com o nome dos arquivos que definem o dominio
     */
    self.getFileNames = function(path){
        self.root = path;
        var filesToLoad = [];
        fs.readdirSync(path+"Dominio").forEach(file => {
            if(file.endsWith(".yaml")){
                filesToLoad.push(file);
            }            
        }) 
        return filesToLoad;
    }

    self.readFile = function(fileName){
        return yaml.safeLoad(fs.readFileSync(self.root+"Dominio/" +fileName));
    };
    return self;
})();