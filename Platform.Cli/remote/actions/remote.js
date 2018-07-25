var RemoteContext = require("../remoteContext");

var stepper = new(require("../../stepper"));
var ConfigPlatformHost = require("./config_steps/configPlatformHostStep");
var CreateSSHKey = require("./config_steps/createSSHKey");
module.exports = class Remote {

    /** Este método seta o cli para trabalhar em modo remoto */

    constructor() {
        stepper.addStep(new CreateSSHKey());
        stepper.addStep(new ConfigPlatformHost());
    }

    exec() {
        var context = new RemoteContext();
        stepper.exec(context).then(() => {
            context.enabled = true;
            context.persist();
        }).catch(_ => {

        });
    }
};