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
            shell.mkdir('-p', path+'/server',path+`/${plataforma.app.name}`,path+"/metadados",path+"/mapa");
            
            shell.touch(path + "/metadados/" + plataforma.app.name + ".yaml");
            
            shell.exec(`dotnet new solution -n ${plataforma.app.name} -o ${path}/server/`);
            
            let webAppName = plataforma.app.name + '.Presentation';
            shell.mkdir('-p', `${path}/server/${webAppName}`);
            shell.exec(`dotnet new webapi -n ${webAppName} -o ${path}/server/${webAppName}`);
            
            shell.exec(`dotnet new -i NUnit3.DotNetNew.Template`);
            let testProjectName = webAppName + '.Tests';
            shell.exec(`dotnet new nunit -n ${testProjectName} -o ${path}/server/${testProjectName}`);
            
            shell.exec(`dotnet sln ${path}/server/${plataforma.app.name}.sln add` + 
                ` ${path}/server/${webAppName}/${webAppName}.csproj ${path}/server/${testProjectName}/${testProjectName}.csproj`);
            
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