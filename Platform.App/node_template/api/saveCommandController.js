
var MapBuilder = require("../mapper/builder.js");
var ChangeTrackPolicy = require("../model/changeTrackPolicy.js");
var facade = new MapBuilder().build();
var domain = require("../model/domain.js")

var mapperIndex = facade.index;
var mapper = facade.transform;
var translator = facade.translator;

class SaveCommandController{
    persist(req,res,next){
        var entities = req.body;        
        var domainEntities = entities.map(e => translator.toDomain(req.params["appId"],e));        
        var track = new ChangeTrackPolicy(domainEntities);        
        var before = new Date().getTime();
        console.log("------------------------------------");
        track.apply(s =>{            
            var after = new Date().getTime();
            console.log("Tempo de execucao do change track")
            console.log((after - before)+" ms");
            res.send("dados salvos");
            console.log("------------------------------------");
        });        
    }
}


module.exports  = SaveCommandController;