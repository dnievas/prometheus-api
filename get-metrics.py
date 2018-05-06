#!/usr/bin/env python3

import json
import sys

from api import PrometheusAPI

prom = PrometheusAPI()

#cpu = prom.query(query='sum(rate(node_cpu{instance="localhost"}[1m])) by (mode)')
#json.dump(cpu, fp=sys.stdout)

series = prom.series(match='node_filesystem_files_free{instance="localhost"}')
json.dump(series, fp=sys.stdout)

