# Python 3.6.9
# Ubuntu 18.04.4 LTS (Bionic Beaver)

import json
from core import unixcmd

print(json.dumps(unixcmd.free("-lh"), indent=4))
print(json.dumps(unixcmd.df("-T"), indent=4))