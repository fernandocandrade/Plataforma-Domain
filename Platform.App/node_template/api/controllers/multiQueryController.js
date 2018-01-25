var QueryService = require("../../app/queryService");

class MultiQueryController {

    constructor(domain, mapperFacade){ 
        this.queryService = new QueryService();
        this.domain = domain;
        this.mapper = mapperFacade.transform;
        this.mapperIndex = mapperFacade.index; 
    }

    /**
     * @method getEntityByAppId
     * @param {Request} req Objeto de request od restify
     * @param {Response} res Objeto de response do Restify
     * @description Busca uma entidade de dominio mapeada
     * Para isso nós fazemos as transformações do modelo mapeado para o modelo de dominio
     */    
    getEntityByAppId(req,res,next) {
        console.log("MultiQueryController:getEntityByAppId");
        this.retrieve_all(req, res);
/*         this.retrieve_one(req.params.appId, req.body[0], req.validityPolicy)
        .then((resposta) => {
            res.send(resposta)
        }).
        catch((error) => {
            console.log("erro =", error);
            res.send(400,{message:error});    
        }); */
    }



    retrieve_all(req,res){

        var appId = req.params.appId;

        var filters = req.body;
        var validityPolicy = req.validityPolicy;

        var promises = [];
        filters.forEach(filter => {
                var p = this.retrieve_one(appId, 
                                        filter,
                                        validityPolicy);
                console.log("promise =", p);
                promises.push(p);
            }
        )
        console.log("promises =", promises);
        Promise.all(promises).
            then((resposta) => {
                res.send(resposta)
            }).
            catch((error) => {
                console.log("erro =", error);
                res.send(400,{message:error});    
            });
    }   


    retrieve_one(appId, filter, validityPolicy){

        console.log("appId =", appId);
        console.log("filter =", filter);

        var mappedEntity = filter.entity;
        var ent = this.mapperIndex.getModelName(appId,mappedEntity);
        var projection = this.mapperIndex.getProjection(appId,mappedEntity)[mappedEntity];
        projection.include = this.mapper.getIncludes(appId,mappedEntity,this.domain);
        if (projection.include.length == 0){
            delete projection.include;
        }

        console.log("buscar: ", 
        "query =", filter,
        ", appId =", appId, 
        ", mappedEntity = ", mappedEntity, 
        ", ent =", ent,
        ", projection.include = ", projection.include); 
        
        projection.where = this.mapper.getFilters1(appId,mappedEntity,filter);                
        if (Object.keys(projection.where).length === 0){
            delete projection.where;
        }

        return this.queryService.filter(appId, mappedEntity, ent, projection, validityPolicy);

/*         this.queryService.filter(appId, mappedEntity, ent, projection, validityPolicy).
        then( 
            (ok) => {
                console.log("result =", ok);
                res.send(ok);                              
            }
        )
        .catch( 
            (error) => {
                console.log("erro =", error);
                res.send(400,{message:error});    
            }
        );                
 */    }    
        

  
}

module.exports = MultiQueryController



    