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

Para instalar a plataforma no ambiente local execute o seguinte comando:
```sh
$ plataforma --install
```

Para iniciar a plataforma no ambiente local execute o seguinte comando:
```sh
$ plataforma --start
```

Para parar a plataforma no ambiente local execute o seguinte comando:
```sh
$ plataforma --stop
```

Para criar uma solução de aplicações execute o comando abaixo:
```sh
$ plataforma --new solution
```
Todas as outras aplicações deverão ser criadas dentro do diretório da solution

Para criar uma aplicação de domínio executar o comando abaixo e preencher as informações da nova aplicação que forem solicitadas
```sh
$ plataforma --new domain
```

Para criar uma aplicação de processo execute o seguinte comando:
```sh
$ plataforma --new process
```

Para criar uma aplicação de apresentação execute o seguinte comando:
```sh
$ plataforma --new presentation
```

Para executar uma aplicação de domínio execute o seguinte comando
```sh
$ plataforma --run
```

Para limpar uma aplicação execute o comando abaixo
```sh
$ plataforma --clean
```

Em caso de dúvidas execute o seguinte comando
```sh
$ plataforma --help
```

