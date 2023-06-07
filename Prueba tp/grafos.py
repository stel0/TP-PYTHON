from graphviz import Digraph
from Database import Database

DATABASE = "base.db"
db = Database(DATABASE)
db.connect()
def generate_graph():
    dot = Digraph()
    return dot

def generate_node(graph, nombre_dependencia, label):
    graph.node(nombre_dependencia, label)

def connect_nodes(graph, node1_label, node2_label, edge_label):
    graph.edge(node1_label, node2_label, edge_label)


def generar_grafo(graph, id_dependencia, id_organigrama, nom_org):
    """
    Función recursiva para generar el organigrama
    Argumentos:
        graph: Objeto Digraph de graphviz
        id_dependencia: dependencia desde la cual graficar el organigrama
        id_organigrama: id del organigrama a graficar
        nom_org: nombre del organigrama a graficar
    """
    # conseguimos a las personas con id_dependencia igual al argumento recibido
    res_jefe = db.buscarData("Persona", f"id_dependencia = {id_dependencia} AND id_organigrama = {id_organigrama}", ["id", "apellido", "nombre"])
    print(res_jefe)
    if len(res_jefe) != 0:
        # buscamos la dependencia con id = id_dependencia para tener nombre del nodo
        if id_dependencia != 0:
            res_dep = db.buscarData("Dependencia", f"id = {id_dependencia} AND id_organigrama = {id_organigrama}", ["nombre"])
            nombre_dep = res_dep[0][0]
        else:
            nombre_dep = nom_org

        # buscamos cada dependencia que maneja cada jefe de res_jefe
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
                    # caso recursivo: generamos nuevos nodos con el id de la dependencia obtenida
                    generar_grafo(graph, dependencia[0], id_organigrama,nom_org)
            
            else: # si la persona actual no maneja ninguna dependencia, generamos un nodo solo de la persona
                generate_node(graph, f"{nombre} {apellido}", f"Apellido: {apellido}\nNombre: {nombre}")
                connect_nodes(graph, nombre_dep, f"{nombre} {apellido}", "")
                # Puede que se quite esta funcionalidad