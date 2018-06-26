var RemoteContext = require("../../remoteContext");
var Deployer = require("../../../services/deployer");
var AppInstance = require("../../../app_instance");
var fs = require("fs");

module.exports = class UploadPublicKey {
    constructor(){
        this.appInstance = new AppInstance();
        this.remoteContext = new RemoteContext();
        this.deployer = new Deployer(this.remoteContext);
    }

    exec() {
        var content = fs.readFileSync(this.remoteContext.user.pkey);
        var key = content.toString();
        if (this.remoteContext.user.email === "") {
            console.log("invalid email");
            return;
        }
        var solution = this.appInstance.getAppConfig()["solution"];
        this.deployer.uploadPublicKey("production",key,solution.name,`${this.remoteContext.user.email}.pub`).then(()=>{
            console.log(`public key installed for solution ${solution.name}`);
        }).catch(e => {
            console.log(e);
        });
    }
}