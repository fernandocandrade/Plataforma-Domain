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
        var param = {
            conf:env,
            docker:instance.docker
        };
        if (param.docker){
            this.docker.run(param,param.docker.tag).then(e =>{
                console.log("Running app");
            });
        }else{
            console.log(`Cannot run a cleaned app, you should redeploy your app\n$ plataforma --deploy local`);
        }
    }


};