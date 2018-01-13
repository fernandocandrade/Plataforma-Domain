var fs = require("fs");
var BuildAppAction = require("./buildAppAction");
var shell = require("shelljs");
var os = require("os");
const InstalledAppCore = require("plataforma-sdk/services/api-core/installedApp");
module.exports = class DeployAppAction{
    constructor(appInstance){
        this.appInstance = appInstance;
        this.buildApp = new BuildAppAction();
        
    }
    deploy(env){
        var config = env.conf;
        config.lock = this.appInstance.getLockInstance();
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
            if (config.app.name !== "Plataforma.ApiCore"){
                this.saveToApiCore(env);
            }else{
                console.log("App deployed");
            }
        });
        
    }

    saveToApiCore(env){
        var appInfo = {
            systemId: config.solution.id,
            name: config.app.name,
            host: "localhost",
            type: "domain",
            port: config.lock.port
        };
        this.installedAppCore = new InstalledAppCore(env["apiCore"]);
        this.installedAppCore.findBySystemId(config.solution.id).then(s =>{
            if (s.length > 0){
                this.installedAppCore.destroy(s[0]).then(()=>{
                    this.installedAppCore.create(appInfo).then(s =>{
                        console.log("App deployed");
                    })
                })
            }else{
                this.installedAppCore.create(appInfo).then(s =>{
                    console.log("App deployed");
                })
            }
        }).catch(e =>{
            console.log(e);
        })
    }
}