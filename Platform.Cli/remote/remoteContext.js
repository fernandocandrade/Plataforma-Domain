var fs = require("fs");
var shell = require("shelljs");
const homedir = require('os').homedir();
const basePath = `${homedir}/.plataforma`;
const path = `${basePath}/remote.json`;
module.exports = class RemoteContext {

    constructor() {
        this.production = {};
        this.user = {};
        this.enabled = false;
        if (fs.existsSync(path)) {
            var str = fs.readFileSync(path).toString();
            var obj = JSON.parse(str);
            Object.assign(this, obj);
        }
    }
    persist() {
        if (!fs.existsSync(basePath)) {
            shell.mkdir(basePath);
        }
        fs.writeFileSync(path, JSON.stringify(this, null, 4));
    }
}