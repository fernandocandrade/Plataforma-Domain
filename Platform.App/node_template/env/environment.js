/**
 * @description esta classe cuida das configurações de acesso a banco da aplicação
 */

var fs = require("fs");

 class Environment {

    /**
     *
     * @return {Promise} retorna uma promessa com os dados de configuração d aplicação
     */
    load() {

        var fileConfig = JSON.parse(fs.readFileSync("plataforma.json"));
        fileConfig.http = {};
        fileConfig.database = {};
        fileConfig.database.name = fileConfig.app.name;
        fileConfig.database.host = process.env.POSTGRES_HOST || "postgres";
        fileConfig.database.user = process.env.POSTGRES_USER || "postgres";
        fileConfig.database.password = process.env.POSTGRES_PASSWROD || "";
        //cnf.http.port = 9090;
        var instanceConfig = JSON.parse(fs.readFileSync("plataforma.instance.lock"));
        if (process.env.PORT){
            fileConfig.http.port = process.env.PORT;
        }else{
            fileConfig.http.port = instanceConfig.port || 9090;
        }
        var p1 = new Promise(function(resolve, reject) {
            if (!fileConfig["core_services"]){
                fileConfig["core_services"] = {
                    api_core:{
                        scheme: process.env.COREAPI_SCHEME || "http",
                        host: process.env.COREAPI_HOST || "apicore",
                        port: process.env.COREAPI_PORT || "9110"
                    }
                };
            }
            resolve(fileConfig);
        });
        return p1;
    }
 }

 module.exports = Environment;