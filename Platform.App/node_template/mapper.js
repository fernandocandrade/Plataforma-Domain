var fs = require("fs");
var yaml = require('js-yaml');
const basePath = "../../Domain.App";
module.exports = (function(){
  var self = {};
  self.modelCache = {};
  self.projectionCache = {};
  self.functionsMap = {};

  self.getMapperByProcessId = (processId)=>{
    if (self.modelCache[processId]){
      return self.modelCache[processId];
    }
    var _map = yaml.safeLoad(fs.readFileSync(basePath+"/Mapas/"+processId+".yaml"));
    self.modelCache[processId] = _map;
    return _map;
  };

  self.getProjection = (processId)=>{
    if (self.projectionCache[processId]){
      return self.projectionCache[processId];
    }
    var _map = self.getMapperByProcessId(processId);
    self.projectionCache[processId] = {};
    var projections = self.projectionCache[processId];
    for(var mappedModel in _map){
      var entity = _map[mappedModel].model;
      projections[mappedModel] = {};
      projections[mappedModel].attributes = [];
      for(var field in _map[mappedModel].fields){
        var fieldObj = _map[mappedModel]["fields"][field];
        if (fieldObj.type && fieldObj.type === "function"){
          self.functionsMap[processId] = {}
          self.functionsMap[processId][mappedModel] = {};
          self.functionsMap[processId][mappedModel][field] = fieldObj;
          continue;//ignora campos calculados
        }
        var proj = [fieldObj.column,field];
        projections[mappedModel].attributes.push(proj);        
      }
    }
    return self.projectionCache[processId];    
  };
  
  self.applyFunctions = (processId,mapName,modelList)=>{    
    var accumulator = {};
    return modelList.map(model => {       
       if (self.functionsMap[processId] && self.functionsMap[processId][mapName]){          
          for(var calcProp in self.functionsMap[processId][mapName]){
            if (accumulator[calcProp] === undefined){
              accumulator[calcProp] = {};
            }
            var fn = eval(self.functionsMap[processId][mapName][calcProp].eval);
            model[calcProp] = fn(model,accumulator);
          }
        }
        return model;
    });    
  }

  self.getModelName = (processId,mapName)=>{    
    var _map = self.getMapperByProcessId(processId);
    return _map[mapName].model;
  }

  return self;
})();