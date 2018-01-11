const fs = require("fs");
const shell = require("shelljs");
const os = require("os");
const SystemCoreLib = require("plataforma-sdk/services/api-core/system")
/**
 * classe temporaria da lib so para nao ficar travado
 */
class SystemCore extends SystemCoreLib{
    findById(id){
        return new Promise((resolve,reject)=>{
            resolve({id:"adasd"});
        });

        /*return this.find({
            filterName:"byId",
            fieldName:"id",
            fieldValue: id
        })*/
    }

    save(system){

    }
}
module.exports = class BaseDeployAction{

    constructor(){}

    registerSolution(env){
        var systemCore = new SystemCore({ip:env.apiCore.host,port:env.apiCore.port});
        var promise = new Promise((resolve,reject)=>{
            systemCore.findById(env.conf.solution.id).then( sys => {
                if (!sys){
                    //não existe uma solution criada
                    //deve se criar uma solution na plataforma
                    resolve(env);
                }else{
                    resolve(env);
                }
            });
        })
        return promise;
    }

    saveMapToCore(env,map){
        var promise = new Promise((resolve,reject)=>{
            try{
                resolve(env);
            }catch(e){
                reject(e);
            }
        });
        return promise;
    }

    saveOperationCore(env,operation){
        var promise = new Promise((resolve,reject)=>{
            try{
                console.log(operation);
                resolve(env);
            }catch(e){
                reject(e);
            }
        });
        return promise;
    }

    saveEventOperationsCore(env,events){
        var promise = new Promise((resolve,reject)=>{
            try{
                console.log(events);
                resolve(env);
            }catch(e){
                reject(e);
            }
        });
        return promise;
    }

    saveProcessEventsApiCore(env,processEvents){
        var promise = new Promise((resolve,reject)=>{
            try{
                resolve(env);
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
        console.log(`Installing ${folderName}`)
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