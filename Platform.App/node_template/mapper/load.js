
/**
 * 
 * Este arquivo é responsavel por carregar os mapas
 * inicialmente o mapas serão arquivos dentro do mesmo diretório da aplicação
 * mas posteriormente os arquivos de mapas virão da api core
 */

var fs = require("fs");
var yaml = require('js-yaml');

class Loader{

    //No caso da POC estamos lendo o arquivo de maps do disco mesmo
    //mas depois iremos alterar este metodo para ler os mapas da API Core
    getMaps() {
        var maps = [];
        fs.readdirSync("../maps").forEach(file => {
            if(file.endsWith(".yaml")){                
                var _map = yaml.safeLoad(fs.readFileSync("../maps/"+file));
                var obj = {};
                obj.appName = file.replace(".yaml","");
                obj.map = _map;
                maps.push(obj);
            }            
        }) 
        return maps;
    };
}

module.exports = Loader;