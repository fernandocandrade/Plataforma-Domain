var fs = require("fs");
var ncp = require("ncp").ncp;
var rimraf = require("rimraf");
ncp.limit = 16;
var root = "../Platform.App/"
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
            rimraf.sync(root+"bundle",fs);    
        }
        fs.mkdirSync(root+"bundle");
        fs.mkdirSync(root+"bundle/migrations");
        fs.mkdirSync(root+"bundle/maps");
        fs.mkdirSync(root+"bundle/mapper");
        fs.mkdirSync(root+"bundle/api");
        fs.mkdirSync(root+"bundle/model");
        ncp(root+"node_template", root+"bundle", function (err) {
            if (err) {
            return console.error(err);
            }
            fs.writeFileSync(root+"bundle/model/domain.js",compiled);
            fs.unlinkSync(root+"bundle/model/domain.tmpl");
            ncp(domainAppRoot+"Mapas",root+"bundle/maps",()=>{
                ncp(root+"node_template/mapper",root+"bundle/mapper",()=>{
                    ncp(root +"node_template/api",root+"bundle/api",()=>{
                        ncp(domainAppRoot+"Migrations",root+"bundle/migrations",callback);
                    });
                });
            });
        });
        
    }

    return self;
})();