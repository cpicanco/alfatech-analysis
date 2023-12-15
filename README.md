# alfatech-analysis

Este repositório contém uma estratégia de análise (proof-of-concept) baseada na leitura direta do banco de dados relacional do GEIC.

# Sobre o banco de dados do GEIC
O GEIC não possui um módulo de análise de dados e não possui um banco de dados documentado. Adicionalmente, o GEIC e seus programas de ensino possuem diferentes versões e não há contratos que garantam a compatibilidade entre diferentes módulos. Esses fatos tornam o processo de construção de um módulo de análise de dados desafiador, especialmente quando se deseja fazer análises globais, reunindo todos os participantes.

# Sobre a estratégia adotada

Esta análise usa a biblioteca `sqlalchemy` para criar um cliente que realiza consultas ao servidor de banco de dados MySQL do GEIC. Atualmente, por questão de segurança, o cliente se comunica apenas com um servidor local, e não diretamente com o servidor no ambiente de produção.

As consultas foram organizadas em arquivos de texto sql de forma modular dentro da pasta `\figures\databases\queries`. No momento, cada consulta é chamada de forma procedural em uma rotina com as seguintes etapas:

1. Popular os objetos `student` e `students` com as informações do banco de dados de cada estudante.
2. Usar o objeto `students` para pupular os objetos `ACOLE1`, `ACOLE2`, `ACOLE3`, `MODULO1`, `MODULO2`, `MODULO3`.
3. Filtrar, limpar, editar, e salvar os objetos populados em um cache binário.
4. E, finalmente, ler o cache para tarefas de graficação, exportação, e contrução de tabelas.

Embora um esforço substancial tenha sido feito no sentido da modularização e abstração, o estágio de desenvolvimento atual é inicial e demanda refatoração.

# Como começar a trabalhar com o cache?

Após conseguir acesso aos arquivos de cache, copie eles para a pasta `cache`. Em seguida, execute um script dentro da pasta `figures`.

# Como começar a trabalhar com o banco de dados diretamente?

## Opção 1. Obtenha a acesso ao dump do banco de dados e importe ele para um servidor local.

Essa opção pode ser usada para a análise dos dados existentes.

## Opção 2. Obtenha as senhas de acesso ao banco de dados do ambiente de produção.

Embora possível, essa opção não é recomendada no presente estágio de desenvolvimento.
