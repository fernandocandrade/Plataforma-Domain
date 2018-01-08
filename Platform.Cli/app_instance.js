/**
 * @class AppInstance
 * @description retorna as configurações de aplicação e de instancia do App
 */
module.exports = class AppInstance{
    getLockInstance(){
        var fs = require("fs");
        if (fs.existsSync("./plataforma.instance.lock")){
            return JSON.parse(fs.readFileSync("./plataforma.instance.lock","UTF-8"));
        }
        return {};
    }

    getAppConfig(){
        var fs = require("fs");
        if (fs.existsSync("./plataforma.json")){
            return JSON.parse(fs.readFileSync("./plataforma.json","UTF-8"));
        }
        return {};
    }
}