# Estoque Crítico

Aplicação em Python para monitorar produtos com estoque abaixo do mínimo, com interface gráfica em Tkinter.

## Descrição

Este projeto simula um sistema de verificação de estoque crítico para um setor de logística. A partir de uma lista de produtos e quantidades, o programa:

- classifica cada item como `CRÍTICO` ou `Adequado`;
- mostra um relatório em tabela com produto, quantidade e status;
- exibe alertas visuais para itens com estoque abaixo do mínimo;
- permite ajustar o valor do estoque mínimo em tempo real pela interface.

## Funcionalidades

- Lista de produtos e quantidades configuradas no código;
- Cálculo automático do status de cada item;
- Janela principal com tabela de estoque;
- Destaque visual em vermelho para produtos críticos;
- Campo para alterar o estoque mínimo ao vivo;
- Mensagens de alerta para cada produto em situação crítica;
- Suporte opcional a `pandas` para montar o relatório em DataFrame.

## Requisitos

- Python 3.8 ou superior
- Biblioteca padrão `tkinter`
- `pandas` (opcional, apenas para a versão com DataFrame)

## Como executar

1. Clone o repositório:

```bash
git clone https://github.com/EmersonLopes2589/estoque_cr-tico.git
cd estoque_cr-tico
```

2. Execute o programa:

```bash
python estoque_critico_dinamico.py
```

## Exemplo de funcionamento

O projeto inicia com os seguintes dados:

- Produtos: `monitor`, `teclado`, `mouse`, `headset`, `gabinete`
- Quantidades: `5, 12, 2, 8, 15`
- Estoque mínimo inicial: `8`

Com isso, os itens abaixo do limite serão destacados como críticos e receberão alertas.

## Estrutura do projeto

```text
estoque_cr-tico/
├── estoque_critico_dinamico.py
├── README.md
└── .gitignore (se existir)
```

## Observações

- O programa foi desenvolvido como exercício de lógica e interface gráfica;
- o comportamento de atualização do relatório é recalculado sempre que o estoque mínimo é alterado;
- caso `pandas` não esteja instalado, a aplicação continua funcionando com listas e tuplas.

## Licença

Este projeto não possui licença definida no repositório.
