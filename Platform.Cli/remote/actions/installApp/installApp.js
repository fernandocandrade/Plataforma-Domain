var stepper = new(require("../../../stepper"));
var CheckGitRepositoryStep = require("./checkGitRepositoryStep");
var InstallAppPlatformStep = require("./installAppPlatformStep");
var AddRemoteToGitStep = require("./addRemoteToGitStep");
var AppContext = require("./installAppContext");
module.exports = class InstallApp {
    constructor(){
        stepper.addStep(new CheckGitRepositoryStep());
        stepper.addStep(new InstallAppPlatformStep());
        stepper.addStep(new AddRemoteToGitStep());
    }

    exec() {
        var context = new AppContext();
        stepper.exec(context).then(()=>{
            console.log("app installed");
        }).catch((e)=>{
            console.log(e);
        });
    }
}