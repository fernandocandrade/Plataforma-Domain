/**
 * Esta action compila a App
 */
const AppInstance = require("../app_instance");
const DomainCompileAppAction = require("./domain/compileAppAction");
const Env = require("../env/environment");
module.exports = class CompileAppAction {

    constructor() {
        this.appInstance = new AppInstance();
        this.env = new Env();
        this.domainCompileAppAction = new DomainCompileAppAction(this.appInstance);
    }
    exec(environment) {
        var conf = this.appInstance.getAppConfig();
        var env = {};
        env.conf = conf;
        switch (conf.app.type) {
            case "domain":
                this.domainCompileAppAction.exec(env);
                break;
            default:
                console.log("Not supported app type");
        }
    }
}