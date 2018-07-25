module.exports = class ConfigPlatformHostStep {

    exec(context) {
        return new Promise((res, rej) => {
            var inquirer = require('inquirer');
            inquirer.prompt([{
                type: "input",
                default: "http://localhost:6970",
                name: "urlProd",
                message: "Informe a URL da Plataforma de Produção"
            }]).then(answers => {
                context.production.url = answers["urlProd"]
                res(context);
            });
        });
    }
}