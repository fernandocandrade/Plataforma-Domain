# Platform.Cli

#### Introdução
Essa aplicação é um utilitário de compilação e geração do pacote preparado para execução do modelo de domínio declarado no Domain.App. O objetivo é transformar o arquivos em YAML num modelo de domínio Sequelize, que é um ORM para a plataforma NodeJS

#### Requisitos

* NodeJS
* Npm

### Executando o compilador de domínio

Antes de executar a aplicação é necessário instalar todas as dependências necessárias para a execução do projeto.
Para isso você deve executar o seguinte comando:
```sh
$ npm install
#disponibiliza o cliente para ser executado em outros diretórios
$ npm link
```

Para criar uma aplicação de domínio executar o comando abaixo e preencher as informações da nova aplicação que forem solicitadas
```sh
$ plataforma --new domain
```

Para executar uma aplicação execute o comando abaixo
```sh
$ plataforma --run
```

Em caso de dúvidas execute o seguinte comando
```sh
$ plataforma --help
```
