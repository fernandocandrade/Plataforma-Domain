var shell = require("shelljs");

module.exports = class AddRemoteToGit {
    constructor() {

    }

    exec(context) {
        return new Promise((resolve, reject)=>{
            shell.exec(`git remote rm plataforma`);
            var out = shell.exec(`git remote add plataforma ${context.gitRemote}`);
            if (out.code != 0) {
                reject(new Error(out.stdout));
            }else{
                resolve(context);
            }
        });
    }
}