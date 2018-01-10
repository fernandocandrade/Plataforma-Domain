const shell = require("shelljs");
const os = require("os");
const AppInstance = require("../app_instance");
const uuidv4 = require('uuid/v4');
const inquirer = require('inquirer');
const fs = require("fs");
module.exports = class InstallPlatformAction{

    exec(){
        inquirer.prompt(this.getQuestions()).then(answers => {
            var environment = answers["environment"];
            console.log(os.tmpdir());
            var path = os.tmpdir()+"/installed_plataforma_"+environment;
            shell.mkdir('-p', path);
            shell.cd(path);
            shell.exec("git clone https://github.com/ONSBR/Plataforma-Installer.git");            

        });
    }

    getQuestions(){
        var questions = [];

        var q0 = {
            type: "input",
            default: "local",
            name: "environment",
            message: "Ambiente"
       };         
       questions.push(q0);
       return questions;
     }
}