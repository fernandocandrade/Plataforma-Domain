
const AppInstance = require("../../app_instance");
const uuidv4 = require('uuid/v4');
module.exports = class CreateDomainAppAction{
    

    constructor(){
        this.appInstance = new AppInstance();
    }

    /** 
     * @method create
     * @description Monta a estrutura básica de uma aplicação de dominio
     * */ 
    create(type){
        var shell = require('shelljs');
        
        var inquirer = require('inquirer');
        var fs = require("fs");
        var solution = this.appInstance.getSolutionConfig(".");
        var plataforma = {};
        plataforma.app = {};
        plataforma.app.type = "domain";
        inquirer.prompt(this.getQuestions()).then(answers => {
            var name = answers["nome"];
            var path = process.cwd()+"/"+name;
            plataforma.app.name = name;
            
            plataforma.app.version = answers["versao_plataforma"];
            plataforma.app.description = answers["descricao"];
            plataforma.app.author = answers["autor"];
            plataforma.solution = solution.solution;

            this.saveApiCore(plataforma,(id)=>{
                plataforma.app.id = id;
                shell.mkdir('-p', path+'/Dominio',path+'/Migrations',path+'/Mapas');
                fs.writeFileSync(path+"/plataforma.json",JSON.stringify(plataforma, null, 4),"UTF-8");
            })
        });
    }

    getQuestions(){
        var questions = [];

        var q0 = {
            type: "input",
            default: "Domain.App",
            name: "nome",
            message: "Nome da Aplicação"
       };

        var q1 = {
             type: "input",
             name: "versao_plataforma",
             message: "Versão da Plataforma"
        };

        var q2 = {
            type: "input",
            name: "descricao",
            message: "Descrição"
        };

        var q3 = {
            type: "input",
            name: "autor",
            message: "Autor"
        };
         
        questions.push(q0,q1,q2,q3);
        return questions;
     }

     saveApiCore(platform,callback){
        //TODO migrar para uma lib do Api Core
        var unirest = require("unirest");
        var req = unirest("POST", "http://localhost:9095/core/persist");
        req.headers({
            "content-type": "application/json",
            "instance-id": "fe93a9a8-84d9-41ec-a056-e4606a72fbdd"
        });
        req.type("json");
        var clone = JSON.parse(JSON.stringify(platform.app));
        clone.systemId = platform.solution.id;
        clone._metadata = {};
        clone._metadata.type= "installedApps";
        clone._metadata.changeTrack = "create";

        req.send([clone]);
        req.end(function (res) {
            //caso nao esteja rodando a API Core
            //entao executa "local"
            if  (res.error){
                callback(uuidv4())
            }else{
                callback(res.body[0].id);
            }            
        });
     }
}