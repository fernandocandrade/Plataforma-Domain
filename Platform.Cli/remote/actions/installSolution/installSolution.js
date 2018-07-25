var RemoteContext = require("../../remoteContext");
var Deployer = require("../../../services/deployer");
var AppInstance = require("../../../app_instance");
module.exports = class InstallSolution {
    constructor() {
        this.appInstance = new AppInstance();
        this.remoteContext = new RemoteContext();
        this.deployer = new Deployer(this.remoteContext);
    }

    exec(){
        var info = this.appInstance.getAppConfig();
        if(!info.solution) {
            console.log("cannot install solution on platform, solution not found");
            return;
        }
        var solution = info.solution;
        this.deployer.createSolution("production",solution).then((s)=>{
            console.log("solution installed on production");
        }).catch(e => console.log("solution not installed ",e));

    }
}