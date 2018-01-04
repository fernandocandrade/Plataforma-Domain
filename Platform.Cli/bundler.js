var fs = require("fs");
var ncp = require("ncp").ncp;
var rimraf = require("rimraf");
var shell = require("shelljs");
var os = require("os");
ncp.limit = 16;
//var root = process.cwd()+"/";
var root = os.tmpdir() + "/";
var baseTemplate = __dirname+"/";
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
        if (fs.existsSync(root+"bundle")){
            shell.rm("-rf",root+"bundle");
            //rimraf.sync(root+"bundle",fs);    
        }
        shell.cp("-R",baseTemplate+"node_template",root+"bundle");        
        fs.writeFileSync(root+"bundle/model/domain.js",compiled);
        fs.unlinkSync(root+"bundle/model/domain.tmpl");
        
        shell.cp("-R",domainAppRoot+"Migrations/",root+"bundle/");
        shell.mv(root+"bundle/Migrations/",root+"bundle/migrations");

        shell.cp("-R",domainAppRoot+"Mapas/",root+"bundle/");
        shell.mv(root+"bundle/Mapas/",root+"bundle/maps");


        shell.cp(domainAppRoot+"/plataforma.json",root+"bundle/");
        callback();
    }

    return self;
})();