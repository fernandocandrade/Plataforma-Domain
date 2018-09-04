const BaseAction = require("../../baseCreateAction");
var shell = require("shelljs");
var fs = require("fs");
const TecnologyApp = require("../../tecnologyApp");

module.exports = class CreatePresentationAppAction{
    constructor(){
        this.baseAction = new BaseAction();
    }

    create(type){
        this.baseAction.create("presentation", TecnologyApp.dotnet, (plataforma)=>{
            
            var path = process.cwd()+"/"+plataforma.app.name;
            shell.mkdir('-p', path+'/server',path+"/metadados",path+"/mapa");
            
            shell.touch(path + "/metadados/" + plataforma.app.name + ".yaml");
            
            shell.exec(`dotnet new solution -n ${plataforma.app.name} -o ${path}/`);
            
            let webAppName = plataforma.app.name;
            shell.exec(`dotnet new webapi -n ${webAppName} -o ${path}/server`);
            
            shell.exec(`dotnet new -i NUnit3.DotNetNew.Template`);
            let testProjectName = webAppName + '.UnitTest';
            shell.exec(`dotnet new nunit -n ${testProjectName} -o ${path}/test/unit`);
            
            shell.exec(`dotnet sln ${path}/${plataforma.app.name}.sln add` + 
                ` ${path}/server/${webAppName}.csproj ${path}/test/unit/${testProjectName}.csproj`);
            
            const Dockerfile = `
FROM microsoft/dotnet:2.1-sdk
COPY . .
ENV PORT 8088
CMD [ "dotnet", "server/${webAppName}.dll" ]
`
            fs.writeFileSync(path+"/Dockerfile",new Buffer(Dockerfile),"UTF-8");

        });
    }
}