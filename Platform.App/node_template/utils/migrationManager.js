/**
 * @class MigrationManager
 * @description Esta classe faz o processo de migração das entidades de dominio
 * A unica operação permitida é adicionar colunas
 */
var ArrayUtils = require("./array");
class MigrationManager{

    seqTypeMap()  {
        var dataTypes = this.domain["_dataTypes"];
        return {
            "string":dataTypes.STRING,
            "integer":dataTypes.INTEGER,
            "char":dataTypes.CHAR,
            "text":dataTypes.TEXT,
            "bigint":dataTypes.BIGINT,
            "float":dataTypes.FLOAT,
            "real":dataTypes.REAL,
            "double":dataTypes.DOUBLE,
            "decimal":dataTypes.DECIMAL,
            "boolean":dataTypes.BOOLEAN,
            "time":dataTypes.TIME,
            "date":dataTypes.DATE,
            "hstore":dataTypes.HSTORE,
            "json":dataTypes.JSON,
            "jsonb":dataTypes.JSONB,
            "blob":dataTypes.BLOB,
            "uuid":dataTypes.UUID,
            "uuidV1":dataTypes.UUIDV1,
            "uuidV4":dataTypes.UUIDV4
        }
    };

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
    addColumn(table, columnName, colDef){
        var sql = this.domain["_engine"];
        var dataTypes = this.domain["_dataTypes"];
        colDef.type = this.seqTypeMap()[colDef.type];    
        return sql.queryInterface.addColumn(table,columnName,colDef);
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
            sql.queryInterface.removeColumn(table,columnName)
            .then(resolve).catch(reject);
        });
        return promise;
    }

    /**
     * 
     * @param {String} table nome da tabela de dominio
     * @param {String} columns array de colunas da tabela
     * @description cria uma tabela no banco de dados com as infromações da migration
     */
    createTable(table,columns){        
        var sql = this.domain["_engine"];
        Object.keys(columns).forEach(c => {
            columns[c].type = this.seqTypeMap()[columns[c].type];
        });
        var Sequelize = this.domain["_dataTypes"];
        //campos obrigatórios
        columns["rid"] = { type: Sequelize.UUID , primaryKey: true, defaultValue: Sequelize.UUIDV4   };
        columns["id"] = { type: Sequelize.UUID,  defaultValue: Sequelize.UUIDV4  };
        columns["instance_id"] = { type: Sequelize.UUID };
        columns["data_inicio_vigencia"] = { type: Sequelize.DATE, defaultValue: Sequelize.NOW };
        columns["data_fim_vigencia"] = { type: Sequelize.DATE };        
        return sql.queryInterface.createTable(table,columns);
    }

    dropTable(table){        
        var sql = this.domain["_engine"];
        return sql.queryInterface.dropTable(table);
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
                    list = list.sort();
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
            if (migration.command["add_column"]){
                this.executeAddColumnCommand(migration).then(resolve).catch(reject);
            }else if (migration.command["create_table"]){
                this.executeCreateTableCommand(migration).then(resolve).catch(reject);
            }
        });
        return promise;
    }

    /**
     * 
     * @param {Object} migration é o objeto de migração que será executado
     * @description Executa o comando de migração add_column
     * @return {Promise}
     */
    executeAddColumnCommand(migration){
        var promise = new Promise((resolve,reject)=>{                        
            var table = migration.command["add_column"].table;             
            var cols = Object.keys(migration.command["add_column"].columns);            
            this.arrayUtils.asyncEach(cols,(col,nextCol,stop)=>{
                this.addColumn(table,col,migration.command["add_column"].columns[col])
                .then(nextCol).catch(()=>{
                    this.dropColumn(table,col).then(stop).catch(stop);
                });
            },()=>{
                this.updateMigrationHistory(migration.name)
                .then(resolve)
                .catch(reject);
            });
        });
        return promise;
    }

    /**
     * 
     * @param {Object} migration é o objeto de migração que será executado
     * @description Executa o comando de migração add_column
     * @return {Promise}
     */
    executeCreateTableCommand(migration){
        var promise = new Promise((resolve,reject)=>{                        
            var table = migration.command["create_table"].name;
            this.createTable(table,migration.command["create_table"].columns)
            .then(()=>{
                this.updateMigrationHistory(migration.name)
                .then(resolve)
                .catch((e)=>{
                    console.log(e);
                    this.dropTable(table).then(nextCol).catch(nextCol);
                });
            }).catch(resolve);
            
        });
        return promise;
    }
 }

 module.exports = MigrationManager;