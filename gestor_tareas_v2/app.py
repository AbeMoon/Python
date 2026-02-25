from tarfile import data_filter
from flask import Flask, request, redirect, render_template
import json
import os

app = Flask(__name__)

tareas = []
siguiente_id = 1

DATA_FILE = "taraes.json"

def cargar_datos():
    global tareas, siguente_id

    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
            tareas = data.get("tareas", [])
            siguiente_id = data.get("siguiente_id", 1)

def guardar_tareas():
    with open(DATA_FILE, "w") as f:
        json.dump({
            "tareas" : tareas,
            "siguiente_id" : siguiente_id
        }, f, indent = 4)

def agregar_tarea(texto):
    global siguiente_id

    tareas.append({
        "id" : siguiente_id,
        "texto" : texto,
        "hecho" : False
    })

    siguiente_id += 1
    guardar_tareas()

def completar_tarea(id):
    for tarea in tareas:
        if tarea["id"] == id:
            tarea["hecho"] = True
            break
    guardar_tareas()

@app.route("/")
def index():
    tareas_ordenadas = sorted(tareas, key=lambda t : t["hecho"])
    return render_template("index.html", tareas = tareas_ordenadas)

@app.route("/agregar", methods = ["POST"])
def agregar():
    texto = request.form.get("texto_tarea")

    if texto:
        agregar_tarea(texto)

    return redirect("/")

@app.route("/completar/<int:id>")
def completar(id):
    completar_tarea(id)
    return redirect("/")

if __name__ == "__main__":
    cargar_datos()
    app.run(debug=True)