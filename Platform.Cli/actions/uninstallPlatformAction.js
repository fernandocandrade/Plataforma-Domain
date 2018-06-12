const shell = require("shelljs");
const os = require("os");
module.exports = class UnInstallPlatformAction{

    exec(){
        var path = os.homedir()+"/installed_plataforma";
        shell.exec(`rm  -rf "${os.homedir()}/git-server"`)
        shell.cd(path+"/Plataforma-Installer");
        shell.exec("docker-compose down");
    }
};