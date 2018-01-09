
const AppInstance = require("../app_instance");
const uuidv4 = require('uuid/v4');
var shell = require('shelljs');        
var inquirer = require('inquirer');
var fs = require("fs");
module.exports = class BaseCreateAction{
    constructor(){
        this.appInstance = new AppInstance();
    }
    /**
     * 
     * @param {String} type É o tipo da app que esta sendo criada
     * @param {Function} callback Funcao chamada ao final da configuração da aplicação
     */
    create(type, callback){       
        var solution = this.appInstance.getSolutionConfig(".");
        var plataforma = {};
        plataforma.app = {};
        plataforma.app.type = type;
        inquirer.prompt(this.getQuestions()).then(answers => {
            var name = answers["nome"];
            var path = process.cwd()+"/"+name;
            plataforma.app.name = name;            
            plataforma.app.version = answers["versao"];
            plataforma.app.description = answers["descricao"];
            plataforma.app.author = answers["autor"];
            plataforma.solution = solution.solution;            
            this.installAppApiCore(plataforma,(id)=>{
                shell.mkdir('-p', path);
                plataforma.app.id = id;                
                fs.writeFileSync(path+"/plataforma.json",JSON.stringify(plataforma, null, 4),"UTF-8");
                callback(plataforma);
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
             name: "versao",
             message: "Versão da Aplicação"
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

     installAppApiCore(platform,callback){
        callback(uuidv4())
     }
}