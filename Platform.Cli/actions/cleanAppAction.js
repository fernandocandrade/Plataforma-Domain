var DomainCleanApp = require("./domain/cleanAppAction");
module.exports = class CleanAppAction{
    constructor(){
        this.domainCleanApp = new DomainCleanApp();
    }
    exec(type){
        this.domainCleanApp.clean();
    }
}