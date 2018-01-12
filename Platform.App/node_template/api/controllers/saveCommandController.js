var ChangeTrackPolicy = require("../../model/changeTrackPolicy.js");
var ArrayUtils = require("../../utils/array");
/**
 * @class SaveCommandController
 * @description Classe responsável por persistir as entidades mapeadas no dominio
 */
class SaveCommandController{

    constructor (domain, mapperFacade){
        this.domain = domain;
        this.mapper = mapperFacade.transform;
        this.translator = mapperFacade.translator;
        this.mapperIndex = mapperFacade.index;
    }
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
                var translatedEntity = this.translator.toDomain(req.params["appId"],e);
                translatedEntity.meta_instance_id = req.instanceId;
                return translatedEntity;
            });
            var track = new ChangeTrackPolicy(domainEntities, req.validityPolicy);
            var before = new Date().getTime();
            console.log("------------------------------------");
            var arrayU = new ArrayUtils();
            track.apply(persisted =>{
                var after = new Date().getTime();
                console.log("Tempo de execucao do change track")
                console.log((after - before)+" ms");
                var persistedMap = persisted.map(e => this.translator.toMap(req.params["appId"],e))
                var finalMap = persistedMap.map(final => this.mapper.applyRuntimeFields(req.params["appId"],final._metadata.type,[final]));
                res.send(arrayU.flatMap(finalMap));
                console.log("------------------------------------");
            },(err)=>{
                res.send(400,{message:err.toString()});
            });
        } catch (error) {
            res.send(400,{message:error.toString()});
            console.log("------------------------------------");
            console.log("Error " + error);
            console.log("------------------------------------");
            return;
        }

    }
}


module.exports  = SaveCommandController;