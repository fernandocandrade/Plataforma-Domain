const fs = require("fs");
const shell = require("shelljs");
const os = require("os");
const BaseDeployAction = require("../baseDeployAction");
const DockerService = require("../../services/docker");
const DependencyDomainCore = require("plataforma-sdk/services/api-core/dependencyDomain");


module.exports = class DeployProcessAppAction extends BaseDeployAction {
    constructor(appInstance) {
        super();
        this.appInstance = appInstance;
        this.docker = new DockerService();
    }
    deploy(env) {
        var prep = this.prepare(env);
        if (!env.metamapa) {
            prep = prep.then((prepared) => this.copyFiles(prepared))
                .then(context => this.registerSolution(context))
                .then(context => this.registerApp(context));
        }
        prep = prep.then(context => this.uploadMaps(context))
            .then(context => this.uploadMetadata(context))
            .then(context => this.uploadDomainDependency(context));
        prep.then(this.finalize).catch(this.onError);
    }

    prepare(env) {
        var promise = new Promise((resolve, reject) => {
            console.log("Preparing Deploy");
            var path = os.homedir() + "/installed_plataforma";
            var fullPath = path+"/apps/"+env.conf.app.version+"_"+env.conf.app.id;
            env.conf.fullPath = fullPath;
            env.conf.path = path;
            env.conf.appPath = process.cwd();
            env.conf.app.newVersion = require('uuid/v4')();
            resolve(env);
        });
        return promise;
    }

    copyFiles(env) {
        var promise = new Promise((resolve, reject) => {
            try {
                var source = ".";
                var dest = env.conf.fullPath;
                console.log("Copying Files");
                shell.rm("-rf",env.conf.fullPath);
                shell.mkdir("-p",env.conf.fullPath);
                shell.cp("-R",".",env.conf.fullPath);
                resolve(env);
            } catch (e) {
                reject(e);
            }
        });
        return promise;
    }

    uploadMaps(env) {
        return this.getFiles(env, "mapa", (ctx, v) => this.saveMapToCore(ctx, v));
    }

    uploadMetadata(env) {
        var promise = this.getFiles(env, "metadados", (ctx, v) => this.processMetadata(ctx, v));
        return promise;
    }

    processMetadata(env, metadata) {
        if (metadata.name.indexOf(".yaml") > 0 || metadata.name.indexOf(".yml") > 0) {
            return this.processOperations(env, metadata);
        } else {
            return new Promise((resolve) => resolve(env));
        }
    }

    processEventCatalog(env, metadata) {
        var events = eval(metadata.content);
        var processEvents = [];
        Object.keys(events).forEach(k => {
            var processEvent = {};
            processEvent.systemId = env.conf.solution.id;
            processEvent.processId = env.conf.app.id;
            processEvent.name = events[k];
            processEvents.push(processEvent);
        });
        return this.saveProcessEventsApiCore(env, processEvents);
    }

    processOperations(env, metadata) {
        var promise = new Promise((resolve, reject) => {
            try {
                var yaml = require('js-yaml');
                var operations = yaml.safeLoad(metadata.content);
                var promises = [];
                operations["operations"].forEach(op => {
                    promises.push(this.processOperation(env, op));
                })
                Promise.all(promises).then(values => {
                    resolve(env);
                })
                resolve(env);
            } catch (e) {
                reject(e);
            }
        });
    }

    processOperation(env, operation) {
        var promise = new Promise((resolve, reject) => {
            try {
                operation.systemId = env.conf.solution.id;
                operation.processId = env.conf.app.id;
                operation.event_in = operation.event;
                operation.event_out = `${operation.name}.done`;
                operation.image = this.docker.getContainer(env);
                operation.version = env.conf.app.newVersion;
                env.image = operation.image;
                this.saveOperationCore(env,operation).then((c)=>{
                    resolve(env);
                });
            } catch (e) {
                reject(e);
            }
        });
    }

    uploadDomainDependency(env) {
        return new Promise((resolve, reject)=>{
            console.log("Compiling data dependency")
            this.getFiles(env, "mapa", (ctx, v) => {
                var yaml = require('js-yaml');
                var map = yaml.safeLoad(v.content);
                var model = this.getDependency(map);
                if (!model) {
                    resolve(env);
                    return;
                }
                var dep = {
                    "entity": model,
                    "systemId": env.conf.solution.id,
                    "processId": env.conf.app.id,
                    "version": env.conf.app.newVersion
                }
                var api = new DependencyDomainCore({scheme:env.apiCore.scheme, host:env.apiCore.host,port:env.apiCore.port});
                api.save(dep).then(e => {
                    resolve(env);
                }).catch(reject);
            });
        });
    };

    getDependency(map) {
        /**
         * Para saber se uma process app tem uma dependencia funcional com alguma entidade do dominio
         * devemos verificar se a process app faz algum filtro no domain
         * o fato de realizar algum filtro no dominio já caracteriza uma dependencia funcional
         * pois independente dos campos é muito arriscado, a principio, a plataforma julgar uma dependencia funcional
         * observando modficações em campos de entidade
         */
        var model = null;
        Object.keys(map).forEach(entity => {
            if (map[entity]["filters"]) {
                var filters = map[entity]["filters"]
                if (Object.keys(filters).length > 0) {
                    model =  map[entity].model
                    return false;
                }
            }
        });
        return model;
    }

    registerApp(env) {
        var promise = new Promise((resolve, reject) => {
            var process = {};
            process.systemId = env.conf.solution.id;
            process.id = env.conf.app.id;
            process.name = env.conf.app.name;
            process.relativePath = env.conf.fullPath;
            process.deployDate = new Date();
            process.tag = this.docker.getContainer(env);
            this.docker.build(env, process.tag).then((r) => {
                process.image = r.imageId;
                //console.log("Docker publish...");
                //this.docker.publish(env, process.tag).then(() => {
                    this.saveProcessToCore(env, process).then(() => {
                        if (env.conf.app.type === "presentation"){
                            env.docker = {port:"8087"};
                            console.log("presentation app should start app");
                            this.docker.rm(env).then(()=>{
                                env.variables = {};
                                env.variables["API_MODE"] = true;
                                env.variables["SYSTEM_ID"] = env.conf.solution.id;
                                this.docker.run(env, process.tag).then(r => resolve(env));
                            });
                        }else{
                            resolve(env);
                        }
                    }).catch(reject);
                //});
            }).catch(reject);
        });
        return promise;
    }

    finalize() {
        console.log("Finished deploy");
    }

    onError(e) {
        console.log(e.toString());
    }
}
