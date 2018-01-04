#!/usr/bin/env node
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
//var root = "../Domain.App/";
//var files = FileLoader.getFileNames(root)
var runAppAction    = new (require("./actions/runAppAction"));
var createAppAction = new (require("./actions/createAppAction"));
var deployAppAction = new (require("./actions/deployAppAction"));
var program = require('commander');

program
  .version('0.0.1')
  .option('-r, --run', 'Run local App')
  .option('-c, --create [type]', 'Creates a new App')
  .option('-d, --deploy [env]', 'Deploy App')
  .parse(process.argv);
if (program.run) runAppAction.exec();
if (program.create) createAppAction.exec(program.create);
if (program.deploy) deployAppAction.exec(program.deploy);

/**
 * 
 * Funcoes
 * 
 * Criar nova App
 *  - Criar a estrutura de pastas da aplicação
 * Rodar um App
 *  - Compila a aplicação e joga o bundle para uma pasta temporaria e roda de la
 * Deployar uma App
 *  - Compila a aplicação e joga dentro do ambiente da plataforma
 * 
 */



/*files.forEach((f)=>ModelBuilder.loadModel(FileLoader.readFile(f)))
//compilou o template para o modelo do Node com Sequelize
var compiled = ModelBuilder.compile();
Bundler.generate(compiled,root,()=>{
    console.log("done!");    
});*/

