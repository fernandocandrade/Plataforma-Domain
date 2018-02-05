
import pytest
import os

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
        transferencia:
            id:
                $in:
                    - ":origem"
                    - ":destino"
""")
f.close()

pytest.main(['--cov', '--cov-report=html'])

import shutil
shutil.rmtree('./migrations')
shutil.rmtree('./maps')