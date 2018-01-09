const AppInstance = require("../../app_instance");
const uuidv4 = require('uuid/v4');
const BaseAction = require("../baseCreateAction");
var shell = require("shelljs");
var fs = require("fs");


module.exports = class CreateAppAction{
    constructor(){
        this.appInstance = new AppInstance();
        this.baseAction = new BaseAction();
    }

    create(type){        
        this.baseAction.create("process",(plataforma)=>{
            var path = process.cwd()+"/"+plataforma.app.name;
            shell.mkdir('-p', path+'/mapa',path+'/metadados',path+'/process');
            shell.touch(path+"/process/"+plataforma.app.name+".js");
            shell.touch(path+"/metadados/EventCatalog.js");
            shell.touch(path+"/metadados/"+plataforma.app.name+".yaml");
            
            const Dockerfile = `
FROM node:carbon
WORKDIR /usr/src/${plataforma.app.name}
COPY . .
CMD [ "node", "process/${plataforma.app.name}.js" ]
`
            fs.writeFileSync(path+"/Dockerfile",new Buffer(Dockerfile),"UTF-8")
            shell.touch(path+"/Dockerfile");
            
        }) 
    }     
}