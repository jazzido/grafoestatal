import logging
import sys

from model import Graph
import db_utils

QUERY = """
SELECT campaigns.*,
       political_parties.*,
       lists.*,
       providers.*,
       incomes.*
FROM incomes
INNER JOIN political_parties ON political_parties.id = incomes.`political_party_id`
INNER JOIN campaigns ON campaigns.id = incomes.`campaign_id`
INNER JOIN lists ON lists.`id` = incomes.`list_id`
INNER JOIN providers ON providers.`id` = incomes.`provider_id`
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

    for r in db_utils.query_db(conn.cursor(), QUERY):
        # XXX TODO
        # partidos politicos
        # personas (fisicas, juridicas) ver que onda con los cuits/dnis. tabla providers
        # donaciones
        # listas?

        LOG.info('%r - %r - %r %r' % (articulo, dependencia, puesto, persona,))
        
if __name__ == '__main__':
    main()

