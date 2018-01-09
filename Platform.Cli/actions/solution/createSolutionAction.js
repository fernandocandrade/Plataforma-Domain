module.exports = class CreateSolutionAction{
    constructor(){}

    create(){
        var shell = require('shelljs');
        const uuidv4 = require('uuid/v4');
        var inquirer = require('inquirer');
        var fs = require("fs");        
        var plataforma = {};
        plataforma.solution = {};
        inquirer.prompt(this.getQuestions()).then(answers => {
            var name = answers["nome"];
            var path = process.cwd()+"/"+name;
            plataforma.solution.name = name;            
            plataforma.solution.description = answers["descricao"];
            plataforma.solution.version = answers["versao"];
            this.saveAppPlatform(plataforma,(id)=>{
                shell.mkdir('-p', path);
                plataforma.solution.id = id;
                fs.writeFileSync(path+"/plataforma.json",JSON.stringify(plataforma, null, 4),"UTF-8");
            });            
        });
    }

    getQuestions(){
        var questions = [];

        var q0 = {
            type: "input",
            default: "Solution1",
            name: "nome",
            message: "Nome da Solução"
        };

        var q1 = {
            type: "input",
            default: "0.0.1",
            name: "versao",
            message: "Versão"
        };

        var q2 = {
            type: "input",
            name: "descricao",
            message: "Descrição"
        };                    
        questions.push(q0,q2);
        return questions;
    }
    

    saveAppPlatform(platform, callback){
        //TODO Migrar esse código para uma LIB Do Core
        var unirest = require("unirest");
        var req = unirest("POST", "http://localhost:9095/core/persist");
        req.headers({
            "content-type": "application/json",
            "instance-id": "fe93a9a8-84d9-41ec-a056-e4606a72fbdd"
        });
        req.type("json");
        var clone = JSON.parse(JSON.stringify(platform.solution));
        clone._metadata = {};
        clone._metadata.type= "system";
        clone._metadata.changeTrack = "create";

        req.send([clone]);
        req.end(function (res) {
            if  (res.error){
                throw new Error(res.error);
            }
            callback(res.body[0].id);
        });
    }
};