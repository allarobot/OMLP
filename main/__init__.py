#!/Users/jayhan/VirtualEnvs/flask_py3/bin python
# -*- coding: utf-8 -*-
from .models import Neo4j,Jsw,Pvg,FindFiles,Save
#Neo4j._graph.run("DROP CONSTRAINT on (n:pin) ASSERT n.fullName IS UNIQUE")
Neo4j._graph.run("CREATE INDEX on :pin(fullName)")
Neo4j._graph.run("CREATE INDEX on :pin(connectorName)")
Neo4j._graph.run("CREATE INDEX on :NOTE(key)")
