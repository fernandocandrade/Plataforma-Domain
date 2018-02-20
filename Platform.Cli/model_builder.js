const Sequelize = require('sequelize');
var Handlebars = require('handlebars');
var root = __dirname + "/";
Handlebars.registerHelper("join", function (obj, sep, options) {
    return Object.keys(obj).map(function (item) {
        return options.fn(obj[item]);
    }).join(sep);
});

Handlebars.registerHelper("eq", function (lvalue, rvalue, options) {
    if (lvalue != rvalue) {
        return options.inverse(this);
    } else {
        return options.fn(this);
    }
});

Handlebars.registerHelper("lower", function (lvalue, options) {
    return lvalue.toLowerCase();
});

Handlebars.registerHelper("up_first", function (lvalue, options) {
    var ts = lvalue[0].toUpperCase();
    var tmp = ts + lvalue.toLowerCase().substring(1);
    return tmp;
});

var fs = require("fs");

module.exports = (function () {
    var self = {};
    self.model = {};
    self.model.tables = {};
    self.model.relationships = [];
    self.model.seeds = {};

    var keys = (model) => Object.keys(model)
    var hasValue = (array, value) => array.filter(v => v === value).length > 0;

    var isRelationship = (value) => ["hasMany", "belongsTo", "hasAndBelongsTo"].filter(v => v === value).length > 0;
    /**
     *
     * @param {JSON} model é o modelo definido no YAML no formato JSON
     * @description Este método carrega o modelo do YAML e verifica se ele já foi previamente
     * carregado e adiciona na estrutra de dados de modelos que serão compilados na aplicação de
     * dominio da plataforma
     */
    self.loadModel = function (model) {
        var name = keys(model)[0];
        if (self.model.tables[name]) {
            throw "model " + name + " already defined";
        }
        self.model.tables[name] = {};
        self.model.tables[name].columns = [];

        var _model = self.model.tables[name];
        _model.tableName = name; //by default
        _model.columns = [];
        var columns = keys(model[name]);
        columns.forEach(column => {
            if (isRelationship(column)) {
                self.model.relationships.push([name, column, model[name][column][0]]);
                return;
            }
            var modelColumn = {};
            modelColumn.name = column;
            var attrs = model[name][column];
            modelColumn.attributes = attrs;
            self.model.tables[name].columns.push(modelColumn);
        });
    };

    /**
     * @description Compila o modelo de dados declarados no YAML
     * para JavaScript/Sequelize através de um template definido
     * dentro da pasta Platform.App/python-template/model/domain.tmpl
     */
    self.compile = (appName) => {
        var tables = keys(self.model.tables);
        tables.forEach(t => {
            self.compileTable(self.model.tables[t]);
        });

        var source = fs.readFileSync(root + "python-template/model/domain.tmpl").toString();
        var template = Handlebars.compile(source);
        var obj = { "database_name": appName, "model": self.sequelizeModel, "relations": self.model.relationships };
        console.log(JSON.stringify(obj,null,4));
        var compiled = template(obj);
        return compiled;
    };

    /**
     *
     * @param {JSON} obj modelo de dominio na estrutura de dados pre compilacao
     * @param {Array<String>} array lista de atributos do dominio
     * @description Define o tipo da coluna já no formato do Sequelize
     */
    var defineType = (obj, array) => array.forEach(v => {
        if (self.seqTypeMap[v]) {
            obj.type = self.seqTypeMap[v];
            return false;
        }
    });

    self.seqTypeMap = {
        "string": "String",
        "integer": "Integer",
        "char": "Char",
        "text": "Text",
        "bigint": "BigInt",
        "float": "Float",
        "real": "Real",
        "double": "Double",
        "decimal": "Decimal",
        "boolean": "Boolean",
        "time": "Time",
        "date": "Date",
        "datetime": "DateTime",
        "hstore": "HsStore",
        "json": "Json",
        "jsonb": "Jsonb",
        "blob": "Blob",
        "uuid": "sap.UUID(as_uuid\=True)",
        "uuidV1": "UUIDV1",
        "uuidV4": "UUIDV4"
    };

    self.sequelizeModel = {};

    /**
     *
     * @param {JSON} table estrutura pre compilacao
     * @description compila um objeto de dominio para ja considerando
     * detalhes de chave ou atributos
     */
    self.compileTable = (table) => {
        var tableDefinition = {};
        console.log(`Processing ${table.tableName}`);

        table.columns.forEach(c => {
            tableDefinition[c.name] = {};
            tableDefinition[c.name].name = c.name;
            if (!Array.isArray(c.attributes)) {
                throw `Syntax error in file ${table.tableName} near to field ${c.name} attribute ${c.attributes}`;
            }
            defineType(tableDefinition[c.name], c.attributes);
            if (hasValue(c.attributes, "primary key")) {
                tableDefinition[c.name].primaryKey = true;
            }
            if (hasValue(c.attributes, "auto increment")) {
                tableDefinition[c.name].autoIncrement = true;
            }
        });
        self.sequelizeModel[table.tableName] = tableDefinition;
    };
    return self;
})();