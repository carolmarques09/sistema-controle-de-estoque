# Controle de Estoque

import mysql.connector

from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk

# Conexão com o MySQL

conn = mysql.connector.connect(
    user='root',
    password='whyblu3',
    host='localhost',
    port='3306',
    database='estoque_discos'
)

cursor = conn.cursor()

    # if conn.is_connected():
    #    print("Conectado com sucesso!")
    #    cursor = conn.cursor()
    #    cursor.execute("SELECT DATABASE();")
    #    record = cursor.fetchone()
    #    print(f"Connected to database: {record}")

# estoque = {}

# Funções do banco

def adicionar_produto(nome, artista, genero, quantidade, preco):
    cursor.execute("""
        INSERT INTO produtos (nome, artista, genero, quantidade, preco)
        VALUES (%s, %s, %s, %s, %s)
    """, (nome, artista, genero, quantidade, preco))

    conn.commit()
    print("Produto adicionado com sucesso!")

def vender_produto(nome, quantidade):
    cursor.execute("""
        UPDATE produtos
        SET quantidade = quantidade - %s
        WHERE nome = %s AND quantidade >= %s
    """, (quantidade, nome, quantidade))

    conn.commit()

    if cursor.rowcount == 0:
        print("Estoque insuficiente ou produto não encontrado.")
    else:
        print("Venda realizada com sucesso!")

# adicionar_produto(estoque)
# vender_produto(estoque)

def alterar_produto(id_produto, novo_nome, nova_quantidade, novo_preco):
    cursor.execute("""
        UPDATE produtos
        SET nome = %s, quantidade = %s, preco = %s
        WHERE id_produto = %s
    """, (novo_nome, nova_quantidade, novo_preco, id_produto))

    conn.commit()

    if cursor.rowcount == 0:
        print("Produto não encontrado.")
    else:
        print("Produto atualizado com sucesso!")

# Testando a função
# alterar_produto(estoque)
# print(estoque)

# Interface gráfica

def init_prog():

    # colors
    azul = "#0394fc"
    branco = "#ffffff"
    preto = "#000000"
    vermelho =  "#d92316"
    verde = "#30d927"

    root = Tk()
    root.title("Controle de Estoque - Galeria do Metal")
    root.resizable(width=FALSE, height=FALSE)
    image = Image.open("ativ_paradigmas/heavymetal.jpg")
    photo = ImageTk.PhotoImage(image)

    def fechar_programa():
        cursor.close()
        conn.close()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", fechar_programa)

    tarja = Frame(root, width=400, height=80, bg=azul, relief='flat')
    tarja.grid(row=0, column=0)

    escopo = Frame(root, width=310, height=500, bg=branco, relief='flat')
    escopo.grid(row=1, column=0, padx=1, pady=0, sticky=NSEW)

    direita = Frame(root, width=1000, height=80, bg=preto, relief='flat')
    direita.grid(row=0, column=1, rowspan=2, padx=1, pady=0, sticky=NSEW)

    nomep = Label(tarja, text='Controle de Estoque', bg=azul, fg=branco, font=('Ivy 8'), anchor=NW, relief='flat')
    nomep.place(x=60, y=40)

    root.iconphoto(True, photo)
    root.mainloop()

init_prog()
