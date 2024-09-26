import ast
import os
import tkinter as tk
from tkinter import ttk
import subprocess
import threading
import signal
import pip
import time

process = None
stop_flag = False

def apply_dark_mode():
    root.tk_setPalette(background='#2E2E2E')
    root.configure(bg='#2E2E2E')

    file_label.configure(bg='#2E2E2E', fg='#FFFFFF')

    style = ttk.Style()
    style.configure("TCombobox", fieldbackground="#4B4B4B", background="#4B4B4B", foreground="#FFFFFF")

    run_button.configure(bg='#3A3A3A', fg='#FFFFFF')
    stop_button.configure(bg='#3A3A3A', fg='#FFFFFF')

def list_py_files(folder):
    py_files = []
    for root, dirs, files in os.walk(folder):
        py_files.extend([os.path.join(root, f) for f in files if f.endswith('.py') or f.endswith('.pyw')])
    return py_files

def output_console():
    if process is not None:
        while True:
            if stop_flag:
                break

            output = process.stdout.readline().decode()
            error = process.stderr.readline().decode()
            if (output == '' and error == '') and process.poll() is not None:
                break

            if output:
                console_output.config(state=tk.NORMAL)
                console_output.insert(tk.END, output)
                console_output.yview(tk.END)
                console_output.config(state=tk.DISABLED)

            if error:
                console_output.config(state=tk.NORMAL)
                console_output.insert(tk.END, f"Error: {error}")
                console_output.yview(tk.END)
                console_output.config(state=tk.DISABLED)
            
            time.sleep(0.1)  # Pequeno atraso para reduzir o uso da CPU

def analyze_imports(filename):
    with open(filename, 'r') as f:
        tree = ast.parse(f.read())
    imports = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.extend(name.name for name in node.names)
        elif isinstance(node, ast.ImportFrom):
            imports.append(node.module)
    return imports

def install_packages(packages):
    try:
        subprocess.check_call(['pip', 'install'] + packages)
    except subprocess.CalledProcessError as e:
        console_output.config(state=tk.NORMAL)
        console_output.insert(tk.END, f"Erro ao instalar pacotes: {e}\n")
        console_output.yview(tk.END)
        console_output.config(state=tk.DISABLED)

def run_selected_file():
    global process, stop_flag
    selected_file = file_var.get()
    if selected_file:
        required_packages = analyze_imports(selected_file)
        missing_packages = [package for package in required_packages if not pip.main(['show', package])]
        if missing_packages:
            console_output.config(state=tk.NORMAL)
            console_output.insert(tk.END, f"Instalando pacotes faltantes: {', '.join(missing_packages)}\n")
            console_output.yview(tk.END)
            console_output.config(state=tk.DISABLED)
            install_packages(missing_packages)

        command = ['python', selected_file]
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stop_flag = False
        threading.Thread(target=output_console).start()

def stop_script():
    global process, stop_flag
    if process is not None:
        stop_flag = True
        try:
            process.terminate()
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            os.kill(process.pid, signal.SIGKILL)
        except Exception as e:
            console_output.config(state=tk.NORMAL)
            console_output.insert(tk.END, f"Erro ao parar o processo: {e}\n")
            console_output.yview(tk.END)
            console_output.config(state=tk.DISABLED)
        process = None

def update_file_list():
    py_files = list_py_files(current_dir)
    file_dropdown['values'] = py_files

current_dir = os.getcwd()

root = tk.Tk()
root.title("Run Your Python Script")
root.resizable(False, False)

root.grid_rowconfigure(0, minsize=100)
root.grid_rowconfigure(1, minsize=20)
root.grid_rowconfigure(2, minsize=200)

root.grid_columnconfigure(0, minsize=680)
root.grid_columnconfigure(1, minsize=60)
root.grid_columnconfigure(2, minsize=60)

file_var = tk.StringVar()

file_label = tk.Label(root, text="Select File:")
file_label.grid(row=0, column=0, columnspan=3, padx=0, pady=0, sticky="nsew")

py_files = list_py_files(current_dir)

file_dropdown = ttk.Combobox(root, textvariable=file_var)
file_dropdown['values'] = py_files
file_dropdown.grid(row=1, column=0, padx=0, pady=0, sticky="nsew")

run_button = tk.Button(root, text="Run", command=run_selected_file)
run_button.grid(row=1, column=1, padx=0, pady=0, sticky="nsew")

stop_button = tk.Button(root, text="Kill", command=stop_script)
stop_button.grid(row=1, column=2, padx=0, pady=0, sticky="nsew")

console_output = tk.Text(root, wrap='word', height=20)
console_output.grid(row=2, column=0, columnspan=3, padx=0, pady=0, sticky="nsew")
console_output.config(state=tk.DISABLED)  # Torna o widget de texto somente leitura

apply_dark_mode()

root.mainloop()
