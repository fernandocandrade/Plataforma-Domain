const fs = require("fs");
const BuildAppAction = require("./buildAppAction");
const DockerService = require("../../services/docker");
const PortsService = require("../../services/ports");
const shell = require("shelljs");
const os = require("os");
const InstalledAppCore = require("plataforma-sdk/services/api-core/installedApp");
const uuid = require("uuid/v4");

module.exports = class CompileAppAction {

    constructor(appInstance) {
        this.appInstance = appInstance;
        this.buildApp = new BuildAppAction();
        this.docker = new DockerService();
        this.ports = new PortsService();
    }
    exec(env) {
        return new Promise((resolve, reject) => {
            var config = env.conf;
            env.conf.app.newVersion = uuid();
            config.lock = this.appInstance.getLockInstance();
            env.docker = {
                tag: this.docker.getContainer(env),
                worker_tag: this.docker.getContainer(env,"worker"),
                port: this.ports.getNextAvailablePort()
            };
            if (env.conf.lock.id) {
                env.path = `${os.tmpdir()}/${env.conf.lock.id}`;
            } else {
                env.path = `${os.tmpdir()}/plataforma_${env.conf.app.id || env.conf.app.name}`;
            }
            console.log("Getting templates");
            var currentPath = process.cwd();
            env.appPath = currentPath;
            shell.cd(__dirname);
            shell.cd("../..");
            var cliPath = shell.pwd().toString();
            if (fs.existsSync(cliPath + "/python-template/")){
                shell.rm("-rf", cliPath + "/python-template/");
            }
            shell.cd("../Platform.App");
            shell.cp("-R", "python-template", cliPath);
            shell.cd(currentPath);
            console.log("Starting Compiling App");
            this.buildApp.build(env, (id) => {
                console.log("App Compiled");
                shell.cd(env.path);
                resolve(env);
            });
        });

    }
};