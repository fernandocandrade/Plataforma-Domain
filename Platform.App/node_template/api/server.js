var restify = require('restify');
var QueryController = require('./queryController.js');
var SaveCommandController = require('./saveCommandController.js');
var server = restify.createServer();
server.use(restify.plugins.queryParser());
server.use(restify.plugins.bodyParser());
var query = new QueryController();
var command = new SaveCommandController();
server.get('/:appId/:entity', query.getEntityByAppId);
server.post('/:appId/persist', command.persist);

server.listen(9090, function() {
    console.log('%s listening at %s', server.name, server.url);
});