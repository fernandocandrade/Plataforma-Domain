const shell = require("shelljs");
const uuid = require('uuid/v4');
const Handlebars = require('handlebars');
const fs = require("fs");
module.exports = class DockerService{
    constructor(){

    }

    build(env,tag){
        var promise = new Promise((resolve,reject)=>{
            try{
                var cmd = `docker build . --tag ${tag} -q --no-cache`;
                var first = shell.exec(cmd).stdout.toString().split("sha256:")[1];
                var imageId = first.replace("\n","");
                resolve({imageId:imageId});
            }catch(e){
                reject(e);
            }
        });
        return promise;
    }
    compileDockerFile(env){
      return new Promise((resolve,reject)=>{
        var source = fs.readFileSync(`${env.path}/Dockerfile.tmpl`).toString();
        var template = Handlebars.compile(source);
        var compiled = template(env.docker);
        fs.writeFileSync(`${env.path}/Dockerfile`,compiled,'utf-8');
        resolve(compiled);
      });

    }
    publish(env,tag){
      var promise = new Promise((resolve,reject)=>{
        try{
          var cmd = `docker push ${tag}`;
          shell.exec(cmd);
          resolve();
        }catch(e){
          reject(e);
        }
      });
      return promise;
    }

    run(env,tag){
      return new Promise((resolve,reject)=>{
          var cmd = `docker run -d --network=plataforma_network -p  ${env.docker.port}:${env.docker.port} --name ${env.conf.solution.name}-${env.conf.app.name} ${tag}`;
          shell.exec(cmd);
          resolve();
        resolve();
      });
    }

    rm(env){
      return new Promise((resolve,reject)=>{
          var cmd = `docker rm --force ${env.conf.solution.name}-${env.conf.app.name}`;
          shell.exec(cmd);
          resolve();
        resolve();
      });
    }

    getContainer(env){
      return `registry:5000/${env.conf.app.name}:${env.conf.app.newVersion}`;
    }

    getContainerLocal(env){
        return `localhost:5000/${env.conf.app.name}:${env.conf.app.newVersion}`;
    }


};
