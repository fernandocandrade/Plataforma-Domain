
/**
 *
 * Este arquivo é responsavel por carregar os mapas
 * inicialmente o mapas serão arquivos dentro do mesmo diretório da aplicação
 * mas posteriormente os arquivos de mapas virão da api core
 */

const fs = require("fs");
const yaml = require('js-yaml');
const MapCore = require("plataforma-sdk/services/api-core/map")
const Env = require("../env/environment");
/**
 * @class Loader
 * @description Esta classe é responsavel por carregar os mapas
 * inicialmente o mapas serão arquivos dentro do mesmo diretório da aplicação
 * mas posteriormente os arquivos de mapas virão da api core
 */
class Loader {

    constructor(){
        this.env = new Env();
    }
    /**
    * @description No caso da POC estamos lendo o arquivo de maps do disco mesmo
    * mas depois iremos alterar este metodo para ler os mapas da API Core
    * @returns {Array<Object>} Lista de objetos json dos mapas
    */
    getMaps() {

        var promise = new Promise((resolve, reject) => {
            try {
                var maps = [];
                //mantem o suporte para mapas dentro de apps de dominio
                fs.readdirSync("./maps").forEach(file => {
                    if (file.endsWith(".yaml")) {
                        var _map = yaml.safeLoad(fs.readFileSync("./maps/" + file));
                        var obj = {};
                        obj.appName = file.replace(".yaml", "");
                        obj.map = _map;
                        maps.push(obj);
                    }
                });
                this.env.load().then((env)=>{
                    var core = new MapCore(env["core_services"]["api_core"]);
                    core.findBySystemId(env.solution.id).then(coreMaps =>{
                        coreMaps.forEach(m =>{
                            var obj = {};
                            obj.map = yaml.safeLoad(m.content);
                            obj.appName = m.name;
                            maps.push(obj);
                        });
                        resolve(maps);
                    });
                });
            } catch (e) {
                reject(e);
            }
        })
        return promise;
    }
}

module.exports = Loader;