var fs = require("fs");
var ncp = require("ncp").ncp;
var rimraf = require("rimraf");
ncp.limit = 16;
module.exports = (function(){
    var self= {};

    self.generate = (compiled, root, callback)=>{
        if (fs.existsSync("bundle")){
            rimraf.sync("bundle",fs);    
        }
        fs.mkdirSync("bundle");
        fs.mkdirSync("bundle/maps");
        fs.mkdirSync("bundle/mapper");
        fs.mkdirSync("bundle/api");
        fs.mkdirSync("bundle/model");
        ncp("node_template", "bundle", function (err) {
            if (err) {
            return console.error(err);
            }
            fs.writeFileSync("bundle/model/domain.js",compiled);
            fs.unlinkSync("bundle/model/domain.tmpl");
            ncp(root+"Mapas","bundle/maps",()=>{
                ncp("./mapper","bundle/mapper",()=>{
                    ncp("./api","bundle/api",callback);
                });
            });
        });
        
    }

    return self;
})();