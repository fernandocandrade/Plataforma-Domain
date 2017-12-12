class Translator {
    
    constructor(index, transform){
        this.index = index;
        this.transform = transform;   
    }
    
    toDomain(processId, mapped){        
        var mapType = mapped._metadata.type;
        var map = this.index.getMapByAppIdAndName(processId,mapType);
        var translated = {};
        translated._metadata = mapped._metadata;
        translated._metadata.type = map.model;
        var list = this.index.columnsFromMapType(processId,mapType);      
        list.forEach(replacement => {
            var from = replacement[0];
            var to = replacement[1];                                    
            if (mapped[from]){                                
                if (typeof(mapped[from]) !== "object"){                    
                    translated[to] = mapped[from];
                }else if (Array.isArray(mapped[from])){                                        
                    translated[to] = mapped[from].map(m => this.toDomain(processId,m));                    
                }else if(typeof(mapped[from])==="object"){
                    translated[to] = this.toDomain(processId,mapped[from]);
                }
            }            
        });
        return translated;
    }

    toMap(processId, mapped){                
        var mapType = this.index.getMapTypeByDomainType(processId,mapped._metadata.type);
        var map = this.index.getMapByAppIdAndName(processId,mapType);
        var translated = {};
        translated._metadata = {};
        translated._metadata.type = mapType;
        var list = this.index.columnsFromMapType(processId,mapType);      
        list.forEach(replacement => {
            var from = replacement[1];
            var to = replacement[0];                                    
            if (mapped[from]){                                
                if (typeof(mapped[from]) !== "object"){                    
                    translated[to] = mapped[from];
                }else if (Array.isArray(mapped[from])){                                        
                    translated[to] = mapped[from].map(m => this.toMap(processId,m));                    
                }else if(typeof(mapped[from])==="object"){
                    translated[to] = this.toMap(processId,mapped[from]);
                }
            }            
        });
        return translated;
    }
}

module.exports = Translator;