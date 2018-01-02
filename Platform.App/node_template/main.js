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
      });      
    const database = conf.database.name;
    
    sequelize.query(`SELECT datname FROM pg_database where datname='${database}'`).then((c)=>{
        var exist = c[1].rowCount > 0;
        if(!exist){
            sequelize.query(`CREATE DATABASE "${database}";`).then(() => {
                startServer(); 
            }).catch(e => console.log(e));
        }else{
            startServer();
        }
    })
});

function startServer(){
    var server = require("./api/server");
    server.listen(9090, function() {
        console.log('%s listening at %s', server.name, server.url);
    });
}


 



