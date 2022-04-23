from PyQt5 import uic,QtWidgets
import mysql.connector as mysql
from reportlab.pdfgen import canvas

banco = mysql.connect(
    host="localhost",
    user="root",
    passwd="",
    database="cadastro_produtos"
)


def editar_dados():
    global numero_id

    linha = segunda_tela.tableWidget.currentRow()

    cursor = banco.cursor()
    cursor.execute("SELECT id FROM produtos")
    dados_lidos = cursor.fetchall()
    valor_id = dados_lidos[linha][0]
    cursor.execute("SELECT * FROM produtos WHERE id=" + str(valor_id))
    produto = cursor.fetchall()
    tela_editar.show()

    tela_editar.lineEdit.setText(str(produto[0][0]))
    tela_editar.lineEdit_2.setText(str(produto[0][1]))
    tela_editar.lineEdit_3.setText(str(produto[0][2]))
    tela_editar.lineEdit_4.setText(str(produto[0][3]))
    tela_editar.lineEdit_5.setText(str(produto[0][4]))
    tela_editar.lineEdit_6.setText(str(produto[0][5]))
    numero_id = valor_id


def salvar_valor_editado():
    global numero_id

    # ler dados do lineEdit
    codigo = tela_editar.lineEdit_2.text()
    descricao = tela_editar.lineEdit_3.text()
    preco = tela_editar.lineEdit_4.text()
    Qntd = tela_editar.lineEdit_5.text()
    categoria = tela_editar.lineEdit_5.text()
    # atualizar os dados no banco
    cursor = banco.cursor()
    cursor.execute(
        "UPDATE produtos SET codigo = '{}', descricao = '{}', preco = '{}', Qntd ='{}', categoria ='{}' WHERE id = {}".format(
            codigo, descricao, preco, Qntd, categoria, numero_id))
    banco.commit()
    # atualizar as janelas
    tela_editar.close()
    segunda_tela.close()
    chama_segunda_tela()


def excluir_dados():
    linha = segunda_tela.tableWidget.currentRow()
    segunda_tela.tableWidget.removeRow(linha)
    cursor = banco.cursor()
    cursor.execute("SELECT id FROM produtos")
    dados_lidos = cursor.fetchall()
    valor_id = dados_lidos[linha][0]
    cursor.execute("DELETE FROM produtos WHERE id=" + str(valor_id))


def gerar_pdf():
    cursor = banco.cursor()
    comando_SQL = "SELECT * FROM produtos"
    cursor.execute(comando_SQL)
    dados_lidos = cursor.fetchall()
    y = 0
    pdf = canvas.Canvas("cadastro_produtos.pdf")
    pdf.setFont("Times-Bold", 25)
    pdf.drawString(200, 800, "Produtos cadastrados:")
    pdf.setFont("Times-Bold", 11)

    pdf.drawString(10, 750, "ID")
    pdf.drawString(50, 750, "CODIGO")
    pdf.drawString(150, 750, "PRODUTO")
    pdf.drawString(250, 750, "PREÇO")
    pdf.drawString(300, 750, "Qntd")
    pdf.drawString(350, 750, "CATEGORIA")

    for i in range(0, len(dados_lidos)):
        y = y + 30
        pdf.drawString(10, 750 - y, str(dados_lidos[i][0]))
        pdf.drawString(50, 750 - y, str(dados_lidos[i][1]))
        pdf.drawString(150, 750 - y, str(dados_lidos[i][2]))
        pdf.drawString(250, 750 - y, str(dados_lidos[i][3]))
        pdf.drawString(300, 750 - y, str(dados_lidos[i][4]))
        pdf.drawString(350, 750 - y, str(dados_lidos[i][5]))
    pdf.save()
    print("PDF FOI GERADO COM SUCESSO")


def funcao_principal():
    linha1 = formulario.lineEdit.text()
    linha2 = formulario.lineEdit_2.text()
    linha3 = formulario.lineEdit_3.text()
    linha4 = formulario.lineEdit_4.text()

    categoria = ""

    if formulario.radioButton.isChecked():
        print("Produto adicionado ao departamento Interruptor e tomada")
        categoria = "Interruptor e tomada"
    elif formulario.radioButton_2.isChecked():
        print("Produto adicionado ao departamento Luminarias")
        categoria = "Luminarias"
    else:
        print("Produto adicionado ao departamento Cabos")
        categoria = "Cabos"

    print("Código:", linha1)
    print("Descricao:", linha2)
    print("Preco", linha3)
    print("Qntd", linha4)

    cursor = banco.cursor()
    comando_SQL = "INSERT INTO produtos (codigo,descricao,preco,Qntd,categoria) VALUES (%s,%s,%s,%s,%s)"
    dados = (str(linha1), str(linha2), str(linha3), str(linha4), categoria)
    cursor.execute(comando_SQL, dados)
    banco.commit()
    formulario.lineEdit.setText("")
    formulario.lineEdit_2.setText("")
    formulario.lineEdit_3.setText("")
    formulario.lineEdit_4.setText("")


def chama_segunda_tela():
    segunda_tela.show()

    cursor = banco.cursor()
    comando_SQL = "SELECT * FROM produtos"
    cursor.execute(comando_SQL)
    dados_lidos = cursor.fetchall()

    segunda_tela.tableWidget.setRowCount(len(dados_lidos))
    segunda_tela.tableWidget.setColumnCount(6)

    for i in range(0, len(dados_lidos)):
        for j in range(0, 6):
            segunda_tela.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))


app=QtWidgets.QApplication([])
formulario=uic.loadUi("formulario2.ui")
segunda_tela=uic.loadUi("Listardados.ui")
tela_editar=uic.loadUi("menu_editar.ui")
formulario.pushButton.clicked.connect(funcao_principal)
formulario.pushButton_2.clicked.connect(chama_segunda_tela)
segunda_tela.pushButton.clicked.connect(gerar_pdf)
segunda_tela.pushButton_2.clicked.connect(excluir_dados)
segunda_tela.pushButton_3.clicked.connect(editar_dados)
tela_editar.pushButton.clicked.connect(salvar_valor_editado)

formulario.show()
app.exec()
