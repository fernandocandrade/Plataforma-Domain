/**
 * @description o server.js configura a API Rest da aplicação de domínio
 */
var domainPromise = require('../model/domain');

var serverPromise = new Promise(function(resolve,reject){
    domainPromise.then(domain =>{
        var restify = require('restify');
        var restifyCors = require('restify-cors-middleware');
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

        var cors = restifyCors({
            origins: ['*'], // defaults to ['*'] to allow all origins
            allowHeaders: ['Instance-Id'],
            exposeHeaders: ['API-Token-Expiry']
          });
        
        server.pre(cors.preflight)
        server.use(cors.actual)
    
        //Routing
        var query = new QueryController(domain);
        var command = new SaveCommandController(domain);
        server.get('/:appId/:entity', query.getEntityByAppId);
        server.post('/:appId/persist', command.persist);        
        resolve(server);        
    })
});
module.exports = serverPromise;