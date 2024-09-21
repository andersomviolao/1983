import os
import tkinter as tk
from tkinter import ttk
import subprocess
import threading
import signal

# Variável global para armazenar o processo em execução
process = None

# Função para procurar o ambiente virtual Python nas subpastas
def find_venv(folder):
    for root, dirs, files in os.walk(folder):
        if 'Scripts' in dirs and 'python.exe' in os.listdir(os.path.join(root, 'Scripts')):
            return os.path.join(root, 'Scripts', 'python.exe')
    return None

# Função para listar arquivos .py e .pyw nas subpastas
def list_py_files(folder):
    py_files = []
    for root, dirs, files in os.walk(folder):
        py_files.extend([os.path.join(root, f) for f in files if f.endswith('.py') or f.endswith('.pyw')])
    return py_files

# Função para rodar o arquivo selecionado
def run_selected_file():
    global process
    selected_file = file_var.get()
    if selected_file:
        command = [venv_path, selected_file]  # Não usar shell=True
        process = subprocess.Popen(command)
        threading.Thread(target=process.communicate).start()

# Função para parar o script em execução
def stop_script():
    global process
    if process is not None:
        try:
            process.terminate()  # Tentar encerrar o processo
            process.wait(timeout=5)  # Esperar que o processo termine
        except subprocess.TimeoutExpired:
            os.kill(process.pid, signal.SIGKILL)  # Forçar o encerramento se não encerrar normalmente
        process = None

# Definir o diretório atual como ponto de partida
current_dir = os.getcwd()

# Localizar o ambiente virtual Python automaticamente
venv_path = find_venv(current_dir)

if venv_path is None:
    print("No Python VA?")
    exit()

# Inicializar interface gráfica
root = tk.Tk()
root.title("Run Your Python Script")
root.geometry("700x200")

# Variável para armazenar o arquivo selecionado
file_var = tk.StringVar()

# Dropdown menu
file_label = tk.Label(root, text="File:")
file_label.pack(pady=10)

# Listar arquivos Python nas subpastas
py_files = list_py_files(current_dir)

# Caixa de seleçao
file_dropdown = ttk.Combobox(root, textvariable=file_var, width=100)
file_dropdown['values'] = py_files
file_dropdown.pack(pady=10)

# Botão para executar o arquivo
run_button = tk.Button(root, text="Run", command=run_selected_file)
run_button.pack(pady=10)

# Botão para parar o script
stop_button = tk.Button(root, text="Kill", command=stop_script)
stop_button.pack(pady=10)

root.mainloop()
