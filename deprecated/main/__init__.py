#
from .graphData import Neo4j
from .views import upload_jsw, update_ditmco, clear_all
#Neo4j._graph.run("DROP CONSTRAINT on (n:pin) ASSERT n.fullName IS UNIQUE")
Neo4j._graph.run("CREATE INDEX on :pin(fullName)")
Neo4j._graph.run("CREATE INDEX on :pin(connectorName)")