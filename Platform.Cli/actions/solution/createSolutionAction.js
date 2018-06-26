const uuidv4 = require('uuid/v4');
const Deployer = require('../../services/deployer');
var RemoteContext = require("../../remote/remoteContext");
module.exports = class CreateSolutionAction{

    constructor(){
        this.remoteContext = new RemoteContext();
        this.deployer = new Deployer(this.remoteContext);
    }

    create(){
        var shell = require('shelljs');
        var inquirer = require('inquirer');
        var fs = require("fs");
        var plataforma = {};
        plataforma.solution = {};
        inquirer.prompt(this.getQuestions()).then(answers => {
            var name = answers["nome"].toLowerCase();
            var path = process.cwd()+"/"+name;
            plataforma.solution.name = name;
            plataforma.solution.description = answers["descricao"];
            plataforma.solution.version = answers["versao"];
            plataforma.solution.id = uuidv4();
            shell.mkdir('-p', path);
            fs.writeFileSync(path+"/plataforma.json",JSON.stringify(plataforma, null, 4),"UTF-8");
        });
    }

    getQuestions(){
        var questions = [];

        var q0 = {
            type: "input",
            default: "solution1",
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
};