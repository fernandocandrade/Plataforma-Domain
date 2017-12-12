class Transform {
    constructor(index){
        this.index = index;
    }

    replaceAll(from,needle,replacement){
        return from.split(needle).join(replacement);
    }

    replaceAllAtributes(from,needle,replacement){
        return this.replaceAll(from,"\""+needle+"\":","\""+replacement+"\":")
    }

    //Aplica os atributos calculados num resultado de consulta
    //do banco de dados
    applyRuntimeFields (processId,mapName,modelList) {    
        var accumulator = {};
        if (!this.index.hasFunctions(processId,mapName)){
            return modelList;
        }        
        return modelList.map(model => {
            var modelJson = model;
            if (typeof(model["toJSON"]) === "function"){
                modelJson = model.toJSON();
            }            
            modelJson._metadata = {};
            modelJson._metadata.type = mapName;            
            this.applyIncludeFields(modelJson,processId,mapName);
            this.applyFunctionFields(modelJson,processId,mapName,accumulator);            
            return modelJson;
        });
    }

    //Este metodo faz o map do nome do atributo de include
    //pois o sequelize não consegue aplicar um alias em runtime
    applyIncludeFields(modelJson, processId, mapName){
        var includes = this.index.getIncludes(processId,mapName);
        for (var include in includes){ 
          var modelApplied = this.index.getFields(processId,mapName)[include].model;
          var attrBase = this.index.getMapByAppIdAndName(processId,modelApplied).model;
          var keyToRename =  Object.keys(modelJson).find(s => s.indexOf(attrBase) >= 0);
          modelJson[include] = modelJson[keyToRename].map(c => {
            c._metadata = {};
            c._metadata.type = modelApplied;
            return c;
          });          
          delete modelJson[keyToRename];          
        }
    }

    //Este metodo aplica os campos calculados na lista resultante
    applyFunctionFields(modelJson,processId,mapName, accumulator){
        var functions = this.index.getFunctions(processId,mapName);
        for(var calcProp in functions){
            if (accumulator[calcProp] === undefined){
              accumulator[calcProp] = {};
            }
            var fn = eval(functions[calcProp].eval);
            modelJson[calcProp] = fn(modelJson,accumulator[calcProp]);
        }       
    }

    //Aplica os filtros do mapa no modelo de dominio
    getFilters(processId,mapName,request){
        var filters = this.index.getFilters(processId,mapName);
        if (!filters){
            return {};
        }
        var filter = filters[request.query["filter"]];
        if (!filter){
            return {};
        }
        var str = JSON.stringify(filter);
        Object.keys(request.query).forEach(r => str = this.replaceAll(str,":"+r,request.query[r]));
        var mapFields = this.index.getFields(processId,mapName);
        var fields = Object.keys(mapFields);
        fields.forEach(f => str = this.replaceAll(str,f,mapFields[f].column));
        return JSON.parse(str);        
    }

    getIncludes(processId,mapName,ormModel){        
        var includeMap = this.index.getIncludes(processId,mapName);
        var query = [];
        for(var includeProp in includeMap){
            var sqlObj = {};      
            var mappedAttr = includeMap[includeProp].model;
            var ormName = this.index.getMapByAppIdAndName(processId,mappedAttr).model;            
            sqlObj.model = ormModel[ormName];
            sqlObj.as = ormName; 
            sqlObj.attributes = this.index.getProjection(processId)[mappedAttr].attributes;
            query.push(sqlObj);
        }
        return query;          
    }

}

module.exports = Transform;