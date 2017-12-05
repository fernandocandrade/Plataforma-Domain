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
        ncp("node_template", "bundle", function (err) {
            if (err) {
            return console.error(err);
            }
            fs.writeFileSync("bundle/app.js",compiled);
            fs.unlinkSync("bundle/app.tmpl");            
            ncp(root+"Mapas","bundle/maps",callback);
        });
        
    }

    return self;
})();