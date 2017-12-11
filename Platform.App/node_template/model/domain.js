
//Temporario vou remover do git este arquivo


const Sequelize = require('sequelize');

const sequelize = new Sequelize('app', 'postgres', '', {
  host: 'localhost',
  dialect: 'postgres',
  pool: {
    max: 5,
    min: 0,
    acquire: 30000,
    idle: 10000
  },
  logging: true,
  operatorsAliases: true
  
});

var model = {};

//Declaring models with Sequelize
model["tb_account"] = sequelize.define('tb_account', {
    id: { type: Sequelize.INTEGER , primaryKey: true, autoIncrement: true   } ,    vl_balance: { type: Sequelize.INTEGER  } 
    
},{
    timestamps: true,
    freezeTableName: true,
    paranoid:true
});

model["tb_client"] = sequelize.define('tb_client', {
    id: { type: Sequelize.INTEGER , primaryKey: true, autoIncrement: true   } ,    nm_client: { type: Sequelize.STRING  } ,    cpf: { type: Sequelize.STRING  } ,    lst_name: { type: Sequelize.STRING  } 
    
},{
    timestamps: true,
    freezeTableName: true,
    paranoid:true
});

model["tb_operation"] = sequelize.define('tb_operation', {
    acc_origin: { type: Sequelize.INTEGER , primaryKey: true } ,    acc_dest: { type: Sequelize.INTEGER , primaryKey: true } ,    tp_operation: { type: Sequelize.STRING  } 
    
},{
    timestamps: true,
    freezeTableName: true,
    paranoid:true
});


//Declaring relationship between models

var associations = {};

associations["tb_account.tb_client"] = model["tb_account"].belongsTo(model["tb_client"],{as: 'tb_client'});
associations["tb_client.tb_account"] = model["tb_client"].hasMany(model["tb_account"],{as: 'tb_account'});

model["associations"] = associations;

//Sincronize database
sequelize.sync();


module.exports = model;