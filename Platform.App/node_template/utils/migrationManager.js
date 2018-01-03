/**
 * @class MigrationManager
 * @description Esta classe faz o processo de migração das entidades de dominio
 * A unica operação permitida é adicionar colunas
 */
var ArrayUtils = require("./array");
class MigrationManager{

    constructor(domain){
        this.arrayUtils = new ArrayUtils();
        this.domain = domain;
    }

    /**
     * 
     * @param {String} table nome da tabela de dominio
     * @param {String} columnName nome da nova colune
     * @param {String} type tipo de dados da coluna
     */
    add_column(table, columnName, type){
        var promise = new Promise((resolve,reject)=>{
            var sql = this.domain["_engine"];
            var dataTypes = this.domain["_dataTypes"];
            sql.queryInterface.addColumn(table,columnName,{ type: dataTypes.STRING })
            .then(resolve).catch(reject);
        });
        return promise;
    }
    /**
     * 
     * @param {String} table nome da tabela
     * @param {String} column nome da coluna
     * @description Em caso de falha ao escrever na tabela migration_history a aplicação faz o rollback
     * da migração
     */
    dropColumn(table,column){
        var promise = new Promise((resolve,reject)=>{
            var sql = this.domain["_engine"];
            var dataTypes = this.domain["_dataTypes"];
            sql.queryInterface.removeColumn(table,columnName)
            .then(resolve).catch(reject);
        });
        return promise;
    }

    /**
     * 
     * @param {String} name nome da migração
     * @description salva o registro de execução de migration na tabela
     * migration_history
     */
    updateMigrationHistory(name){
        return this.domain["migration_history"].create({name:name});
    }

    /**
     * @method migrate
     * @description Inicia o processo de migração
     * @returns {Promise} retorna uma Promise para o final do processo de migração
     */
    migrate(){
        console.log("Starting migrating process");        
        var promise = new Promise((resolve,reject)=>{
            this.getMigrations().then((migrations)=>{
                console.log(`There is ${migrations.length} migrations to be execute`);
                this.arrayUtils.asyncEach(migrations,(migration,next)=>{
                    console.log(`Executing migration ${migration.name}`);
                    this.execute(migration).then(next);
                },resolve);
            });
        });
        return promise;
    }

    /**
     * @method getMigrations
     * @description retorna todas as migrações que ainda não foram executadas
     */
    getMigrations(){
        var promise = new Promise((resolve,reject)=>{
            this.loadMigrationApp().then((migrationsFile)=>{                
                this.loadMigrationHistory().then(migrationsHistory =>{
                    this.getNotExecutedMigrations(migrationsFile,migrationsHistory)
                    .then(resolve);
                })
            })
        });
        return promise;
    }
    /**
     * @method loadMigrationApp
     * @description Carrega os arquivos de migration da aplicação e retorna
     */
    loadMigrationApp(){
        var promise = new Promise((resolve,reject)=>{
            var fs = require("fs");
            var yaml = require("js-yaml");
            fs.readdir("./migrations", (err, items) => {
                var list = [];
                this.arrayUtils.asyncEach(items,(item,next)=>{
                    fs.readFile("./migrations/"+item,"UTF-8",(err,data)=>{
                        var migrationObject = {};
                        migrationObject.command = yaml.safeLoad(data);
                        migrationObject.name = item.split(".")[0];
                        list.push(migrationObject);
                        next();
                    });
                },()=>{
                    resolve(list);
                })
            });
        });
        return promise;
    }

    /**
     * @description Carrega todas as migrações que foram executadas na aplicação
     * @returns {Promise}
     */
    loadMigrationHistory(){
        var promise = new Promise((resolve,reject)=>{
            this.domain["migration_history"].findAll().then(history => {
                resolve(history);
            });
        });
        return promise;
    }

    /**
     * 
     * @param {Array} loadedMigrations arquivo de migrações da aplicação
     * @param {Array} migrationsHistory registro de migrações executadas no banco
     * @description faz um diff para saber quais migrações precisam ser executadas no banco de dados
     */
    getNotExecutedMigrations(loadedMigrations, migrationsHistory){        
        var promise = new Promise((resolve,reject)=>{
            var toExecute = [];
            loadedMigrations.forEach(migration => {
                if (migrationsHistory.filter(h => h.name === migration.name).length === 0){
                    toExecute.push(migration);
                }
            });            
            resolve(toExecute);
        });
        return promise;
    }


    /**
     * 
     * @param {Object} migration é o objeto de migração que será executado
     * @return {Promise}
     */
    execute(migration){
        var promise = new Promise((resolve,reject)=>{            
            var table = migration.command["add_column"].table;             
            var cols = Object.keys(migration.command["add_column"].columns);
            this.arrayUtils.asyncEach(cols,(col,nextCol)=>{
                this.add_column(table,col,migration.command["add_column"].columns[col])
                .then(()=>{
                    this.updateMigrationHistory(migration.name)
                    .then(nextCol)
                    .catch((e)=>{
                        console.log(e);
                        this.dropColumn(table,col).then(nextCol).catch(nextCol);
                    });
                });
            },resolve);
        });
        return promise;
    }
 }

 module.exports = MigrationManager;