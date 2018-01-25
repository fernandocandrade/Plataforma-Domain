const shell = require("shelljs");
const os = require("os");
const fs = require("fs");
module.exports = class StartPlatformAction{
    constructor(){}

    exec(){
        var path = os.tmpdir()+"/installed_plataforma";
        shell.cd(path+"/Plataforma-Installer");
        shell.exec("docker-compose up -d");
        var apicore = `${os.tmpdir()}/plataforma_apicore/plataforma.instance.lock`;
        if (fs.existsSync(apicore)){
            var conf = JSON.parse(fs.readFileSync(apicore,'utf-8'));
            var cmd = `docker run -d --network=plataforma_network -p  9110:9110 --name apicore ${conf.docker.tag}`;
            shell.exec(cmd);
        }else{
            console.log("ApiCore not found please reinstall platform \n plataforma --install");
        }
    }
};