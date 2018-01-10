const fs = require("fs");
const shell = require("shelljs");
const os = require("os");
const BaseDeployAction = require("../baseDeployAction");
module.exports = class DeployProcessAppAction extends BaseDeployAction{
    constructor(appInstance){
        super();
        this.appInstance = appInstance;
        
    }
    deploy(env){
        this.prepare(env)
        .then((prepared)=> this.copyFiles(prepared))
        .then(context => this.registerSolution(context))
        .then(this.finalize).catch(this.onError);
    }

    prepare(env){
        var promise = new Promise((resolve,reject)=>{
            console.log("Preparing Deploy");
            var path = os.tmpdir() + "/installed_plataforma";        
            var fullPath = path+"/apps/"+env.conf.app.version+"_"+env.conf.app.id;
            env.conf.fullPath = fullPath;
            env.conf.path = path;
            resolve(env);
        });
        return promise;
    }

    copyFiles(env){
        var promise = new Promise((resolve,reject)=>{            
            try{
                console.log("Copying Files")
                shell.rm("-rf",env.conf.fullPath);
                shell.mkdir("-p",env.conf.fullPath);
                shell.cp("-R",".",env.conf.fullPath);
                resolve(env);
            }catch(e){
                reject(e);
            }            
        });
        return promise;
    }

    

    registerApp(env){

    }

    finalize(){
        console.log("Finished deploy");
    }

    onError(e){
        console.log(e.toString());
    }
}