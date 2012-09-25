import logging
import sys

from model import Graph
import db_utils

QUERY = """
SELECT persona.*,
       puestos.nombre AS puesto_nombre,
       puestos.id AS puesto_id,
       dependencias.id AS dependencia_id,
       dependencias.nombre AS dependencia_nombre,
       articulos.id AS articulo_id,
       articulos.texto AS articulo_texto
FROM designaciones
LEFT OUTER JOIN puestos ON puestos.id = designaciones.puesto_id
LEFT OUTER JOIN dependencias ON dependencias.id = designaciones.dependencia_id
LEFT OUTER JOIN articulos ON articulos.id = designaciones.articulo_id
LEFT OUTER JOIN persona ON persona.per_id = designaciones.persona_id
"""

root_logger = logging.getLogger()
if root_logger.handlers:
    for handler in root_logger.handlers:
        root_logger.removeHandler(handler)
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

LOG = logging.getLogger(__name__)


def main():
    conn = db_utils.connect('localhost', 'root', 'boletin_oficial')

    g = Graph()

    # ['articulo_id', 'articulo_texto', 'dependencia_id', 'dependencia_nombre', 'per_apellido', 'per_boletines', 'per_cuit', 'per_dni', 'per_domicilio_especial', 'per_estado_civil', 'per_id', 'per_nombre', 'per_nya', 'per_prefijo', 'per_sufijo', 'per_titulo', 'puesto_id', 'puesto_nombre']

    for r in db_utils.query_db(conn.cursor(), QUERY):

        articulo = g.articulos.create(id=r['articulo_id'],
                                      texto=r['articulo_texto'].decode('utf-8'))

        try:
            dependencia = list(g.dependencias.index.lookup(id=r['dependencia_id']))[0]
        except IndexError:
            dependencia = g.dependencias.create(id=r['dependencia_id'],
                                                nombre=r['dependencia_nombre'].decode('utf-8'))

        try:
            puesto = list(g.puestos.index.lookup(id=r['puesto_id']))[0]
        except IndexError:
            puesto = g.puestos.create(id=r['puesto_id'], nombre=r['puesto_nombre'].decode('utf-8'))
        
        try:
            persona = list(g.personas.index.lookup(id=r['per_id']))[0]
        except IndexError:
            persona = g.personas.create(dni=r['per_dni'],
                                        nombre_y_apellido=r['per_nya'].decode('utf-8'),
                                        id=r['per_id'])

        g.nombramientos.create(persona, dependencia, { 'puesto_id': r['puesto_id'] })
        g.plantel.create(dependencia, puesto, { 'persona_id': r['per_id'] })

        LOG.info('%r - %r - %r %r' % (articulo, dependencia, puesto, persona,))

        
if __name__ == '__main__':
    main()

