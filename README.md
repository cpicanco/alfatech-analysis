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

# Instalação no VSCode

1. Instale o Python com o Pip (https://www.python.org/)
2. Instale o VSCode (https://code.visualstudio.com/)
3. Clique na opção "Source Control" ou pressione `CTRL+SHIFT+G` no teclado.
4. Clone este repositório (por exemplo, por meio do link https://github.com/cpicanco/alfatech-analysis.git) ou o seu fork do repositório.
5. Abra o `Powershell` dentro do VSCode; assegure-se que você está dentro da pasta do repositório.
6. Crie um novo ambiente virtual: `py -m venv .alfatech`
7. Ative o ambiente virtual dentro do VSCode quando ele perguntar para você ou faça isso manualmente no Powershell do VSCode `.\alfatech\Scripts\activate`
8. Instale as dependências do projeto `py -m pip install -r requirements.txt`
9. Lembre-se de desativar o ambiente virtual ao sair `.\alfatech\Scripts\deactivate` ou configure seu ambiente para que isso ocorra automaticamente.

# Como começar a trabalhar com o cache?

Após conseguir acesso aos arquivos de cache, copie eles para a pasta `cache`. Em seguida, execute um script dentro da pasta `figures`.

# Como começar a trabalhar com o banco de dados diretamente?

## Opção 1. Obtenha a acesso ao dump do banco de dados e importe ele para um servidor local.

Essa opção pode ser usada para a análise dos dados existentes.

## Opção 2. Obtenha as senhas de acesso ao banco de dados do ambiente de produção.

Embora possível, essa opção não é recomendada no presente estágio de desenvolvimento.
