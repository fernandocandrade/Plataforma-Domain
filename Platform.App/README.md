# Platform.App

#### Introdução
Este é o módulo executor da aplicação de domínio, todo o modelo de domínio foi convertido para a linguagem do ORM do template definido, no caso o NodeJS, bem como o mapa de domínio.
Esta aplicação sobe um servidor http e expõe alguns serviços rest para consulta e persistência de dados no domínio

#### Requisitos

* NodeJS
* Npm


### Conexão com o banco de dados
A string de conexão com o banco de dados pode ser configurada no [template do domínio](https://github.com/ONSBR/Plataforma-Domain/blob/master/Platform.App/node_template/model/domain.tmpl) por padrão as configurações do banco são:
* banco de dados -> 'app'
* usuario -> 'postgres'
* senha -> ''
* host -> 'localhost'

Caso queira mudar as configurações de conexão você deve modificar o seguinte trecho de código:

```js
const sequelize = new Sequelize('<nome do banco>', '<usuario>', '<senha>', {
  host: '<host>',
  dialect: 'postgres',
  pool: {
    max: 5,
    min: 0,
    acquire: 30000,
    idle: 10000
  },
  logging: false,
  operatorsAliases: true
  
});
```

### Executando a aplicação de domínio

Após o processo de compilação da aplicação você deve entrar dentro da pasta "bundle"

```sh
$ cd bundle/api
```

Antes de executar a aplicação é necessário instalar todas as dependências necessárias para a execução do projeto.
Para isso você deve executar o seguinte comando:

```sh
$ npm install
```

Para executar a aplicação, apontando para a aplicação Domain.App você deve executar o seguinte comando:
```sh
$ node server.js
```

Ao subir a aplicação o Sequelize irá sincronizar automaticamente com o banco de dados, criando as respectivas tabelas de dominio.

### API de Domínio

#### Rotas

```
GET http://localhost:9090/:processId/:nomeEntidadeMapeada
GET http://localhost:9090/:processId/:nomeEntidadeMapeada?filter=:nomeFiltro&:nomeParametro=<valor>
POST http://localhost:9090/:processId/persist
```

#### Collection Link

Collection link https://www.getpostman.com/collections/41416eeff8dd00ed8eb1

#### Exemplos

Exemplo para a criação de um registro da entidade cliente.

```http
POST /app1/persist HTTP/1.1
Host: localhost:9090
Content-Type: application/json

[
    {
        "nome": "Elvis",
        "sobrenome": "Presley",
        "_metadata": {
            "type": "cliente",
            "changeTrack":"create"
        }
    }
]
```

Exemplo para a alteração de um registro da entidade cliente.

```http
POST /app1/persist HTTP/1.1
Host: localhost:9090
Content-Type: application/json

[
    {
        "nome": "Elvis",
        "sobrenome": "Presley Jr",
        "id": "6233f23f-d5a1-4183-a6ba-37875a83150a",
        "_metadata": {
            "type": "cliente",
            "changeTrack":"update"
        }
    }
]
```

Exemplo para a exclusão de um registro da entidade cliente.

```http
POST /app1/persist HTTP/1.1
Host: localhost:9090
Content-Type: application/json

[
    {
        "nome": "Elvis",
        "sobrenome": "Presley Jr",
        "id": "6233f23f-d5a1-4183-a6ba-37875a83150a",
        "_metadata": {
            "type": "cliente",
            "changeTrack":"destroy"
        }
    }
]
```

Exemplo de busca de uma entidade sem filtro.

```http
GET /app1/cliente HTTP/1.1
Host: localhost:9090
```

Exemplo de busca de uma entidade com filtro.

```http
GET /app1/contaAssociada?filter=byCliente&clienteId=29c125c4-b7c0-4d80-8c40-90284891e3db HTTP/1.1
Host: localhost:9090
```






