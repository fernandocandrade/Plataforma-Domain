const AppInstance = require("../../app_instance");
const uuidv4 = require('uuid/v4');
const BaseAction = require("../baseCreateAction");
var shell = require('shelljs');
module.exports = class CreateAppAction{
    constructor(){
        this.appInstance = new AppInstance();
        this.baseAction = new BaseAction();
    }

    create(type){        
        this.baseAction.create("process",(plataforma)=>{
            var path = process.cwd()+"/"+plataforma.app.name;
            shell.mkdir('-p', path+'/mapa',path+'/metadados',path+'/process');
        }) 
    }     
}