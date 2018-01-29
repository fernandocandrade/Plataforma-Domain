const Sequelize = require('sequelize');
const _sequelize = new Sequelize("postgres", "postgres", "", {
    host: "localhost",
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
var database = "bitemporal_test";
function getModel(sequelize) {
    return new Promise((resolve, reject) => {
        model.Person = sequelize.define('Person', {
            rid: { type: Sequelize.UUID, primaryKey: true, defaultValue: Sequelize.UUIDV4 },
            id: { type: Sequelize.STRING },
            name: { type: Sequelize.STRING },
            validity_begin: { type: Sequelize.DATE, defaultValue: Sequelize.NOW },
            validity_end: { type: Sequelize.DATE, defaultValue: new Date("9999-12-31") },
            transaction_start: { type: Sequelize.DATE, defaultValue: Sequelize.NOW },
            transaction_stop: { type: Sequelize.DATE, defaultValue: new Date("9999-12-31") }
        },
            {
                timestamps: false,
                freezeTableName: true,
                scopes: {
                    validity: function (reference) {
                        return {
                            where: {
                                validity_begin: {
                                    $lte: reference
                                },
                                validity_end: {
                                    $gt: reference
                                },
                                transaction_stop: new Date("9999-12-31")
                            }
                        };
                    }
                }
            });
        sequelize.sync().then(() => {
            resolve(model);
        });
    });
}

function createDatabase() {
    return new Promise((r, rj) => {
        _sequelize.query(`CREATE DATABASE "${database}";`).then(() => {
            var sequelize = new Sequelize(database, "postgres", "", {
                host: "localhost",
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
            r(sequelize);
        }).catch(rj);

    });

}

function dropDatabase() {
    return _sequelize.query(`DROP DATABASE "${database}";`)
}

function close() {
    sequelize.close();
}

module.exports = {
    getModel: getModel,
    createDatabase: createDatabase,
    dropDatabase: dropDatabase,
    close: close
};