
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
        track.apply(s =>{
            res.send(s);
        });
        
    }
}


module.exports  = SaveCommandController;