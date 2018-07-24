const fs = require("fs");
const shell = require("shelljs");
const os = require("os");
const SystemCore = require("plataforma-sdk/services/api-core/system")
const MapCore = require("plataforma-sdk/services/api-core/map")
const ProcessCore = require("plataforma-sdk/services/api-core/process")
const EventCore = require("plataforma-sdk/services/api-core/event")
const OperationCore = require("plataforma-sdk/services/api-core/operation")

module.exports = class BaseDeployAction{

    constructor(){}

    registerSolution(env){
        var systemCore = new SystemCore({scheme:env.apiCore.scheme, host:env.apiCore.host,port:env.apiCore.port});
        var promise = new Promise((resolve,reject)=>{
          systemCore.findById(env.conf.solution.id).then( sys => {
                if (sys.length === 0){
                   systemCore.create(env.conf.solution).then((s)=>{
                        resolve(env);
                    });
                }else{
                    resolve(env);
                }
            });
        })
        return promise;
    }

    clone(obj) {
        return JSON.parse(JSON.stringify(obj));
    }

    indexMapFields(env,map){
        var promise = new Promise((resolve,reject)=>{
            try{
                resolve();
            }catch(e){
                reject(e);
            }
        });
        return promise;
    }

    saveMapToCore(env,map){
        return this.indexMapFields(env, map).then(() => this.persistMapToCore(env,map));
    }
    persistMapToCore(env,map){
        var mapCore = new MapCore({scheme:env.apiCore.scheme, host:env.apiCore.host,port:env.apiCore.port});
        var promise = new Promise((resolve,reject)=>{
            try{
                map.systemId = env.conf.solution.id;
                map.processId = env.conf.app.id;
                map.name = map.name.split(".")[0];
                mapCore.findByProcessId(map.processId).then(m =>{
                    mapCore.destroy(m).then(()=>{
                        mapCore.create(map).then(()=>{
                            resolve(env);
                        }).catch(reject);
                    });
                }).catch(reject);
            }catch(e){
                reject(e);
            }
        });
        return promise;
    }

    saveProcessToCore(env,process){
        var processCore = new ProcessCore({scheme:env.apiCore.scheme, host:env.apiCore.host,port:env.apiCore.port});
        var promise = new Promise((resolve,reject)=>{
            try{
                //TODO mudar para o metodo save
                processCore.findById(process.id).then((process)=>{
                    if (!process){
                        processCore.create(process).then(()=>{
                            resolve(env);
                        }).catch(reject);
                    }else{
                        processCore.save(process).then(()=>{
                            resolve(env);
                        }).catch(reject);
                    }

                }).catch(reject);
            }catch(e){
                reject(e);
            }
        });
        return promise;
    }

    saveOperationCore(env,operation){
        console.log(env)
        var operationCore = new OperationCore({scheme:env.apiCore.scheme, host:env.apiCore.host,port:env.apiCore.port});
        var promise = new Promise((resolve,reject)=>{
            try{
                operationCore.findByEventInAndSystemId(env.conf.solution.id, operation.event_in).then(ops =>{
                    if (ops.length > 0){
                        Object.assign(ops[0], operation);
                        operationCore.save(ops[0]).then(()=> resolve(ops[0])).catch(reject);
                    }else{
                        operationCore.create(operation).then((newOp)=>{
                           resolve(newOp[0]);
                       }).catch(reject);
                    }
                });
            }catch(e){
                reject(e);
            }
        });
        return promise;
    }

    readFile(path){
        var promise = new Promise((resolve,reject)=>{
            try{
                resolve(fs.readFileSync(path,"UTF-8"));
            }catch(e){
                reject(e);
            }
        });
        return promise;
    }

    getFileList(path){
        var promise = new Promise((resolve,reject)=>{
            try{
                var files = shell.ls(path);
                resolve(files);
            }catch(e){
                reject(e);
            }
        });
        return promise;
    }

    getFiles(env, folderName, action){
        var promise = new Promise((resolve,reject)=>{
            var pathMap = env.conf.fullPath+"/"+folderName+"/";
            this.getFileList(pathMap).then(list =>{
                var promises = [];
                list.forEach(f => {
                    promises.push(this.readFile(pathMap+f));
                });
                Promise.all(promises).then(values=>{
                    var waitToSave = [];
                    var i = 0;
                    values.forEach(v=>{
                        var obj = {};
                        obj.content = v;
                        obj.name = list[i];
                        waitToSave.push(action(env,obj));
                        i++;
                    });
                    Promise.all(waitToSave).then(values=>{
                        console.log(`${folderName} Installed`);
                        resolve(env);
                    })
                });
            })
        });
        return promise;
    }
}
