import re
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from graphviz import Digraph
from PIL import Image, ImageTk

# Diccionario de operadores y símbolos
diccionario_operadores = {
    '#+': {'nombre': 'operador aditivo'},
    '#-': {'nombre': 'operador sustractivo'},
    '#*': {'nombre': 'operador multiplicativo'},
    '#/': {'nombre': 'operador de division'},
    '1#1': {'nombre': 'operador relacional igual'},
    '1#0': {'nombre': 'operador relacional diferente'},
    'N#': {'nombre': 'operador relacional mayor'},
    'n#': {'nombre': 'operador relacional menor'},
    'N##': {'nombre': 'operador relacional mayor o igual'},
    'n##': {'nombre': 'operador relacional menor o igual'},
    'y': {'nombre': 'Y logico'},
    'o': {'nombre': 'O logico'},
    '¬': {'nombre': 'NO logico'},
    ':': {'nombre': 'simbolo de apertura'},
    ';': {'nombre': 'simbolo de cierre'},
    '.': {'nombre': 'terminal'},
    ',': {'nombre': 'separador de sentencias'},
    'identificadores': [
        {'nombre': 'identificador variable', 'prefijos': ['rav']},
        {'nombre': 'identificador metodo', 'prefijos': ['tolf']},
        {'nombre': 'palabra para clase', 'prefijos': ['klasa']},
        {'nombre': 'identificador clase', 'prefijos': ['vip', 'all']}
    ],
}

# Función para abrir el explorador de archivos y seleccionar un archivo
def open_file_dialog():
    filename = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    return filename

# Función para leer el contenido del archivo
def read_file(filename):
    with open(filename, 'r') as file:
        return file.read()

# Función para crear expresiones regulares para identificadores
def create_identifier_patterns(identificadores):
    patterns = {}
    for identificador in identificadores:
        for prefijo in identificador['prefijos']:
            patterns[prefijo] = re.compile(r'\b' + prefijo + r'\w*\b')
    return patterns

# Función para analizar el texto y generar tokens
def lexer(text, diccionario_operadores):
    position = 0
    tokens = []

    # Crear expresiones regulares para operadores y símbolos
    token_patterns = {key: re.compile(re.escape(key)) for key in diccionario_operadores if key != 'identificadores'}

    # Añadir patrones para identificadores
    identifier_patterns = create_identifier_patterns(diccionario_operadores['identificadores'])

    # Patrones adicionales
    additional_patterns = {
        'NUMERO_ENTERO': re.compile(r'\b\d+E\b'),
        'NUMERO_REAL': re.compile(r'\b\d+(\.\d+)?R\b'),
        'CADENA_CARACTERES': re.compile(r'@#\*'),
        'CARACTER': re.compile(r'[#$/%?¿]')
    }

    while position < len(text):
        match = None

        # Combinar todas las expresiones regulares
        combined_patterns = {**token_patterns, **identifier_patterns, **additional_patterns}

        for token_type, regex in combined_patterns.items():
            match = regex.match(text, position)
            if match:
                if token_type in diccionario_operadores:
                    token = {
                        'type': diccionario_operadores[token_type]['nombre'],
                        'value': match.group(0),
                        'position': position
                    }
                elif token_type in additional_patterns:
                    token = {
                        'type': token_type.replace('_', ' ').capitalize(),  # Formato de tipo de token legible
                        'value': match.group(0),
                        'position': position
                    }
                else:
                    # Buscar el tipo de identificador correspondiente
                    for ident in diccionario_operadores['identificadores']:
                        if any(match.group(0).startswith(prefijo) for prefijo in ident['prefijos']):
                            token = {
                                'type': ident['nombre'],
                                'value': match.group(0),
                                'position': position
                            }
                            break
                tokens.append(token)
                position = match.end(0)
                break

        if not match:
            # Si no coincide con ningún patrón, avanza un carácter
            position += 1

    return tokens

# Función para crear un autómata visual a partir de un token
def crear_automata_token(token_value):
    dfa = Digraph()

    # Crear estados inicial y final
    dfa.node('start', 'Inicio', shape='circle')
    estado_anterior = 'start'
    estado_id = 0

    for caracter in token_value:
        estado_id += 1
        estado_actual = f'state{estado_id}'
        dfa.node(estado_actual, estado_actual, shape='circle')
        dfa.edge(estado_anterior, estado_actual, label=caracter)
        estado_anterior = estado_actual

    dfa.node('end', 'Fin', shape='doublecircle')
    dfa.edge(estado_anterior, 'end', label='')

    return dfa

# Función para mostrar un autómata dentro del canvas de Tkinter
def mostrar_automata_token(token_value, canvas):
    dfa = crear_automata_token(token_value)
    dfa.render('automata', format='png', cleanup=True)
    img = Image.open('automata.png')
    img = img.resize((canvas.winfo_width(), canvas.winfo_height()), Image.Resampling.LANCZOS)  # Ajustar el tamaño de la imagen
    img = ImageTk.PhotoImage(img)
    canvas.create_image(canvas.winfo_width() // 2, canvas.winfo_height() // 2, anchor=tk.CENTER, image=img)  # Centrando la imagen
    canvas.image = img

# Función principal para la interfaz gráfica
def main():
    root = tk.Tk()
    root.title("Lexer y Generador de Autómatas")
    root.geometry("1200x800")  # Ajustar el tamaño de la ventana

    # Crear el frame principal
    frame = ttk.Frame(root, padding="10")
    frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    # Frame izquierdo para botones y texto
    frame_izquierdo = ttk.Frame(frame, padding="10")
    frame_izquierdo.grid(row=0, column=0, sticky=(tk.W, tk.N, tk.S))

    # Frame derecho para el canvas
    frame_derecho = ttk.Frame(frame, padding="10")
    frame_derecho.grid(row=0, column=1, sticky=(tk.E, tk.N, tk.S))

    # Botón para abrir archivo
    btn_abrir = ttk.Button(frame_izquierdo, text="Abrir Archivo", command=lambda: seleccionar_archivo(txt_tokens, combobox, canvas))
    btn_abrir.grid(row=0, column=0, padx=5, pady=5)

    # Textbox para mostrar tokens
    txt_tokens = tk.Text(frame_izquierdo, width=80, height=20)
    txt_tokens.grid(row=1, column=0, padx=5, pady=5)

    # Lista desplegable para seleccionar tokens
    combobox = ttk.Combobox(frame_izquierdo)
    combobox.grid(row=2, column=0, padx=5, pady=5)
    combobox.bind("<<ComboboxSelected>>", lambda event: seleccionar_token(combobox, canvas))

    # Canvas para mostrar el autómata
    canvas = tk.Canvas(frame_derecho, width=600, height=600)
    canvas.grid(row=0, column=0, padx=5, pady=5)

    root.mainloop()

# Función para seleccionar archivo y mostrar tokens
def seleccionar_archivo(txt_tokens, combobox, canvas):
    filename = open_file_dialog()
    if not filename:
        messagebox.showerror("Error", "No se seleccionó ningún archivo.")
        return

    text = read_file(filename)
    tokens = lexer(text, diccionario_operadores)
    mostrar_tokens(tokens, txt_tokens, combobox, canvas)
    global tokens_global
    tokens_global = tokens

# Función para mostrar tokens en el Textbox y actualizar la lista desplegable
def mostrar_tokens(tokens, txt_tokens, combobox, canvas):
    txt_tokens.delete('1.0', tk.END)

    for token in tokens:
        txt_tokens.insert(tk.END, f"{token['type']}: {token['value']} (posición {token['position']})\n")

    # Actualizar la lista desplegable
    combobox['values'] = [f"{token['type']}: {token['value']}" for token in tokens]
    combobox.current(0)

    # Mostrar el autómata del primer token en el canvas
    mostrar_automata_token(tokens[0]['value'], canvas)

# Función para seleccionar un token de la lista desplegable y mostrar su autómata
def seleccionar_token(combobox, canvas):
    index = combobox.current()
    if index >= 0:
        token = tokens_global[index]
        mostrar_automata_token(token['value'], canvas)

if __name__ == '__main__':
    tokens_global = []
    main()
