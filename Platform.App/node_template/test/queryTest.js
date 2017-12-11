var ValidityPolicy = require("../model/validityPolicy");
var domain = require('../model/domain');


domain["tb_client"].findAll().then(r => console.log(r));
