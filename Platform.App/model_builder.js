const Sequelize = require('sequelize');
var Handlebars = require('handlebars');

Handlebars.registerHelper( "join", function( obj, sep, options ) {
    
    return Object.keys(obj).map(function( item ) {        
        return options.fn( obj[item] );
    }).join( sep );
});

var fs = require("fs");
const sequelize = new Sequelize('app', 'postgres', 'example', {
    host: 'localhost',
    dialect: 'postgres',
    pool: {
      max: 5,
      min: 0,
      acquire: 30000,
      idle: 10000
    },
    operatorsAliases: false
  });

module.exports = (function(){
    var self = {};
    self.model = {};
    self.model.tables = {};
    self.model.relationships = [];
    self.model.seeds = {};

    var keys = (model) => Object.keys(model)    
    var hasValue = (array,value) => array.filter(v => v === value).length > 0;

    var isRelationship = (value) => ["hasMany","belongsTo","hasAndBelongsTo"].filter(v => v === value).length > 0;

    self.loadModel = function(model){
        var name = keys(model)[0];
        if (self.model.tables[name]){
            throw "model " + name + " already defined";
        }
        self.model.tables[name] = {};
        self.model.tables[name].columns = [];
        
        var _model = self.model.tables[name];
        _model.tableName = name; //by default
        _model.columns = [];
        var columns = keys(model[name]);
        columns.forEach(column => {
            if (isRelationship(column)){
                self.model.relationships.push([name,column,model[name][column][0]]);
                return;
            }            
            var modelColumn = {};
            modelColumn.name = column;
            var attrs = model[name][column];
            modelColumn.attributes = attrs;
            self.model.tables[name].columns.push(modelColumn);            
        });        
    };

    self.compile = ()=>{
        var tables = keys(self.model.tables);
        tables.forEach(t => {
            self.compileTable(self.model.tables[t]);
        });

        var source = fs.readFileSync("node_template/app.tmpl").toString();
        var template = Handlebars.compile(source);
        var obj = { "model":self.sequelizeModel, "relations":self.model.relationships};        
        var compiled = template(obj);
        return compiled;
    };

    var defineType = (obj,array) => array.forEach(v => {
        if (self.seqTypeMap[v]){
            obj.type = self.seqTypeMap[v];
            return false;
        }
    });

    self.seqTypeMap = {
        "string":"Sequelize.STRING",
        "integer":"Sequelize.INTEGER",
        "char":"Sequelize.CHAR",
        "text":"Sequelize.TEXT",
        "bigint":"Sequelize.BIGINT",
        "float":"Sequelize.FLOAT",
        "real":"Sequelize.REAL",
        "double":"Sequelize.DOUBLE",
        "decimal":"Sequelize.DECIMAL",
        "boolean":"Sequelize.BOOLEAN",
        "time":"Sequelize.TIME",
        "date":"Sequelize.DATE",
        "hstore":"Sequelize.HSTORE",
        "json":"Sequelize.JSON",
        "jsonb":"Sequelize.JSONB",
        "blob":"Sequelize.BLOB",
        "uuid":"Sequelize.UUID",
        "uuidV1":"Sequelize.UUIDV1",
        "uuidV4":"Sequelize.UUIDV4"
    };
    
    self.sequelizeModel = {};
    
    self.compileTable = (table)=>{        
        var tableDefinition = {};              
        table.columns.forEach(c => {
            tableDefinition[c.name] = {};
            tableDefinition[c.name].name = c.name;
            defineType(tableDefinition[c.name],c.attributes);
            if (hasValue(c.attributes,"primary key")){
                tableDefinition[c.name].primaryKey = true;
            }
            if (hasValue(c.attributes,"auto increment")){
                tableDefinition[c.name].autoIncrement = true;
            }            
        });  
        self.sequelizeModel[table.tableName] = tableDefinition;      
    };
    return self;
})();