const fs = require("fs");
const BuildAppAction = require("./buildAppAction");
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
    }
    deploy(env) {
        var config = env.conf;
        env.conf.app.newVersion = uuid();
        config.lock = this.appInstance.getLockInstance();
        env.docker = {
            tag: this.docker.getContainer(env),
            port: this.ports.getNextAvailablePort()
        };
        if (env.conf.lock.id) {
            env.path = `${os.tmpdir()}/${env.conf.lock.id}`;
        } else {
            env.path = `${os.tmpdir()}/plataforma_${env.conf.app.id || env.conf.app.name}`;
        }
        console.log("Getting templates");
        var currentPath = process.cwd();
        shell.cd(__dirname);
        shell.cd("../..");
        var cliPath = shell.pwd().toString();
        shell.rm("-rf", cliPath + "/node_template/");
        shell.cd("../Platform.App");
        shell.cp("-R", "node_template", cliPath);
        shell.cd(currentPath);
        console.log("Starting building App");
        this.buildApp.build(env, (id) => {
            shell.cd(env.path);
            console.log("Installing dependencies");
            shell.exec("npm install");
            this.createDockerContainer(env).then(() => {
                shell.cd(cliPath);
                console.log("cleaning temporary files");
                shell.rm("-rf",env.path);
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
