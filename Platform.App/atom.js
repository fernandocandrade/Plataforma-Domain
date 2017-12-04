var FileLoader = require("./file_loader.js");
var ModelBuilder = require("./model_builder.js");
var Bundler = require("./bundler.js");
var root = "../Domain.App"
var files = FileLoader.getFileNames(root)

files.forEach((f)=>ModelBuilder.loadModel(FileLoader.readFile(f)))
//compilou o template para o modelo do Node com Sequelize
var compiled = ModelBuilder.compile();
Bundler.generate(compiled,()=>{
    console.log("done!");
});

