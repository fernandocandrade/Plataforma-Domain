const shell = require("shelljs");
const os = require("os");
const AppInstance = require("../app_instance");
const uuidv4 = require('uuid/v4');
const inquirer = require('inquirer');
const fs = require("fs");
const StopPlatformAction = require("./stopPlatformAction");
module.exports = class InstallPlatformAction{

    exec(){

        inquirer.prompt(this.getQuestions()).then(answers => {
            var environment = answers.environment;
            console.log(os.homedir());
            // new StopPlatformAction().exec();
            var path = os.homedir()+"/installed_plataforma";
            if (fs.existsSync(path)){
                shell.cd(path+"/Plataforma-Installer");
                shell.exec("git pull");
            }else{
                shell.rm("-rf",path);
                shell.mkdir('-p', path);
                shell.cd(path);
                shell.exec("git clone https://github.com/ONSBR/Plataforma-Installer.git");
                shell.cd("Plataforma-Installer");
            }
            shell.exec(`mkdir -p "${os.homedir()}/git-server/keys"`)
            shell.exec(`mkdir -p "${os.homedir()}/git-server/repos"`)
            shell.exec("docker network rm plataforma_network");
            shell.exec("docker network create --driver=bridge plataforma_network");
            shell.exec("docker-compose build --no-cache");
            shell.exec("docker-compose up -d");
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
