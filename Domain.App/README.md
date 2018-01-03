# Domain.App

#### Introdução
A aplicação de modelagem de domínio e mapeamento(temporário) da plataforma oferece uma abstração técnologica sobre o modelo de dados usados dentro da plataforma, o usuário configura seu modelo de dados independente de qual tecnologia a plataforma irá oferecer

#### Estrutura do Projeto
O projeto é dividido em três módulos:
* Dominio
* Mapas
* Migrations(não implementado)

A pasta Dominio contém todos os arquivos YAML que o usuário modelou seu problema. A modelagem de entidades segue o seguinte padrão:

```yaml
tb_client:  
  nm_client:
    - string
  cpf:
    - string
  lst_name:
    - string
```

O modelo acima permite o usuário dar nomes para suas entidades e nome para os atributos, além disso, ele deve configurar o tipo de dado de cada atributo. Atualmente são suportados os seguintes tipos:


* string
* integer
* char
* text
* bigint
* float
* real
* double
* decimal
* boolean
* time
* date
* hstore
* json
* jsonb
* blob
* uuid  


Observação: ```Cada entidade deverá estar descrita em seu próprio arquivo.```


A pasta Mapas contém a definição de mapeamento de domínio, cada aplicação dentro da plataforma poderá descrever seu próprio mapa, a ideia é montar um subdomínio de dados totalmente desacoplado do modelo real em relação as aplicações.

Segue abaixo um exemplo de um mapeamento de dados:

```yaml
cliente:
  model: tb_client
  fields:
    nome:
      column: nm_client
      required: true
    sobrenome:
      column: lst_name
      required: true    
    nomeCompleto:
      type: function
      eval: (client,acc)=> client.nome + " " + client.sobrenome
  filters:
    byName:
      nome: :nome
    umOuOutro:      
      $or:
        - nome:
            $eq: :nome1
        - nome:
            $eq: :nome2

conta:
  model: tb_account
  fields:
    saldo:
      column: vl_balance
  filters:
    byId:
      id: :id

contaAssociada:
  model: tb_opened_account
  fields:
    conta: 
      column: account_id
    cliente: 
      column: client_id
  filters:
    byId:
      id: :id
    byCliente:
      cliente: :clienteId
    byConta:
      conta: :contaId

```

Dentro de um mapeamento podemos definir 3 importantes seções:
* model
* fields
* filters

Model é a associação de nome de entidade, no exemplo acima o modelo de dominio "tb_client" foi associada ao nome "cliente" a aplicação que irá consumir este mapa irá conhecer apenas uma entidade chamada "cliente" e não vai conhecer a entidade de dóminio "tb_client"

Fields define o mapeamento de campos entre a entidade de domínio e o subdomínio da aplicação, além disso é possível criar mapeamentos calculados através de funções lambda JavaScript

Filters define uma seção de filtros dentro do domínio, o usuário de aplicação não poderá consultar livremente dados dentro do domínio de dados, cada mapa terá especificado quais filtros serão suportados e a associação do nome de parâmetro para nome do modelo exemplo:
```yaml
byId:
    id: :id
```
No exemplo acima, existe um filtro de nome "byId" que vai associar um parâmetro de nome id ao campo id da entidade mapeada.

A aplicação de domínio não depende de nenhuma tecnologia específica tudo é feito de forma declarativa através de arquivos YAML.

### Migrações

Migrações são operações de mudanças físicas no banco de dados, para a plataforma será possível
executar dois tipo de migração: adicionar colunas, criar tabelas.
As migrações são executadas no startup da aplicação

Exemplo de migração para adicionar colunas:
```yaml
add_column:
  table: "tb_client"
  columns:
    address: 
      type: string
```

Exemplo de migração para adicionar uma tabela:
```yaml
create_table:
  name: tb_address
  columns:
    client_id: 
      type: string
    street: 
      type: string
    number: 
      type: integer
    zipCode:
      type: string
```

