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
        fileConfig.database.host = process.env.POSTGRES_HOST || "localhost";
        fileConfig.database.user = "postgres";
        fileConfig.database.password = "";
        //cnf.http.port = 9090;
        var instanceConfig = JSON.parse(fs.readFileSync("plataforma.instance.lock"));
        fileConfig.http.port = instanceConfig.port || 9090;
        var p1 = new Promise(function(resolve, reject) {
            if (!fileConfig["core_services"]){
                fileConfig["core_services"] = {
                    api_core:{
                        scheme:"http",
                        host:"localhost",
                        port:"9100"
                    }
                };
            }
            resolve(fileConfig);
        });
        return p1;
    }
 }

 module.exports = Environment;