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
```

Para executar o compilador, apontando para a aplicação Domain.App você deve executar o seguinte comando:
```sh
$ node atom.js
```

Ao final da execução execute o seguinte comando para verificar se o pacote da aplicação foi gerado corretamente.
```sh
$ ls ../Platform.App
```
Se a sua sáida gerou um diretório chamado "bundle" dentro da pasta Platform.App significa que o compilador executou com sucesso.