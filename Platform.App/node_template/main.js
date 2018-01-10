/**
 * @description o main.js é o ponto de entrada para a aplicação de dominio
 * ele sobe o servidor http que irá servir a API
 */
const Environment = require('./env/environment');
var config = new Environment();
config.load().then((conf)=>{
    try{
        connect(1000,(retry,stop)=>{
            connectDatabase(conf,()=>{
                stop();
            },(e)=>{
                console.log(e.toString());
                retry();
            });
        },()=>{
            console.log("Connected");
        });        
    }catch(e){
        console.log("erro");
        console.log(e);
    }    
});
function connect(timeout,callback,done) {
    function next(){
        setTimeout(function(){
            typeof callback === "function" && callback(next,stop);
        },timeout);        
    }
    var stoped = false;
    function stop(status, error){        
        stoped = true;
        typeof done === "function" && done();
    }
    if(stoped) return;        
    typeof callback === "function" && callback(next,stop);
};


function connectDatabase(conf,callback,errorCallback){
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
                    startServer(conf.http.port); 
                    sequelize.close();
                    callback();
                });
            }).catch(e =>{
                sequelize.close();
                errorCallback(e);
            });
        }else{
            require("./model/domain.js").then(domain =>{          
                var MigrationManager = require("./utils/migrationManager");
                var mm = new MigrationManager(domain);
                mm.migrate().then(()=>{
                    startServer(conf.http.port); 
                    sequelize.close();
                    callback();
                }).catch(e =>{
                    sequelize.close();
                    errorCallback(e);
                });
            });
        }
    }).catch(e=>{
        sequelize.close();
        errorCallback(e);
    });
}

function startServer(port){
    require("./api/server").then(server => {
        server.listen(port, function() {
            console.log('%s listening at %s', server.name, server.url);
        });
    });    
}


 



