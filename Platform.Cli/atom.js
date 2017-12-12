/**
 * A aplicacao principal carrega os módulos;
 * Lista todos os arquivos YAML que foram criados para o usuário
 * Monta o modelo de dominio em memoria
 * Converte o modelo para Sequelize
 * Gera o pacote de aplicacao através do Bundler
 * 
 */
var FileLoader = require("./file_loader.js");
var ModelBuilder = require("./model_builder.js");
var Bundler = require("./bundler.js");
var root = "../Domain.App/";
var files = FileLoader.getFileNames(root)




files.forEach((f)=>ModelBuilder.loadModel(FileLoader.readFile(f)))
//compilou o template para o modelo do Node com Sequelize
var compiled = ModelBuilder.compile();
Bundler.generate(compiled,root,()=>{
    console.log("done!");    
});

