var unirest = require("unirest");

module.exports = class Deployer {

    constructor(context) {
        this.context = context;
    }

    uploadPublicKey(env, pk, solution, keyName) {
        return new Promise((resolve, reject) => {
            var url = `${this.context[env].url}/api/v1.0.0/publickey/${solution}/${keyName}`
            var req = unirest("POST", url);
            req.send(pk);

            req.end(function (res) {
                if (res.error) reject(new Error(res.error));
                resolve(res.body)
            });
        });
    }

    createSolution(env, solution) {
        return new Promise((resolve, reject) => {
            var url = `${this.context[env].url}/api/v1.0.0/solution`
            var req = unirest("POST", url);
            req.headers({
                "content-type": "application/json"
            });
            req.type("json");
            var body = {
                "name": solution.name,
                "version": solution.version,
                "id": solution.id,
                "description": solution.description
            }
            req.send(body);
            req.end(function (res) {
                if (res.error) reject(res.body);
                resolve(res.body);
            });
        });
    }

    createApp(env, app) {
        return new Promise((resolve, reject) => {
            var url = `${this.context[env].url}/api/v1.0.0/solution/${app.systemId}/create/app`;
            //var url = "https://pruu.herokuapp.com/dump/teste"
            var req = unirest("POST", url);
            req.headers({
                "content-type": "application/json"
            });

            req.type("json");
            req.send({
                "name": app.name,
                "version": app.version,
                "id": app.id,
                "description": app.description,
                "type": app.type
            });

            req.end(function (res) {
                if (res.error) reject(new Error(res.error));
                resolve(res.body);
            });

        });
    }
}