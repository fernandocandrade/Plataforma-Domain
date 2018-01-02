
var MapBuilder = require("../../mapper/builder.js");
var ChangeTrackPolicy = require("../../model/changeTrackPolicy.js");
var facade = new MapBuilder().build();
var domain = require("../../model/domain.js");

var mapperIndex = facade.index;
var mapper = facade.transform;
var translator = facade.translator;

/**
 * @class SaveCommandController
 * @description Classe responsável por persistir as entidades mapeadas no dominio
 */
class SaveCommandController{
    /**
     * @method persist
     * @param {Request} req Objeto de request do restify
     * @param {Response} res Objeto de response do restify
     * @param {Function} next  funcao callback para prosseguir com o fluxo http
     * @description Este é o controlador para a persistencia de dados no dominio
 * Os dados vão chegar baseado no mapa configurado, a aplicação vai converter para o
 * modelo de dominio, logo após aplicamos o change track para criar/atualizar/exluir entidades
     */
    persist(req,res,next){
        var entities = req.body;
                
        try {
            var domainEntities = entities.map(e => {
                var translatedEntity = translator.toDomain(req.params["appId"],e);
                translatedEntity.instance_id = req.instanceId;
                return translatedEntity;
            });
            
        } catch (error) {
            res.send(400,{message:error});
            console.log("------------------------------------");
            console.log("Error " + error);
            console.log("------------------------------------");
            return;
        }
        var track = new ChangeTrackPolicy(domainEntities);        
        var before = new Date().getTime();
        console.log("------------------------------------");
        track.apply(persisted =>{            
            var after = new Date().getTime();
            console.log("Tempo de execucao do change track")
            console.log((after - before)+" ms");
            var persistedMap = persisted.map(e => translator.toMap(req.params["appId"],e))
            var finalMap = persistedMap.map(final => mapper.applyRuntimeFields(req.params["appId"],final._metadata.type,[final]));
            res.send(finalMap);
            console.log("------------------------------------");
        },(err)=>{
            res.send(400,{message:err});
        });        
    }
}


module.exports  = SaveCommandController;