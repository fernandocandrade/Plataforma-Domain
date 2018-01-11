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
        var promise = this.getFiles(env,"mapa",(ctx,v)=>this.saveMapToCore(ctx,v));
        return promise;
    }

    uploadMetadata(env){
        var promise = this.getFiles(env,"metadados",(ctx,v)=>this.processMetadata(ctx,v));
        return promise;
    }

    processMetadata(env,metadata){
        if (metadata.name == "EventCatalog.js"){
            return this.processEventCatalog(env,metadata);
        }else if(metadata.name.indexOf(".yaml") > 0 || metadata.name.indexOf(".yml") > 0){
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
            processEvent.processVersion = env.conf.app.version;
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
                operations["operacao"].forEach(op =>{
                    promises.push(this.processOperation(env,op["operacoes"]));
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

                var op = {};
                op.systemId = env.conf.solution.id;
                op.processId = env.conf.app.id;
                op.processName = env.conf.app.name;
                op.method = operation.metodo;
                op.filePath = operation.caminhoDoArquivo;
                var eventsByOperation = operation["eventos-entrada"] || [];
                eventsByOperation = eventsByOperation.map(evt =>{
                    var event = {};
                    event.systemId  = op.systemId;
                    event.processId = op.processId;
                    event.processName = env.conf.app.name;
                    event.name = evt;
                    event.direction = "inbound";
                    return event;
                });

                var eventsByOperationOut = operation["eventos-saida"] || [];
                eventsByOperationOut = eventsByOperationOut.map(evt =>{
                    var event = {};
                    event.systemId  = op.systemId;
                    event.processId = op.processId;
                    event.processName = env.conf.app.name;
                    event.name = evt;
                    event.direction = "outbound";
                    return event;
                });
                eventsByOperation = eventsByOperation.concat(eventsByOperationOut);
                this.saveOperationCore(env,op).then(()=>{
                    this.saveEventOperationsCore(env,eventsByOperation).then(()=>{
                        resolve(env);
                    });
                })
            }catch(e){
                reject(e);
            }
        });
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