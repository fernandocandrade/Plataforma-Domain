const shell = require("shelljs");
const os = require("os");
module.exports = class UpgradeComponentAction{
    exec(components){
        if (components && components.length == 0){
            console.log("Você deve especificar qual componente será atualizado");
            return;
        }
        var path = os.homedir()+"/installed_plataforma";
        shell.cd(path+"/Plataforma-Installer");
        shell.exec("git pull");
        components.forEach(component => {
            this.upgradeComponent(component);
        });
        console.log("Componentes atualizados");
    }

    upgradeComponent(component){
        shell.exec(`docker-compose build --no-cache ${component}`);
        shell.exec(`docker-compose up -d ${component}`);
    }

};