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
}