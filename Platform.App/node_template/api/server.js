var restify = require('restify');
var QueryController = require('./queryController.js');
var server = restify.createServer();
server.use(restify.plugins.queryParser());
server.use(restify.plugins.bodyParser());
var query = new QueryController();

server.get('/:appId/:entity', query.getEntityByAppId);

server.listen(9090, function() {
    console.log('%s listening at %s', server.name, server.url);
});