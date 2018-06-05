/**
 * Esta action faz o deploy da App
 * dentro do ambiente da plataforma
 */
const AppInstance = require("../app_instance");
const DeployProcessAppAction = require("./process/deployAppAction");
const DeployDotNetProcessAppAction = require("./process/dotnet/deployDotNetAppAction");
const DeployDotNetPresentationAppAction = require("./presentation/dotnet/deployDotNetAppAction");
const DeployDomainAppAction = require("./domain/deployAppAction");
const Env = require("../env/environment");
const TecnologyApp = require("./tecnologyApp")

module.exports = class DeployAppAction {

    constructor() {
        this.appInstance = new AppInstance();
        this.env = new Env();
        this.deployProcessAppAction = new DeployProcessAppAction(this.appInstance);
        this.deployDotNetProcessAppAction = new DeployDotNetProcessAppAction(this.appInstance);
        this.deployDotNetPresentationAppAction = new DeployDotNetPresentationAppAction(this.appInstance);
        this.deployDomainAppAction = new DeployDomainAppAction(this.appInstance);
    }
    exec(environment) {
        if (typeof (environment) !== "string") {
            console.log("Invalid Environment");
            console.log("Example: plataforma --deploy local");
            return;
        }
        var conf = this.appInstance.getAppConfig();
        var env = this.env.getEnv(environment);
        env.conf = conf;
        env.metamapa = this.metamapa;
        switch (conf.app.type) {
            case "process":
                if (conf.app.tecnology == TecnologyApp.dotnet) {
                    this.deployDotNetProcessAppAction.deploy(env);
                } else {
                    this.deployProcessAppAction.deploy(env);
                }
                break;
            case "presentation":
                if (conf.app.tecnology == TecnologyApp.dotnet) {
                    this.deployDotNetPresentationAppAction.deploy(env);
                } else {
                    this.deployProcessAppAction.deploy(env);
                }
                break;
            case "domain":
                this.deployDomainAppAction.deploy(env);
                break;
            default:
                console.log("Not supported app type");
        }
    }
}