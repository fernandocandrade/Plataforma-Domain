var DockerService = require("../../services/docker");
var AppInstance = require("../../app_instance");
module.exports = class RunAppAction{
    constructor(){
        this.appInstance = new AppInstance();
        this.docker = new DockerService();
    }
    run(config){
        var instance = this.appInstance.getLockInstance();
        var env = this.appInstance.getAppConfig();
        var container_name = this.docker.getContainerName({conf:env});
        this.docker.start(container_name);
    }


};