const BaseAction = require("../baseCreateAction");
var shell = require("shelljs");
var fs = require("fs");
const TecnologyApp = require("../tecnologyApp");
module.exports = class CreatePresentationAppAction{
    constructor(){
        this.baseAction = new BaseAction();
    }

    create(type){
        this.baseAction.create("presentation", TecnologyApp.node, (plataforma)=>{
            var path = process.cwd()+"/"+plataforma.app.name;
            shell.mkdir('-p', path+'/server',path+`/${plataforma.app.name}`,path+"/metadados",path+"/mapa");
            const Dockerfile = `
            FROM node:carbon
            WORKDIR /usr/src/${plataforma.app.name}
            COPY . .
            CMD [ "node", "server/${plataforma.app.name}.js" ]
            `
            fs.writeFileSync(path+"/Dockerfile",new Buffer(Dockerfile),"UTF-8")
        });
    }
}