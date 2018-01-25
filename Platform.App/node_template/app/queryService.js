
class QueryService{

    constructor(){}

    filter(appId, mappedEntity, entity, projection, validityPolicy){        
        return new Promise(
            (resolve, reject) => {

                validityPolicy.setQueryContext(appId,mappedEntity,entity);
                validityPolicy.query(
                    projection, 
                    (result)=>{
                        resolve(result);
                    }, 
                    (e)=>{
                        reject(e);
                    }
                );
            }
        );
    }
    
}

module.exports = QueryService;