const AppInstance = require("../../app_instance");
const uuidv4 = require('uuid/v4');
const BaseAction = require("../baseCreateAction");
var shell = require("shelljs");
var fs = require("fs");


module.exports = class CreateAppAction {
    constructor() {
        this.appInstance = new AppInstance();
        this.baseAction = new BaseAction();
    }

    create(type) {
        this.baseAction.create("process", (plataforma) => {
            var path = process.cwd() + "/" + plataforma.app.name;
            shell.mkdir('-p', path + '/mapa', path + '/metadados', path + '/process');
            shell.touch(path + "/metadados/" + plataforma.app.name + ".yaml");
            shell.exec(`dotnet new solution -n ${plataforma.app.name} -o ${path}/process/`);
            let consoleAppName = plataforma.app.name + '.Process';
            shell.mkdir('-p', `${path}/process/${consoleAppName}`);
            shell.exec(`dotnet new console -n ${consoleAppName} -o ${path}/process/${consoleAppName}`);
            shell.exec(`dotnet new -i NUnit3.DotNetNew.Template`);
            let testProjectName = consoleAppName + '.Tests';
            shell.exec(`dotnet new nunit -n ${testProjectName} -o ${path}/process/${testProjectName}`);
            shell.exec(`dotnet sln ${path}/process/${plataforma.app.name}.sln add` + 
                ` ${path}/process/${consoleAppName}/${consoleAppName}.csproj ${path}/process/${testProjectName}/${testProjectName}.csproj`);
        })
    }
}