var FileLoader = require("../../file_loader.js");
var ModelBuilder = require("../../model_builder.js");
var Bundler = require("../../bundler.js");


module.exports = class BuildDomainAppAction{

    build(config,callback){
        var root = process.cwd()+"/";
        var files = FileLoader.getFileNames(root)
        files.forEach((f)=>ModelBuilder.loadModel(FileLoader.readFile(f)))
        //compilou o template para o modelo do Node com Sequelize
        var compiled = ModelBuilder.compile(config.app.name);
        Bundler.generate(compiled,root,()=>{
            callback();  
        });
    }
}