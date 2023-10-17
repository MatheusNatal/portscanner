import tkinter as tk
from tkinter import scrolledtext
import socket
import threading
import queue
from PIL import Image, ImageTk
import webbrowser
import tkinter.font as tkFont

def verificar_portas():
    host = socket.gethostname()
    resultado.config(state=tk.NORMAL)
    resultado.delete(1.0, tk.END)
    
    if porta_option.get() == "main_ports":
        portas = [80, 443, 22, 21, 25]
    else:
        portas = portas_entry.get().split(',')
    
    results_queue = queue.Queue()  # Fila para receber resultados das threads

    # Função para realizar a verificação em uma porta
    def verificar_porta(porta):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            try:
                sock.connect((host, porta))
                resultado_text = f'A porta {porta} está aberta.\n'
            except (ConnectionRefusedError, TimeoutError):
                resultado_text = f'A porta {porta} está fechada.\n'
            except Exception as e:
                resultado_text = f'Erro ao verificar a porta {porta}: {e}\n'
            finally:
                sock.close()
            results_queue.put(resultado_text)
        except ValueError:
            results_queue.put(f'Porta inválida: {porta}\n')

    # thread para cada porta
    threads = []
    for porta_str in portas:
        try:
            porta = int(porta_str)
            thread = threading.Thread(target=verificar_porta, args=(porta,))
            threads.append(thread)
            thread.start()

        except ValueError:
            resultado.insert(tk.END, f'Porta inválida: {porta_str}\n')

    for thread in threads:
        thread.join()

    # Obtenha os resultados da fila e insira-os no widget de resultados
    while not results_queue.empty():
        resultado.insert(tk.END, results_queue.get())

    resultado.config(state=tk.DISABLED)

def limpar_resultados():
    resultado.config(state=tk.NORMAL)
    resultado.delete(1.0, tk.END)
    resultado.config(state=tk.DISABLED)

def habilitar_portas_personalizadas():
    portas_entry.config(state=tk.NORMAL, bg='white')
    portas_entry.delete(0, tk.END)

def desabilitar_portas_personalizadas():
    portas_entry.config(state=tk.DISABLED, bg='#2B2B2B')

def mostrar_info_portas():
    info_window = tk.Toplevel(root)
    info_window.title("Informações sobre Portas Principais")
    info_window.geometry("400x300")
    info_text = """
    Porta 80 (HTTP): Tráfego da Web não criptografado.
    Porta 443 (HTTPS): Tráfego da Web criptografado.
    Porta 22 (SSH): Acesso seguro ao servidor.
    Porta 21 (FTP): Transferência de arquivos.
    Porta 25 (SMTP): Envio de email.
    """
    info_label = tk.Label(info_window, text=info_text, wraplength=380, justify='left')
    info_label.pack()

def abrir_link(event):
    webbrowser.open("https://github.com/MatheusNatal")

root = tk.Tk()
root.title("PortScanner v1.0")


root.configure(bg='#2B2B2B')  # Cor de fundo da janela

# Desativar redimensionamento
root.resizable(False, False)

# Definir as dimensões da janela
root.geometry("450x300") 

# Abre o arquivo .ico com o Pillow e o converte para um formato suportado pelo Tkinter
icon_image = Image.open('icon.ico')
icon_photo = ImageTk.PhotoImage(icon_image)

root.iconphoto(True, icon_photo)

# Define a variável porta_option no escopo global
porta_option = tk.StringVar(value="main_ports")

# Cria widgets na janela
host_label = tk.Label(root, text=f"Host: {socket.gethostname()}", bg='#2B2B2B', fg='white')
host_label.grid(row=0, column=0, columnspan=2, padx=10, pady=1)

main_ports_radio = tk.Radiobutton(root, text="Portas Principais", variable=porta_option, value="main_ports", command=desabilitar_portas_personalizadas, bg='#2B2B2B', selectcolor='#2B2B2B', activebackground='#2B2B2B', fg='white', justify='left')
main_ports_radio.grid(row=1, column=0, columnspan=2, padx=10, pady=1, sticky='w')

custom_ports_radio = tk.Radiobutton(root, text="Portas Personalizadas", variable=porta_option, value="custom_ports", command=habilitar_portas_personalizadas, bg='#2B2B2B', selectcolor='#2B2B2B', activebackground='#2B2B2B', fg='white', justify='left')
custom_ports_radio.grid(row=2, column=0, columnspan=2, padx=10, pady=1, sticky='w')

portas_label = tk.Label(root, text="Portas (separadas por vírgula):", bg='#2B2B2B', fg='white', justify='left')
portas_label.grid(row=3, column=0, columnspan=2, padx=10, pady=1, sticky='w')

portas_entry = tk.Entry(root, state=tk.DISABLED, bg='#4A4A4A')
portas_entry.grid(row=4, column=0, columnspan=2, padx=10, pady=1, sticky='w')

verificar_button = tk.Button(root, text="Verificar Portas", command=verificar_portas, bg='#2B2B2B', fg='white')
verificar_button.grid(row=5, column=0, columnspan=2, padx=10, pady=2, sticky='w')

limpar_button = tk.Button(root, text="Limpar Resultados", command=limpar_resultados, bg='#2B2B2B', fg='white')
limpar_button.grid(row=2, column=0, columnspan=2, padx=10, pady=1, sticky='ne')

info_button = tk.Button(root, text="Informações sobre Portas", command=mostrar_info_portas, bg='#2B2B2B', fg='white')
info_button.grid(row=1, column=0, columnspan=2, padx=10, pady=1, sticky='e')

resultado_label = tk.Label(root, text="Resultado:", bg='#2B2B2B', fg='white', justify='left')
resultado_label.grid(row=7, column=0, columnspan=2, padx=10, pady=3)

assinatura = tk.Label(root, text="x-mas", bg='#2B2B2B', fg='white', justify='right', cursor="hand2")
assinatura.grid(row=10, column=0, columnspan=2, padx=10, pady=1, sticky='e')
assinatura.bind("<Button-1>", abrir_link)

fonte_link = tkFont.Font(assinatura, assinatura.cget("font"))
fonte_link.configure(underline=True)
assinatura.config(font=fonte_link)

resultado = scrolledtext.ScrolledText(root, state=tk.DISABLED, bg='#4A4A4A', fg='white')
resultado.grid(row=9, column=0, columnspan=2, padx=10, pady=2, sticky="nsew")

root.grid_rowconfigure(9, weight=1)
root.grid_columnconfigure(0, weight=1)

root.mainloop()
