const fs = require("fs");
const BuildAppAction = require("./buildAppAction");
const CompileAppAction = require("./compileAppAction");
const DockerService = require("../../services/docker");
const PortsService = require("../../services/ports");
const shell = require("shelljs");
const os = require("os");
const InstalledAppCore = require("plataforma-sdk/services/api-core/installedApp");
const uuid = require("uuid/v4");
module.exports = class DeployAppAction {
    constructor(appInstance) {
        this.appInstance = appInstance;
        this.buildApp = new BuildAppAction();
        this.docker = new DockerService();
        this.ports = new PortsService();
        this.compiler = new CompileAppAction();
    }
    deploy(_env) {
        this.compiler.exec(_env).then(env =>{
            this.createDockerContainer(env).then(() => {
                if (config.app.name !== "apicore") {
                    this.saveToApiCore(env);
                } else {
                    console.log("App deployed");
                }
            });
        });
    }
    createDockerContainer(env) {
        return this.docker.compileDockerFile(env).then(() => {
            return this.docker.build(env, env.docker.tag);
        }).then(() => {
            return this.docker.publish(env, env.docker.tag);
        }).then(() => {
            return this.docker.rm(env);
        }).then(() => {
            return this.docker.run(env, env.docker.tag);
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
        this.installedAppCore.findBySystemId(config.solution.id).then(s => {
            if (s.length > 0) {
                this.installedAppCore.destroy(s[0]).then(() => {
                    this.installedAppCore.create(appInfo).then(s => {
                        console.log("App deployed");
                    });
                });
            } else {
                this.installedAppCore.create(appInfo).then(s => {
                    console.log("App deployed");
                });
            }
        }).catch(e => {
            console.log(e);
        });
    }
};
