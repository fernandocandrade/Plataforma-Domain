/**
 * @description o server.js é o ponto de entrada para a aplicação de dominio
 * ele configura o restfiy e as rotas, faz a associação das rotas com os controladores
 * e sobe o servidor http
 */


var restify = require('restify');
var QueryController = require('./controllers/queryController');
var SaveCommandController = require('./controllers/saveCommandController');
var RequireInstanceIdMiddleware = require('./middlewares/requireInstanceId');
var ConfigureValidityPolicyMiddleware = require('./middlewares/configureValidityPolicy');

var server = restify.createServer();
//Configure
server.use(restify.plugins.queryParser());
server.use(restify.plugins.bodyParser());

//Middlewares
server.use(RequireInstanceIdMiddleware);
server.use(ConfigureValidityPolicyMiddleware);

//Routing
var query = new QueryController();
var command = new SaveCommandController();
server.get('/:appId/:entity', query.getEntityByAppId);
server.post('/:appId/persist', command.persist);


server.listen(9090, function() {
    console.log('%s listening at %s', server.name, server.url);
});