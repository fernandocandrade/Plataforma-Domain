const fs = require("fs");
const BuildAppAction = require("./buildAppAction");
const CompileAppAction = require("./compileAppAction");
const DockerService = require("../../services/docker");
const PortsService = require("../../services/ports");
const shell = require("shelljs");
const os = require("os");
const InstalledAppCore = require("plataforma-sdk/services/api-core/installedApp");
const BaseDeployAction = require("../baseDeployAction");
const uuid = require("uuid/v4");
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
        this.compiler.exec(_env).then(env =>{
            this.createDockerContainer(env).then(() => {
                if (env.conf.app.name !== "apicore") {
                    this.saveToApiCore(env);
                } else {
                    console.log("App deployed");
                }
            });
        });
    }
    createDockerContainer(env) {
        return this.docker.compileDockerFile(env).then(() => {
            console.log("A");
            return this.docker.build(env, env.docker.tag);
        }).then(() => {
            console.log("B");
            return this.docker.publish(env, env.docker.tag);
        }).then(() => {
            console.log("C");
            return this.docker.rm(env);
        }).then(() => {
            console.log("D");
            return this.docker.run(env, env.docker.tag);
        }).then(()=>{
            console.log("E");
            return this.docker.build(env, env.docker.worker_tag,"DockerfileWorker");
        }).then(() => {
            console.log("F");
            return this.docker.publish(env, env.docker.worker_tag);
        }).then(()=>{
            return this.saveOperationCore(env,{
                "event_in": env.conf.solution.id+".persist.request",
                "event_out": env.conf.solution.id+".persist.done",
                "image": env.docker.worker_tag,
                "name": env.conf.app.name+".persist",
                "processId": env.conf.app.id,
                "systemId": env.conf.solution.id
            });

        });
    }
    saveToApiCore(env) {
        var config = env.conf;
        var appInfo = {
            systemId: config.solution.id,
            name: config.app.name,
            host: this.docker.getContainerName(env),
            type: "domain",
            port: env.docker.port
        };
        this.installedAppCore = new InstalledAppCore(env.apiCore);
        this.installedAppCore.create(appInfo).then(s => {
            console.log("App deployed");
        }).catch(e => {
            console.log(e);
        });
    }
};
