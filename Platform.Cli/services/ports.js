var shell = require("shelljs");
var os = require("os");
var fs = require("fs");
module.exports = class Ports{
    
    path(){
        return os.tmpdir();
    }
    /**
     * @description este método retorna uma próxima porta 
     * disponível para ser usada por uma aplicação
     */
    getNextAvailablePort(){
        var port = 9090;
        var ports = this.getUsedPorts();
        if (ports.length > 0){
            return this.getUsedPorts().pop() + 1;
        }        
        return port;
    }

    getUsedPorts(){
        return this.getInstalledApps().map(app => {
            var instance = JSON.parse(fs.readFileSync(this.path()+"/"+app+"/plataforma.instance.lock"));
            return instance.port;
        }).sort();
    }

    getInstalledApps(){
        return shell.ls(this.path()).filter(item => {
            return item.indexOf("plataforma_") === 0;
        });
    }
}