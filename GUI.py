import tkinter as tk
from TCPimplementation import FTP_TELNETcom

cli = None

#função de limpar o conteudo da janela ---------------
def clear_window(w):
    for widget in w.winfo_children():
        widget.destroy()
#-----------------------------------------------------

def conectar():
    def login():
        #--------------funções dos botões---------------------------------
        def open_file():
            cli.rqst_CD(file_entry.get())
            contents_label.config(text= cli.rqst_LIST())
            return

        def cdback_file():
            cli.rqst_CD('..')
            contents_label.config(text= cli.rqst_LIST())

        def download_file():
            cli.rqst_GET(file_entry.get())
            return
        
        def upload_file():
            cli.rqst_APPE(file_entry.get())
            contents_label.config(text= cli.rqst_LIST())
            return

        def create_file():
            cli.rqst_MKD(file_entry.get())
            contents_label.config(text= cli.rqst_LIST())
            return
        
        def delete_file():
            cli.rqst_DELE(file_entry.get())
            contents_label.config(text= cli.rqst_LIST())
            return
        #-----------------------------------------------------------------

        #O que acontece após fazer login ---------------------------------
        cli.login(login_user.get(), login_pass.get())

        clear_window(main_window)

        #Pede a lista de arquivos no servidor
        contents_label = tk.Label(main_window, text= cli.rqst_LIST())
        contents_label.pack(pady=5)

        #conteúdo da página
        file_entry = tk.Entry(main_window, width=30)
        open_button = tk.Button(main_window, text= "abrir pasta", command= open_file)
        create_button = tk.Button(main_window, text= "criar pasta", command= create_file)
        delete_button = tk.Button(main_window, text= "deletar", command= delete_file)
        download_button = tk.Button(main_window, text= "download", command= download_file)
        upload_button = tk.Button(main_window, text="upload", command= upload_file)
        cdback_button = tk.Button(main_window, text="voltar diretório", command= cdback_file)

        file_entry.pack(padx=5)
        open_button.pack(pady=1)
        create_button.pack(pady=1)
        delete_button.pack(pady=1)
        cdback_button.pack(pady=1)
        download_button.pack(pady=1)
        upload_button.pack(pady=1)
        # ---------------------------------------------------------------------

# Tela de login do usuario ----------------------------------------------------
    user_input = entry.get()
    user_input = user_input.split(" ")
    cli = FTP_TELNETcom(user_input[0], int(user_input[1]))
    cli.connect_command()

    main_window.title(user_input[0] + " " + user_input[1])
    login_label = tk.Label(main_window, text="Informe o nome de usuário e senha:")
    login_button = tk.Button(main_window, text="Login", command=login)
    login_user = tk.Entry(main_window, width=30)
    login_pass = tk.Entry(main_window, width=30, show="*")

    login_label.pack(pady=5)
    login_user.pack(pady=5)
    login_pass.pack(pady=5)
    login_button.pack(pady=10)
#---------------------------------------------------------------------------------
    


# Cria a tela principal
main_window = tk.Tk()
main_window.title("Cliente FTP")

main_window.geometry("600x400")

label = tk.Label(main_window, text="Informe IP e PORT do servidor:.")
label.pack(pady=10)

label1 = tk.Label(main_window, text="EX: 123.346.7.8 21")
label1.pack(pady=5)

entry = tk.Entry(main_window, width=30)
entry.pack(pady=10)

button = tk.Button(main_window, text="Conectar", command=conectar)
button.pack(pady=20)


main_window.mainloop()