const shell = require("shelljs");
const uuid = require('uuid/v4');
const Handlebars = require('handlebars');
const fs = require("fs");
module.exports = class DockerService{
    constructor(){

    }

    build(env,tag, dockerfile){
        var promise = new Promise((resolve,reject)=>{
            try{
                var cmd = `docker build . --tag ${tag}  --no-cache`;
                if(dockerfile){
                  cmd = `docker build . -f ${dockerfile} --tag ${tag}  --no-cache`;
                }

                var imageId = shell.exec(cmd).stdout.toString();
                resolve({imageId:imageId});
            }catch(e){
                reject(e);
            }
        });
        return promise;
    }
    compileDockerFile(env){
      return new Promise((resolve,reject)=>{
        resolve(env);
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
          var externalPort = "8087";
          var labels = ""
          if (env.conf.app.type !== "process"){
            externalPort = "8088";
            env.docker.port = "8088";
            labels += ` --label traefik.backend=${env.conf.app.name}`
            labels += ` --label "traefik.${env.conf.app.name}.frontend.rule=PathPrefixStrip: /${env.conf.app.name}"`
            labels += ` --label traefik.docker.network=plataforma_network`
            labels += ` --label traefik.port=${env.docker.port}`
          }
          var _e = "";
          if(env.variables){
            Object.keys(env.variables).forEach(k => {
              _e = `${_e} -e ${k}=${env.variables[k]}`;
            })
          }
          var debugPort ="7" + (Math.floor(Math.random() * 1000)).toString();
          var cmd = `docker run -d --network=plataforma_network -p ${debugPort}:9229 ${_e} ${labels} --name ${this.getContainerName(env)} ${tag}`;
          console.log(cmd);
          shell.exec(cmd);
          resolve();
      });
    }

    start(containerName){
      return new Promise((resolve,reject)=>{
        var cmd = `docker start ${containerName}`;
        shell.exec(cmd);
        resolve();
      });
    }

    getContainerName(env){
      var name = env.conf.app.name;
      if (env.conf.solution.name !== "plataforma"){
        name = `${env.conf.solution.name}-${env.conf.app.name}`;
      }
      return name;
    }
    rm(env){
      return new Promise((resolve,reject)=>{
          var cmd = `docker rm --force ${this.getContainerName(env)}`;
          shell.exec(cmd);
          resolve();
        resolve();
      });
    }

    getContainer(env,worker){
      if (worker){
        return `registry:5000/${env.conf.app.name}_${worker}:${env.conf.app.newVersion}`;
      }
      return `registry:5000/${env.conf.app.name}:${env.conf.app.newVersion}`;
    }

    getContainerLocal(env){
        return `localhost:5000/${env.conf.app.name}:${env.conf.app.newVersion}`;
    }


};
