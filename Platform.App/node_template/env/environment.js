/**
 * @description esta classe cuida das configurações de acesso a banco da aplicação
 */

 class Environment {

    /**
     * 
     * @return {Promise} retorna uma promessa com os dados de configuração d aplicação
     * @param {*} fallback 
     */
    load() {
        var cnf = {};
        cnf.database = {};
        cnf.database.name = "app";
        cnf.database.host = "localhost";
        cnf.database.user = "postgres";
        cnf.database.password = "";
        var p1 = new Promise(function(resolve, reject) {
            resolve(cnf);
        });
        return p1;
    }    
 }

 module.exports = Environment;