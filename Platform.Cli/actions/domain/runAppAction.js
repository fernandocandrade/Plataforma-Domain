var fs = require("fs");
var BuildAppAction = require("./buildAppAction");
var shell = require("shelljs");
var os = require("os");
module.exports = class RunAppAction{
    constructor(){
        this.buildApp = new BuildAppAction();
    }
    run(config){
        console.log("Getting templates");
        var currentPath = process.cwd();
        shell.cd(__dirname);
        shell.cd("../..");
        var cliPath = shell.pwd().toString();
        shell.rm("-rf",cliPath+"/node_template/");
        shell.cd("../Platform.App");
        shell.cp("-R","node_template",cliPath);
        shell.cd(currentPath);        
        console.log("Starting building App");
        this.buildApp.build(config,(id)=>{
            shell.cd(os.tmpdir()+"/"+id);
            console.log("Installing dependencies");
            shell.exec("npm install");
            console.log("Running app");
            shell.exec("node main.js");
        });
        
    }    
}