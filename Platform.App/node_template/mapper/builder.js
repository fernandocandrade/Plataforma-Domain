/**
 *
 * Este arquivo e o ponto de construção do mapper
 * para construir as funcionalidades do mapper
 */
var MapLoader    = require("./load.js");
var MapIndex     = require("./index.js");
var MapTransform = require("./transform.js");
var MapTranslator = require("./translator.js");

var promise = new Promise((resolve,reject)=>{
    new MapLoader().getMaps().then((maps)=>{
        var index = new MapIndex(maps);
        var transform = new MapTransform(index);
        var translator = new MapTranslator(index,transform);
        var facade = {};
        facade.index = index;
        facade.transform = transform;
        facade.translator = translator;
        resolve(facade);
    });
});

module.exports = promise;