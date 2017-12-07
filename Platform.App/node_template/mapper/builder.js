/**
 * 
 * Este arquivo e o ponto de construção do mapper
 * para construir as funcionalidades do mapper
 */
var MapLoader    = require("./load.js");
var MapIndex     = require("./index.js");
var MapTransform = require("./transform.js");

class Builder{
     build (){        
        var maps = new MapLoader().getMaps();
        var index = new MapIndex(maps);
        
        var transform = new MapTransform(index);

        var facade = {};
        facade.index = index;
        facade.transform = transform;
        return facade;
     }
}

module.exports = Builder;