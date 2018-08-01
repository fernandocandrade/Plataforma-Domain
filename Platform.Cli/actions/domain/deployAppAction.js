const fs = require("fs");
const BuildAppAction = require("./buildAppAction");
const CompileAppAction = require("./compileAppAction");
const DockerService = require("../../services/docker");
const PortsService = require("../../services/ports");
const shell = require("shelljs");
const os = require("os");
const InstalledAppCore = require("plataforma-sdk/services/api-core/installedApp");
const DomainModelCore = require("plataforma-sdk/services/api-core/domainModel");
const System = require("plataforma-sdk/services/api-core/system");
const BaseDeployAction = require("../baseDeployAction");
const uuid = require("uuid/v4");
var yaml = require('js-yaml');

module.exports = class DeployAppAction extends BaseDeployAction {
    constructor(appInstance) {
        super();
        this.appInstance = appInstance;
        this.buildApp = new BuildAppAction();
        this.docker = new DockerService();
        this.ports = new PortsService();
        this.compiler = new CompileAppAction(appInstance);
    }
    deploy(_env) {
        this.compiler.exec(_env)
        .then(()=>{
            return this.saveSystem(_env)
        }).then(env =>{
            this.createDockerContainer(env).then(() => {
                if (env.conf.app.name !== "apicore") {
                    this.saveDomainToApiCore(env).then(() => this.saveToApiCore(env)).catch(e => {
                        console.log(e)
                    });
                    //this.saveToApiCore(env);
                } else {
                    console.log("App deployed");
                }
            });
        });
    }
    createDockerContainer(env) {
        return this.docker.compileDockerFile(env).then(() => {
            return this.docker.build(env, env.docker.tag);
        })/*.then(() => {
        //    return this.docker.publish(env, env.docker.tag);
        })*/.then(() => {
            return this.docker.rm(env);
        }).then(() => {
            env.variables = {"DOMAIN_API":"1"};
            return this.docker.run(env, env.docker.tag);
        }).then(()=>{
            return this.saveOperationCore(env,{
                "event_in": env.conf.solution.id+".persist.request",
                "event_out": env.conf.solution.id+".persist.done",
                "image": env.docker.tag,
                "version":env.conf.app.newVersion,
                "name": env.conf.app.name+".persist",
                "commit":true,
                "reprocessable":true,
                "processId": env.conf.app.id,
                "systemId": env.conf.solution.id
            });

        }).then(()=>{
            return this.saveOperationCore(env,{
                "event_in": env.conf.solution.id+".merge.request",
                "event_out": env.conf.solution.id+".merge.done",
                "image": env.docker.tag,
                "version":env.conf.app.newVersion,
                "name": env.conf.app.name+".merge",
                "commit":true,
                "reprocessable":false,
                "processId": env.conf.app.id,
                "systemId": env.conf.solution.id
            });

        }).catch(e => {
            console.log(e)
        });
    }

    saveSystem(env) {
        return new Promise((resolve,reject)=>{
            var systemCore  = new System(env.apiCore)
            systemCore.findById(env.conf.solution.id).then(found =>{
                if (found.length === 0) {
                    systemCore.create(env.conf.solution).then(()=>{
                        resolve(env)
                    }).catch(reject)
                }else{
                    resolve(env)
                }
            }).catch(reject)
        })
    }

    saveDomainToApiCore(env){
        return new Promise((resolve, reject)=>{
            this.domainModel = new DomainModelCore(env.apiCore);
            var basePath = env.appPath+"/Dominio";
            var entities = shell.ls(basePath).map(c => c);
            var entities = entities.map(e => ({
                systemId: env.conf.solution.id,
                name:e.split(".")[0],
                model:fs.readFileSync(basePath + "/"+e).toString(),
                version:env.conf.app.newVersion
            }))
            this.domainModel.findBySystemId(env.conf.solution.id).then(regs => {
                this.domainModel.destroy(regs).then(()=>{
                    this.domainModel.create(entities).then(resolve).catch(reject);
                }).catch(reject);
            })
        });
    }


};
