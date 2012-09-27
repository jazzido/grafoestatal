from bulbs.neo4jserver import Graph as Neo4jGraph
from bulbs.model import Node, NodeProxy, Relationship, build_data
from bulbs.property import String, Integer, DateTime
from bulbs.utils import extract, get_file_path

# Modelos de designaciones boletin oficial
class Persona(Node):
    element_type = 'persona'
    id = Integer(nullable=False)

    nombre_y_apellido = String(nullable=False)
    titulo = String() # XXX puede ser una relacion
    prefijo = String()
    sufijo = String()
    cuit = Integer()
    dni = Integer()
    estado_civil = String()
    domicilio = String()
    boletines = String()

class Dependencia(Node):
    element_type = 'dependencia'

    id = Integer(nullable=False)
    nombre = String(nullable=False)

class Puesto(Node):
    element_type = 'puesto'

    id = Integer(nullable=False)
    nombre = String(nullable=False)

class Articulo(Node):
    element_type = 'articulo'

    id = Integer(nullable=False)
    texto = String(nullable=False)

class FuenteDeInformacion(Node):
    element_type = 'fuente_de_informacion'

    nombre = String(nullable=False)

class Nombrado(Relationship):
    label = 'nombrado'

class Plantel(Relationship):
    label = 'plantel'

class AparicionEnFuente(Relationship):
    label = 'aparece_en'

# Modelos de dineroypolitica.org

class PartidoPolitico(Node):
    element_type = 'partido_politico'

    id = Integer(nullable=False)
    kind = String(nullable=False)

class PersonaJuridica(Node):
    nombre = 'persona_juridica'

    id = Integer(nullable=False)
    cuit = Integer(nullable=False)


class Graph(Neo4jGraph):
    
    def __init__(self, config=None):
        super(Graph, self).__init__(config)

        # common node proxies
        self.fuentes_de_informacion = self.build_proxy(FuenteDeInformacion)

        
        
        # Node Proxies designaciones boletin oficial 
        self.personas     = self.build_proxy(Persona)
        self.dependencias = self.build_proxy(Dependencia)
        self.puestos      = self.build_proxy(Puesto)
        self.articulos    = self.build_proxy(Articulo)

        # Relationship Proxies designaciones boletin oficial 
        self.nombramientos       = self.build_proxy(Nombrado)
        self.plantel             = self.build_proxy(Plantel)
        self.aparicion_en_fuente = self.build_proxy(AparicionEnFuente)


        # Node proxies dineroypolitica
        self.partidos_politicos = self.build_proxy(PartidoPolitico)
        self.persona_juridica   = self.build_proxy(PersonaJuridica)

        # Relationship proxies dineroypolitica
        # XXX TODO
        
        
        
        # Add our custom Gremlin-Groovy scripts
        #scripts_file = get_file_path(__file__, "gremlin.groovy")
        #self.scripts.update(scripts_file)
