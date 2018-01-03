/**
 * @description o main.js é o ponto de entrada para a aplicação de dominio
 * ele sobe o servidor http que irá servir a API
 */
const Environment = require('./env/environment');
var config = new Environment();
config.load().then((conf)=>{
    const Sequelize = require('sequelize');
    const sequelize = new Sequelize('postgres', conf.database.user, conf.database.password, {
        dialect: 'postgres',
        host: conf.database.host,
        logging: false,
      });      
    const database = conf.database.name;
    
    sequelize.query(`SELECT datname FROM pg_database where datname='${database}'`).then((c)=>{
        var exist = c[1].rowCount > 0;
        if(!exist){
            sequelize.query(`CREATE DATABASE "${database}";`).then(() => {
                require("./model/domain.js").then(domain =>{
                    console.log("Synchronizing database")
                    domain["_engine"].sync();
                    startServer(); 
                    sequelize.close();
                });
            }).catch(e => console.log(e));
        }else{
            require("./model/domain.js").then(domain =>{          
                var MigrationManager = require("./utils/migrationManager");
                var mm = new MigrationManager(domain);
                mm.migrate().then(()=>{
                    startServer(); 
                    sequelize.close();
                })                
            });
        }
    })
});

function startServer(){
    require("./api/server").then(server => {
        server.listen(9090, function() {
            console.log('%s listening at %s', server.name, server.url);
        });
    });    
}


 



