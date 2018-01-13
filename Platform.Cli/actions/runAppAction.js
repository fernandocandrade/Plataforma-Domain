/**
 * Esta action roda a aplicação de forma local
 */

 const RunDomainApp = require("./domain/runAppAction");
var fs = require("fs");
module.exports = class RunAppAction{
        
    constructor(){
        this.runDomainApp = new RunDomainApp();
    }
    exec(){
        var root = process.cwd();
        var config = this.getConfig(root);
        if(!config.app){
            console.log("Runnable app is not found");
            return;
        }
        switch (config.app.type){
            case "domain":
                this.runDomainApp.run(config);
                break;
            default:
                console.log(`Invalid app type ${config.app.type}`);
        }
    }

    getConfig(root){
        return JSON.parse(fs.readFileSync(root+"/plataforma.json","UTF-8"));
    }
}