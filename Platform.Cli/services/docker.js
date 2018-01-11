const shell = require("shelljs");

module.exports = class DockerService{
    constructor(){

    }

    build(env,tag){
        var promise = new Promise((resolve,reject)=>{
            try{
                var cmd = `docker build . --tag ${tag} -q --no-cache`
                var first = shell.exec(cmd).stdout.toString().split("sha256:")[1];
                var imageId = first.replace("\n","");
                resolve({imageId:imageId});
            }catch(e){
                reject(e);
            }
        })
        return promise;
    }
}