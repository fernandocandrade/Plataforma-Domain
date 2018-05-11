const AppInstance = require("../../app_instance");
const uuidv4 = require('uuid/v4');
const BaseAction = require("../baseCreateAction");
var shell = require("shelljs");
var fs = require("fs");
const TecnologyApp = require("../tecnologyApp");

module.exports = class CreateAppAction{
    constructor(){
        this.appInstance = new AppInstance();
        this.baseAction = new BaseAction();
    }

    create(type){
        this.baseAction.create("process", TecnologyApp.node, (plataforma)=>{
            var path = process.cwd()+"/"+plataforma.app.name;
            shell.mkdir('-p', path+'/mapa',path+'/metadados',path+'/process', path+"/spec");
            shell.touch(path+"/process/"+plataforma.app.name+".js");
            shell.touch(path+"/metadados/"+plataforma.app.name+".yaml");

            const Dockerfile = `
FROM node:carbon
WORKDIR /usr/src/${plataforma.app.name}
COPY . .
CMD [ "node", "process/${plataforma.app.name}.js" ]
`
            fs.writeFileSync(path+"/Dockerfile",new Buffer(Dockerfile),"UTF-8")

            const specTest = `
describe('Sum example', function () {
    it('sum 1 plus 1', function () {
        expect(1+1).toEqual(2);
    });
});
            `
            fs.writeFileSync(path+`/spec/${plataforma.app.name}Spec.js`,new Buffer(specTest),"UTF-8")
            shell.cd(path);
            shell.exec("npm init -y");
            shell.exec("npm install jasmine-node --save");

            var npmConfig = JSON.parse(fs.readFileSync(path+"/package.json","UTF-8"));
            npmConfig.scripts = {};
            npmConfig.scripts.test = "./node_modules/.bin/jasmine-node spec";
            if (!npmConfig.dependencies){
                npmConfig.dependencies = {};
            }
            npmConfig.dependencies["plataforma-sdk"] = "git+https://github.com/ONSBR/Plataforma-SDK";
            fs.writeFileSync(path+"/package.json",JSON.stringify(npmConfig,null,4));
        })
    }
}