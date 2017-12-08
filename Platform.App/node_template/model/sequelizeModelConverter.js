var domain = require("./domain.js");

class SequelizeModelConverter{
    
    
    capitalizeFirstLetter(string) {
        return string.charAt(0).toUpperCase() + string.slice(1);
    }


    getAssociations(domainEntity){        
        var type = domainEntity._metadata.type;
        delete domainEntity._metadata;
        var includes = [];
        Object.keys(domainEntity).forEach(prop => {
            if (Array.isArray(domainEntity[prop])){                
                //inclui o padrao de associação entre entidades
                includes.push(type+"."+domainEntity[prop][0]._metadata.type)
                domainEntity[prop].forEach(s => { 
                    var r = this.getAssociations(s);
                    if (r.length > 0){
                        r.forEach(a => includes.push(a));
                    }
                });
                
            }
        });
        return includes; 
    }
}


module.exports = SequelizeModelConverter;