var Deployer = require("../../../services/deployer");
var RemoteContext = require("../../remoteContext");
var AppInstance = require("../../../app_instance");
module.exports = class InstallAppPlatformStep {
    constructor() {
        this.remoteContext = new RemoteContext();
        this.deployer = new Deployer(this.remoteContext);
        this.appInstance = new AppInstance();
    }

    exec(context){
        return new Promise((resolve, reject)=>{
            var config = this.appInstance.getAppConfig();
            var app = {
                name:config["app"].name,
                id:config["app"].id,
                version:"",
                description: config["app"].description,
                type:config["app"].type,
                systemId:config["solution"].id
            };

            if (config["app"].type === "domain") {
                app.host = config["app"].name;
                app.port = 9110;
            }
            this.deployer.createApp("production",app).then((resp)=>{
                context.gitRemote = resp.git_remote;
                resolve(context);
            }).catch(reject);
        });
    }
}