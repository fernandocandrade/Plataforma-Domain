const shell = require("shelljs");
const os = require("os");
module.exports = class StopPlatformAction{
    constructor(){}

    exec(){
        var path = os.tmpdir()+"/installed_plataforma";
        shell.cd(path+"/Plataforma-Installer");
        shell.exec("docker-compose down");
    }
}