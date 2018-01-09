# Domain App

#### Introdução
A aplicação de dominio da plataforma é responsável por oferecer recuros de leitura e escrita na base de dados da aplicação de forma desacoplada com o modelo físico de dados, além disso permite ao usuário criar um modelo de domínio agnóstico de tecnologia todo baseado em YAML. Além do modelo de domínio abstrato é possível também criar um mapa de acesso a dados customizando assim o nome de entidade e atributos de acordo com a necessidade da aplicação

#### Estrutura do Projeto
O projeto é dividido em três grandes módulos:
* [Domain.App](/Domain.App/README.md)
* [Platform.App](/Platform.App/README.md)
* [Platform.Cli](/Platform.Cli/README.md)

Domain.App contém a aplicação de domínio onde o usuário irá definir o modelo de dados físicos baseados em YAML;

Platoform.App contém o template de tecnologia de execução na plataforma. O NodeJs é o template de implementação atual;

Platform.Cli contém um projeto utilitário que compila a aplicação de domínio em YAML para uma aplicação completa NodeJS.

#### Requisitos

Para executar as aplicações com sucesso você precisa instalar as seguintes ferramentas:
* [NodeJS](https://nodejs.org)
* NPM (vem junto com o NodeJS)
* [Docker](https://www.docker.com/)
* Docker compose
* PostgresSQL*

*No caso de você não possuir o Docker instalado você deve instalar o Postgres manualmente na máquina.

Caso você opte por usar o docker você pode subir o Postgres e o Adminer com o seguinte comando:
```sh
$ docker-compose up -d
```
Ao executar esse comando o docker irá subir um container com o Postgres, Adminer e o PgAdmin4

O Adminer pode ser acessado diretamente pelo browser através do endereço:
http://localhost:8080

O PgAdmin4 poderá ser acessado também diretamente pelo Browser através do endereço:
http://localhost:5050

Ao entrar na tela será solicitado o acesso ao PgAdmin, entre com os seguintes valores:
user: pgadmin4@pgadmin.org
password: admin

Observação Importante:
    ```Lembre-se de escolher o ip da sua maquina para conectar ao Postgres com Adminer, se você colocar localhost o Adminer não irá encontrar o Postgres, lembre-se que eles estão rodando em containers diferentes```
    
<p align="center">
  <img src="./screenshots/loginAdminer.jpg" alt="Login no Adminer">
</p>

Para mais informações você pode consultar o README de cada projeto específico.




