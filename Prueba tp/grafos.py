from graphviz import Digraph
from Database import Database

DATABASE = "base2.db"
db = Database(DATABASE)
db.connect()
def generate_graph():
    dot = Digraph()
    return dot

def generate_node(graph, nombre_dependencia, label):
    graph.node(nombre_dependencia, label)

def connect_nodes(graph, node1_label, node2_label, edge_label):
    graph.edge(node1_label, node2_label, edge_label)

def generar_grafo(graph, id_dependencia, id_organigrama):
    res_jefe = db.buscarData("Persona", f"id_dependencia = {id_dependencia} AND id_organigrama = {id_organigrama}", ["id", "apellido", "nombre"])
    print(res_jefe)
    if len(res_jefe) != 0:
        
        if id_dependencia != 0:
            res_dep = db.buscarData("Dependencia", f"id = {id_dependencia} AND id_organigrama = {id_organigrama}", ["nombre"])
            nombre_dep = res_dep[0][0]
        else:
            nombre_dep = "CEO"

        for jefe in res_jefe:
            id = jefe[0]
            apellido = jefe[1]
            nombre = jefe[2]
            dependencias = db.buscarData("Dependencia", f"manager_id = {id} AND id_organigrama = {id_organigrama}", ["id", "nombre"])
            
            if len(dependencias) > 0: 
                print(dependencias)   
                for dependencia in dependencias:
                    generate_node(graph, dependencia[1], f"Titulo: {dependencia[1]}\nApellido: {apellido}\nNombre: {nombre}")
                    connect_nodes(graph, nombre_dep, dependencia[1], "")
                    generar_grafo(graph, dependencia[0], id_organigrama)
            else:
                generate_node(graph, f"{nombre} {apellido}", f"Apellido: {apellido}\nNombre: {nombre}")
                connect_nodes(graph, nombre_dep, f"{nombre} {apellido}", "")
