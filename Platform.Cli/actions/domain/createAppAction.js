const BaseAction = require("../baseCreateAction");
var shell = require('shelljs');
module.exports = class CreateDomainAppAction {
    constructor(){
        this.baseAction = new BaseAction();
    }

    /** 
     * @method create
     * @description Monta a estrutura básica de uma aplicação de dominio
     * */ 
    create(type){
        this.baseAction.create("domain",(plataforma)=>{
            var path = process.cwd()+"/"+plataforma.app.name;
            shell.mkdir('-p', path+'/Dominio',path+'/Migrations',path+'/Mapas');
        });        
    }
}