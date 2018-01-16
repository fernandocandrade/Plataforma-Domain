const shell = require("shelljs");
const uuid = require('uuid/v4');
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

    publish(env,tag){
      var promise = new Promise((resolve,reject)=>{
        try{
          var cmd = `docker push ${tag}`
          shell.exec(cmd);
          resolve();
        }catch(e){
          reject(e);
        }
      });
      return promise;
    }

    getContainer(env){
      return `registry:5000/${env.conf.app.name}:${env.conf.app.newVersion}`
    }

    getContainerLocal(env){
        return `localhost:5000/${env.conf.app.name}:${env.conf.app.newVersion}`
      }


}
