const BaseAction = require("../baseCreateAction");
var shell = require("shelljs");
module.exports = class CreatePresentationAppAction{
    constructor(){
        this.baseAction = new BaseAction();
    }

    create(type){
        this.baseAction.create("presentation",(plataforma)=>{
            var path = process.cwd()+"/"+plataforma.app.name;
            shell.mkdir('-p', path+'/server',path+`/${plataforma.app.name}`);
        });        
    }
}