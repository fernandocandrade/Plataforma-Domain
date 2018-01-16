const fs = require("fs");
const shell = require("shelljs");
const os = require("os");
const BaseDeployAction = require("../baseDeployAction");
const DockerService = require("../../services/docker");
module.exports = class DeployProcessAppAction extends BaseDeployAction{
    constructor(appInstance){
        super();
        this.appInstance = appInstance;
        this.docker = new DockerService();

    }
    deploy(env){
        this.prepare(env)
        .then((prepared)=> this.copyFiles(prepared))
        .then(context => this.registerSolution(context))
        .then(context => this.registerApp(context))
        .then(context => this.uploadMaps(context))
        .then(context => this.uploadMetadata(context))
        .then(this.finalize).catch(this.onError);
    }

    prepare(env){
        var promise = new Promise((resolve,reject)=>{
            console.log("Preparing Deploy");
            var path = os.tmpdir() + "/installed_plataforma";
            var fullPath = path+"/apps/"+env.conf.app.version+"_"+env.conf.app.id;
            env.conf.fullPath = fullPath;
            env.conf.path = path;
            env.conf.appPath = process.cwd();
            env.conf.app.newVersion = require('uuid/v4')();
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

    uploadMaps(env){
        return this.getFiles(env,"mapa",(ctx,v)=>this.saveMapToCore(ctx,v));
    }

    uploadMetadata(env){
        var promise = this.getFiles(env,"metadados",(ctx,v)=>this.processMetadata(ctx,v));
        return promise;
    }

    processMetadata(env,metadata){
        if(metadata.name.indexOf(".yaml") > 0 || metadata.name.indexOf(".yml") > 0){
            return this.processOperations(env,metadata);
        }else{
            return new Promise((resolve)=>resolve(env));
        }
    }

    processEventCatalog(env, metadata){
        var events = eval(metadata.content);
        var processEvents = [];
        Object.keys(events).forEach(k => {
            var processEvent = {};
            processEvent.systemId = env.conf.solution.id;
            processEvent.processId = env.conf.app.id;
            processEvent.name = events[k];
            processEvents.push(processEvent);
        });
        return this.saveProcessEventsApiCore(env,processEvents);
    }

    processOperations(env, metadata){
        var promise = new Promise((resolve,reject)=>{
            try{
              var yaml = require('js-yaml');
              var operations = yaml.safeLoad(metadata.content);
                var promises = [];
                operations["operations"].forEach(op =>{
                    promises.push(this.processOperation(env,op));
                })
                Promise.all(promises).then(values => {
                    resolve(env);
                })
                resolve(env);
            }catch(e){
               reject(e);
            }
        });
    }

    processOperation(env,operation){
        var promise = new Promise((resolve,reject)=>{
          try{
                operation.systemId = env.conf.solution.id;
                operation.processId = env.conf.app.id;
                operation.event_in = operation.event;
                operation.event_out = `${operation.name}_done`;
                operation.container = this.docker.getContainer(env);
                this.saveOperationCore(env,operation).then((c)=>{
                    resolve(env);
                })
            }catch(e){
                reject(e);
            }
        });
    }
    registerApp(env){
        var promise = new Promise((resolve,reject)=>{
            var process = {};
            process.systemId = env.conf.solution.id;
            process.id = env.conf.app.id;
            process.name = env.conf.app.name;
            process.relativePath = env.conf.fullPath;
            process.deployDate = new Date();
            process.tag = this.docker.getContainer(env);
            this.docker.build(env,process.tag).then((r)=>{
              process.image = r.imageId;
              this.docker.publish(env,process.tag).then(()=>{
                this.saveProcessToCore(env,process).then(()=>{
                    resolve(env);
                }).catch(reject)
              })
            }).catch(reject);
        });
        return promise;
    }

    finalize(){
        console.log("Finished deploy");
    }

    onError(e){
        console.log(e.toString());
    }
}
