# PyCad

PyCad é uma ferramenta automatizada para auxiliar no desenho e detalhamento de projetos de envidraçamento de sacadas no AutoCAD.

## Funcionalidades
- Interface gráfica intuitiva para entrada de dados de medição
- Cálculo de folgas, alturas, níveis e junções
- Exportação de relatórios e listagem de materiais
- Integração com o ECG para cadastro de materiais e dados da obra

## Como usar
Execute a interface principal com o Autocad (preferencialmente versao 2023) aberto com o Drawing1 armazenado na pasta DWGs:
```sh
python main_window.py
```
Siga as etapas na interface para inserir os dados do projeto e gerar os arquivos necessários.

## Estrutura do Projeto
- `src/` - Lógica principal, cálculos e integração com AutoCAD
- `UI/` - Interface gráfica e widgets customizados
- `dwgs/` - Arquivos DWG de base e exportações
- `exportacoes/` - Arquivos JSON gerados

# TODO

Fazer projeto padrao no ecg para cadastro do spev

Adicionar numeracao dos vidros

Adicionar angulos das paredes e prumos no autocad

Adicionar as ferragens no layout e puxar as formulas

Corrigir erros de calculos na funcao de folgas/alturas e niveis

Pegar dados da obra no ecg e completar cabeçalho

Adicionar linhas de sentido de abertura.
Adicionar arcos de porta
Adicionar detalhamentos de passantes/colantes
Adicionar tabelas com vidro de guarda-corpo

Pegar input com dados de perfis e descrição de onde vao, para adicionar nas observacoes
Adicionar informaçoes flutuantes para produção, instalação, transporte, usinagem, etc.

Conferir se fonte está em tamanho adequado
Adicionar logica pra posicionar as cotas de dreno e furo automaticamente sem precisar de intervencao