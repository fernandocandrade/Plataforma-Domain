var fs = require("fs");
var ncp = require("ncp").ncp;
var rimraf = require("rimraf");
var shell = require("shelljs");
var os = require("os");
ncp.limit = 16;
//var root = process.cwd()+"/";
var root = os.tmpdir() + "/";
var baseTemplate = __dirname+"/";
const uuidv4 = require('uuid/v4');
const template = "python-template";
module.exports = (function(){
    var self= {};



    /**
     *
     * @param {String} compiled
     * @param {String} domainAppRoot
     * @param {Function} callback
     * @description Este método monta o pacote do Domain.App que será
     * executado dentro do ambiente da plataforma, o domínio já foi compilado
     * para o formato Sequelize
     */
    self.generate = (env,compiled, domainAppRoot, callback)=>{
        var bundleFolder = uuidv4();
        var conf = env.conf;
        var instance = {};
        instance.docker = env.docker;

        if (fs.existsSync(domainAppRoot+"/plataforma.instance.lock")){
            instance = JSON.parse(fs.readFileSync(domainAppRoot+"/plataforma.instance.lock","UTF-8"));
            if (fs.existsSync(env.path)){
                shell.rm("-rf",env.path);
            }

        }
        shell.cp("-R",`${baseTemplate}python-template`,root+bundleFolder);
        fs.writeFileSync(`${root}${bundleFolder}/model/domain.py`,compiled);
        fs.unlinkSync(`${root}${bundleFolder}/model/domain.tmpl`);

        if(fs.existsSync(domainAppRoot+"Migrations/")){
            shell.cp("-R",domainAppRoot+"Migrations/",`${root}${bundleFolder}/`);
            shell.mv(`${root}${bundleFolder}/Migrations/`,`${root}${bundleFolder}/migrations`);
        }


        shell.cp("-R",domainAppRoot+"Mapas/",`${root}${bundleFolder}/`);
        shell.mv(`${root}${bundleFolder}/Mapas/`,`${root}${bundleFolder}/maps`);


        shell.cp(domainAppRoot+"/plataforma.json",`${root}${bundleFolder}/`);

        shell.mv(`${root}${bundleFolder}`,env.path);
        fs.writeFileSync(domainAppRoot+"/plataforma.instance.lock",JSON.stringify(instance,null,4));
        fs.writeFileSync(env.path+"/plataforma.instance.lock",JSON.stringify(instance,null,4));
        callback();
    };

    return self;
})();