var shell = require("shelljs");

module.exports = class CreateSSHKey {

    exec(context) {
        return new Promise((res, rej) => {
            var inquirer = require('inquirer');
            inquirer.prompt([{
                type: "confirm",
                default: "",
                name: "hasPublicKey",
                message: "Você já possui uma chave pública rsa?"
            }]).then(answers => {
                if (!answers["hasPublicKey"]) {
                    console.log("Para continuar você precisa gerar um par de chaves rsa")
                    console.log("utilize o comando ssh-keygen para gerar seu par de chaves")
                    console.log('exemplo: ssh-keygen -b 4048 -t rsa -C "<your_email>"')
                    rej(context);
                } else {
                    inquirer.prompt([{
                        type:"input",
                        default:`${require("os").homedir()}/.ssh/id_rsa.pub`,
                        name:"publicKey",
                        message:"Informe o caminho da sua chave pública"
                    },{
                        type:"input",
                        default:"",
                        name:"email",
                        message:"Informe o seu email"
                    }]).then((answer) => {
                        context.user.pkey = answer["publicKey"];
                        context.user.email = answer["email"];
                        res(context);
                    })
                }
            });
        });
    }
}