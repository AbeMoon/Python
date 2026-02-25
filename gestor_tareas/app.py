"""
Aplicación Flask - Gestor de Tareas
"""
from flask import Flask, request, redirect, render_template
import json

app = Flask(__name__)

tareas = []
siguiente_id = 1

def agregar_tarea(texto):
    global siguiente_id
    tareas.append({'id': siguiente_id, 'texto': texto, 'hecho': False})
    siguiente_id += 1
    guardar_tareas()

def completar_tarea(id):
    for tarea in tareas:
        if tarea['id'] == id:
            tarea['hecho'] = True
            break
    guardar_tareas()

def guardar_tareas():
    with open('tareas.json', 'w') as f:
        json.dump({ 'siguiente_id': siguiente_id, 'tareas': tareas}, f)

def cargar_datos():
    global siguiente_id, tareas
    try:
        with open('tareas.json', 'r') as f:
            data = json.load(f)
            tareas = data['tareas']
            siguiente_id = data['siguiente_id']
    except FileNotFoundError:
        pass

@app.route("/")
def index():
    tareas_ordenadas = sorted(tareas, key=lambda t: t['hecho'])
    return render_template('index.html', tareas = tareas_ordenadas)

@app.route('/agregar', methods = ['POST'])
def agregar():
    texto_tarea = request.form.get('texto_tarea')
    if texto_tarea:
        agregar_tarea(texto_tarea)
    return redirect('/')

@app.route('/completar/<int:id>')
def completar(id):
    completar_tarea(id)
    return redirect('/')

if __name__ == "__main__":
    cargar_datos()
    app.run(debug=True, port=5000)
