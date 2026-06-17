#!/command/with-contenv bash

set -e

if grep -q "IDOCKER_HOSTNAME" /opt/app/app.py; then
    sed -i -e "s/IDOCKER_HOSTNAME/$HOSTNAME.i.vuln.land/g" /opt/app/app.py
fi
