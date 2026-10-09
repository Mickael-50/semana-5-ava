# Sistema de Análise de Dados em Python

Projeto acadêmico que lê dados de um arquivo CSV, valida e-mail, CPF, telefone e data com expressões regulares (`re`), trata exceções e gera um relatório em texto.

## Requisitos

- Python 3.10 ou superior (usa anotações de tipo como `list[dict]` e `tuple[...]`).
- Não requer bibliotecas externas.

## Arquivos

- `main.py`: funções de validação, leitura, análise e relatório.
- `dados.csv`: arquivo de exemplo.
- `relatorio.txt`: criado automaticamente quando o programa é executado com sucesso.

## Como executar

1. Baixe ou clone o repositório.
2. Deixe `main.py` e `dados.csv` na mesma pasta.
3. Execute:

   ```bash
   python main.py
   ```

O programa mostra o relatório no terminal e salva uma cópia em `relatorio.txt`.

## Formato de entrada

O CSV deve usar cabeçalho com as quatro colunas obrigatórias: `email`, `cpf`, `telefone` e `data`.

```csv
email,cpf,telefone,data
ana.silva@email.com,123.456.789-00,(11) 91234-5678,15/03/2004
bruno@email,12345678900,11987654321,31/02/2020
```

## Validações aplicadas

- **E-mail:** `^[\w.+-]+@[\w-]+(?:\.[\w-]+)+$`. Verifica uma estrutura comum de e-mail, com usuário, `@` e domínio com ponto.
- **CPF:** `(?:\d{11}|\d{3}\.\d{3}\.\d{3}-\d{2})`. Aceita 11 dígitos ou o formato `000.000.000-00`.
- **Telefone:** `(?:\(?\d{2}\)?\s?)?(?:9?\d{4})-?\d{4}`. Aceita formatos comuns de telefone com ou sem DDD e pontuação.
- **Data:** `\d{2}/\d{2}/\d{4}` verifica o padrão `DD/MM/AAAA`; `datetime.strptime` verifica se a data realmente existe no calendário.

Os padrões são aplicados com `re.fullmatch`, que exige que o texto inteiro corresponda ao padrão. A validação do CPF verifica apenas a estrutura, não os dígitos verificadores. A regex de e-mail também não substitui uma confirmação real por envio de mensagem.

## Tratamento de exceções

- `FileNotFoundError`: informa quando o arquivo de entrada não existe.
- `PermissionError`: informa falta de permissão para ler o arquivo.
- `ValueError`: trata datas inexistentes e problemas de valor.
- `KeyError`: informa a ausência de colunas obrigatórias.
- `csv.Error`: trata erros na interpretação do CSV.
- `FormatoInvalidoError`: exceção personalizada para campos que falham nas validações.
- `try/except/else/finally`: demonstra tratamento de falhas, execução em caso de sucesso (`else`) e finalização (`finally`).

## Exemplo de saída

O resultado exato depende dos registros do CSV. O relatório inclui:

- total de registros analisados;
- quantidade de registros válidos e inválidos;
- taxa de aprovação;
- detalhes das linhas válidas e motivos de rejeição das linhas inválidas.

## Limitações conhecidas

Este projeto é didático. Ele verifica formatos comuns, mas não confirma se os dados pertencem a pessoas reais. Para uso em produção, seria recomendável implementar a validação matemática dos dígitos do CPF, definir formalmente os formatos de telefone aceitos e evitar expor dados pessoais completos em relatórios ou repositórios públicos.

## Publicação no GitHub

1. Crie um repositório chamado `sistema-analise-dados`.
2. Selecione a opção **Public**.
3. Envie `main.py`, `dados.csv` e `README.md`.
4. Não envie dados pessoais reais. Use apenas dados fictícios.
5. Execute o projeto e, se desejar, inclua uma amostra de `relatorio.txt`.

Exemplo com Git:

```bash
git init
git add main.py dados.csv README.md
git commit -m "Adiciona sistema de análise de dados"
git branch -M main
git remote add origin https://github.com/SEU-USUARIO/sistema-analise-dados.git
git push -u origin main
```

Substitua `SEU-USUARIO` pelo seu nome de usuário do GitHub.
