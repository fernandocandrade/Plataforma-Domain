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
        var cnf = {};
        cnf.http = {};
        cnf.database = {};
        cnf.database.name = fileConfig.app.name;
        cnf.database.host = process.env.POSTGRES_HOST || "localhost";
        cnf.database.user = "postgres";
        cnf.database.password = "";
        cnf.http.port = 9090;
        var p1 = new Promise(function(resolve, reject) {
            resolve(cnf);
        });
        return p1;
    }    
 }

 module.exports = Environment;