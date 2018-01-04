var fs = require("fs");
var BuildAppAction = require("./buildAppAction");
var shell = require("shelljs");
var os = require("os");
module.exports = class RunAppAction{
    constructor(){
        this.buildApp = new BuildAppAction();
    }
    run(config){        
        this.buildApp.build(()=>{
            shell.cd(os.tmpdir()+"/bundle");
            shell.exec("npm install");
            shell.exec("node main.js");
        });
        
    }    
}