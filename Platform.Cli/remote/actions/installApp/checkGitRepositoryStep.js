var shell = require("shelljs");

module.exports = class CheckGitRepositoryStep {
    constructor() {

    }

    exec(context){
        return new Promise((resolve, reject)=>{
            var out = shell.exec("git status .");
            if (out.code === 0) {
                resolve(context);
                return;
            }
            var inquirer = require("inquirer");
            inquirer.prompt([{
                type:"confirm",
                name:"createGitRepo",
                message:"Criar repositório local?"
            }]).then((answer)=>{
                if (answer["createGitRepo"]){
                    shell.exec("git init .");
                    resolve(context);
                }else{
                    reject(new Error("aborting app installation: git repository required"));
                }
            }).catch(reject);
        });
    }
}