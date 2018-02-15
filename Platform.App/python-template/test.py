
import pytest
import os
import os.path
import shutil
from migration.sync import drop_database

drop_database("app_name")

if os.path.exists("./maps"):
    shutil.rmtree('./maps')
if os.path.exists("./migrations"):
    shutil.rmtree('./migrations')

os.mkdir("./maps")
f = open("./maps/Conta.yaml", "w")
f.write("""
Conta:
    model: conta
    fields:
        saldo:
            column: saldo
        titular:
            column: titular
    filters:
        transferencia: "id in (:origem, :destino)"
""")
f.close()

pytest.main(['--cov', '--cov-report=html', '-s'])


if os.path.exists("./maps"):
    shutil.rmtree('./maps')
if os.path.exists("./migrations"):
    shutil.rmtree('./migrations')