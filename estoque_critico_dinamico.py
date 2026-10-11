"""
Exercício 3: Verificação de Estoque Crítico (Setor de Logística)

Dada a lista de produtos e a lista correspondente de quantidades, o programa
percorre as listas e, para cada item que esteja abaixo do estoque mínimo,
exibe o alerta:
    "ALERTA: O produto [nome] está com apenas [quantidade] unidades no estoque!"

A exibição é feita em janelas gráficas (tkinter):
  - Janela principal com a tabela do relatório (Produto, Quantidade, Status),
    destacando em vermelho os itens críticos.
  - Campo para alterar o estoque mínimo em tempo de execução; ao aplicar,
    a tabela, o resumo e os alertas são recalculados.
  - Caixas de diálogo de alerta para cada produto crítico.
"""

import tkinter as tk
from tkinter import ttk, messagebox

try:
    import pandas as pd
except ImportError:  # pandas é opcional; o programa funciona sem ele
    pd = None

# Listas de produtos e quantidades
estoque_produtos = ["monitor", "teclado", "mouse", "headset", "gabinete"]
estoque_quantidades = [5, 12, 2, 8, 15]

# Estoque mínimo inicial (pode ser alterado pela janela durante a execução)
estoque_minimo = 8


def classificar(quantidade):
    """Retorna o status do item conforme o estoque mínimo."""
    return "CRÍTICO" if quantidade < estoque_minimo else "Adequado"


def montar_relatorio():
    """Monta o relatório como lista de tuplas (Produto, Quantidade, Status).

    Se o pandas estiver disponível, usa um DataFrame (como no enunciado);
    caso contrário, utiliza apenas as listas.
    """
    if pd is not None:
        # Cria DataFrame
        df = pd.DataFrame({
            "Produto": estoque_produtos,
            "Quantidade": estoque_quantidades,
        })
        # Adiciona coluna de status
        df["Status"] = df["Quantidade"].apply(classificar)
        return list(df.itertuples(index=False, name=None))

    return [
        (produto, quantidade, classificar(quantidade))
        for produto, quantidade in zip(estoque_produtos, estoque_quantidades)
    ]


def exibir_alertas(janela, relatorio):
    """Exibe uma janela de alerta para cada produto com estoque crítico."""
    criticos = [item for item in relatorio if item[2] == "CRÍTICO"]

    if not criticos:
        messagebox.showinfo(
            "Estoque",
            "Nenhum produto está abaixo do estoque mínimo.",
            parent=janela,
        )
        return

    for produto, quantidade, _ in criticos:
        messagebox.showwarning(
            "ALERTA DE ESTOQUE CRÍTICO",
            f"ALERTA: O produto {produto} está com apenas "
            f"{quantidade} unidades no estoque!",
            parent=janela,
        )


def criar_janela_principal():
    """Cria a janela principal com a tabela do relatório.

    O relatório NÃO é calculado apenas uma vez: a função interna
    ``atualizar_relatorio`` recalcula tabela, resumo e alertas sempre que o
    estoque mínimo é alterado pelo campo da janela.
    """
    janela = tk.Tk()
    janela.title("Verificação de Estoque Crítico - Setor de Logística")
    janela.geometry("520x420")
    janela.resizable(False, False)

    titulo = tk.Label(
        janela,
        text="Relatório de Estoque",
        font=("Segoe UI", 16, "bold"),
    )
    titulo.pack(pady=(15, 5))

    # --- Campo para alterar o estoque mínimo em tempo de execução ---
    frame_minimo = tk.Frame(janela)
    frame_minimo.pack(pady=(0, 10))

    tk.Label(
        frame_minimo,
        text="Estoque mínimo:",
        font=("Segoe UI", 10),
        fg="gray25",
    ).grid(row=0, column=0, padx=(0, 5))

    var_minimo = tk.StringVar(value=str(estoque_minimo))
    entrada_minimo = tk.Entry(
        frame_minimo,
        textvariable=var_minimo,
        width=6,
        justify="center",
        font=("Segoe UI", 10),
    )
    entrada_minimo.grid(row=0, column=1, padx=(0, 5))

    tk.Label(
        frame_minimo,
        text="unidades",
        font=("Segoe UI", 10),
        fg="gray25",
    ).grid(row=0, column=2, padx=(0, 10))

    colunas = ("Produto", "Quantidade", "Status")
    tabela = ttk.Treeview(janela, columns=colunas, show="headings", height=6)

    for coluna in colunas:
        tabela.heading(coluna, text=coluna)
        tabela.column(coluna, anchor="center", width=150)

    # Destaque visual para itens críticos / adequados
    tabela.tag_configure("critico", foreground="red", font=("Segoe UI", 10, "bold"))
    tabela.tag_configure("adequado", foreground="dark green")
    tabela.pack(padx=20, pady=5, fill="x")

    resumo = tk.Label(janela, font=("Segoe UI", 10, "bold"))
    resumo.pack(pady=(10, 5))

    # Relatório atual (recalculado a cada atualização)
    estado = {"relatorio": []}

    def atualizar_relatorio(mostrar_alertas=False):
        """Recalcula o relatório e atualiza a tabela na janela."""
        for item in tabela.get_children():
            tabela.delete(item)

        relatorio = montar_relatorio()
        estado["relatorio"] = relatorio

        total_criticos = 0
        for produto, quantidade, status in relatorio:
            tag = "critico" if status == "CRÍTICO" else "adequado"
            if tag == "critico":
                total_criticos += 1

            tabela.insert(
                "",
                "end",
                values=(produto, quantidade, status),
                tags=(tag,),
            )

        resumo.config(
            text=(
                f"Estoque mínimo atual: {estoque_minimo} unidades | "
                f"Itens críticos: {total_criticos}"
            )
        )

        if mostrar_alertas:
            janela.after(100, lambda: exibir_alertas(janela, estado["relatorio"]))

    def aplicar_minimo():
        """Lê o valor digitado e aplica como novo estoque mínimo."""
        global estoque_minimo

        texto = var_minimo.get().strip()
        try:
            novo_minimo = int(texto)
        except ValueError:
            messagebox.showerror(
                "Valor inválido",
                "Digite um número inteiro para o estoque mínimo.",
                parent=janela,
            )
            entrada_minimo.focus_set()
            entrada_minimo.select_range(0, tk.END)
            return

        if novo_minimo < 0:
            messagebox.showerror(
                "Valor inválido",
                "O estoque mínimo não pode ser negativo.",
                parent=janela,
            )
            entrada_minimo.focus_set()
            entrada_minimo.select_range(0, tk.END)
            return

        estoque_minimo = novo_minimo
        var_minimo.set(str(estoque_minimo))
        atualizar_relatorio(mostrar_alertas=True)

    botao_aplicar = tk.Button(
        frame_minimo,
        text="Aplicar",
        command=aplicar_minimo,
        font=("Segoe UI", 10),
    )
    botao_aplicar.grid(row=0, column=3)

    entrada_minimo.bind("<Return>", lambda _evento: aplicar_minimo())

    atualizar_relatorio()
    janela.after(300, lambda: exibir_alertas(janela, estado["relatorio"]))
    janela.mainloop()


if __name__ == "__main__":
    criar_janela_principal()
