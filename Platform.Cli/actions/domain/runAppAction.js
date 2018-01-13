var fs = require("fs");
var shell = require("shelljs");
var os = require("os");
var Env = require("../../env/environment");
module.exports = class RunAppAction{
    constructor(){
        this.env = new Env();
    }
    run(config){
        var currentPath = process.cwd();
        var conf = this.env.getEnv("local");
        var instance = JSON.parse(fs.readFileSync(process.cwd()+"/plataforma.instance.lock"));
        shell.cd(os.tmpdir()+"/"+instance.id);
        console.log("Running app");
        shell.exec("node main.js");
    }
}