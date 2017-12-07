String.prototype.replaceAll = String.prototype.replaceAll || function(needle, replacement) {
    return this.split(needle).join(replacement);
};

class Transform {
    constructor(index){
        this.index = index;
    }
    //Aplica os atributos calculados num resultado de consulta
    //do banco de dados
    applyRuntimeFields (processId,mapName,modelList) {    
        var accumulator = {};
        if (!this.index.hasFunctions(processId,mapName)){
            return modelList;
        }        
        return modelList.map(model => {              
            var modelJson = model.toJSON();
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
          var modelApplied = self.modelCache[processId][mapName]["fields"][include].model;
          var attrBase = self.modelCache[processId][modelApplied].model;
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
        for(var calcProp in self.functionsMap[processId][mapName]){
            if (accumulator[calcProp] === undefined){
              accumulator[calcProp] = {};
            }
            var fn = eval(self.functionsMap[processId][mapName][calcProp].eval);            
            modelJson[calcProp] = fn(modelJson,accumulator[calcProp]);
        }       
    }

    
    getFilters(processId,mapName,request){
        var filters = this.index.getFilters(processId,mapName);
        var filter = filters[request.query["filter"]];
        var str = JSON.stringify(filter);
        Object.keys(request.query).forEach(r => str = str.replaceAll(":"+r,request.query[r]));    
        var fields = Object.keys(filters);
        fields.forEach(f => str = str.replaceAll(f,this.index.getMapByAppIdAndName(processId,mapName)["fields"][f].column));
        return JSON.parse(str);        
    }

}

module.exports = Transform;