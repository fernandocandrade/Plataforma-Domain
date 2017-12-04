var fs = require('fs');
var yaml = require('js-yaml');
module.exports = (function(){
    var self = {};
    self.getFileNames = function(path){
        self.root = path;
        var filesToLoad = [];
        fs.readdirSync(path).forEach(file => {
            if(file.endsWith(".yaml")){
                filesToLoad.push(file);
            }            
        }) 
        return filesToLoad;
    }

    self.readFile = function(fileName){
        return yaml.safeLoad(fs.readFileSync(self.root +fileName));
    };
    return self;
})();