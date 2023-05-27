import graphviz

def crear_dependencia(nombre,numero):
    grafo = graphviz.Graph(format='png')

    etiqueta = f"{nombre}"
    grafo.node(etiqueta)

    archivo_salida=f"grafo_{numero}"
    grafo.render(archivo_salida,view=True)
    
crear_dependencia("Rectorado",1);