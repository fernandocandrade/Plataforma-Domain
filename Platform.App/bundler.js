var fs = require("fs");
var ncp = require("ncp").ncp;
var rimraf = require("rimraf");
ncp.limit = 16;
module.exports = (function(){
    var self= {};

    self.generate = (compiled, callback)=>{
        if (fs.existsSync("bundle")){
            rimraf.sync("bundle",fs);    
        }
        fs.mkdirSync("bundle");
        ncp("node_template", "bundle", function (err) {
            if (err) {
            return console.error(err);
            }
            fs.writeFileSync("bundle/app.js",compiled);
            fs.unlinkSync("bundle/app.tmpl");
            callback();
        });
        
    }

    return self;
})();