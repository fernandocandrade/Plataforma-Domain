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
    self.generate = (compiled, domainAppRoot, callback)=>{                
        var id = "plataforma_"+uuidv4();
        var instance = {};
        instance.id = id;
        instance.port = 9092;
        if (fs.existsSync(domainAppRoot+"/plataforma.instance.lock")){
            instance = JSON.parse(fs.readFileSync(domainAppRoot+"/plataforma.instance.lock","UTF-8"));
            shell.rm("-rf",root+instance.id);
        }
        shell.cp("-R",baseTemplate+"node_template",root+"bundle");        
        fs.writeFileSync(root+"bundle/model/domain.js",compiled);
        fs.unlinkSync(root+"bundle/model/domain.tmpl");
        
        shell.cp("-R",domainAppRoot+"Migrations/",root+"bundle/");
        shell.mv(root+"bundle/Migrations/",root+"bundle/migrations");

        shell.cp("-R",domainAppRoot+"Mapas/",root+"bundle/");
        shell.mv(root+"bundle/Mapas/",root+"bundle/maps");


        shell.cp(domainAppRoot+"/plataforma.json",root+"bundle/");
        
        shell.mv(root+"bundle",root+instance.id)
        
        fs.writeFileSync(domainAppRoot+"/plataforma.instance.lock",JSON.stringify(instance,null,4));
        fs.writeFileSync(root+"/"+instance.id+"/plataforma.instance.lock",JSON.stringify(instance,null,4));
        callback(instance.id);
    }

    return self;
})();