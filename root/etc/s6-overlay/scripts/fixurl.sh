#!/command/with-contenv bash

echo "put your commands to deploy the env based flag here"
echo "the variable \$GOLDNUGGET contains the dynamic flag"

echo "please extend this script and move $GOLDNUGGET to the final destination"
sed -i -e "s/IDOCKER_HOSTNAME/$HOSTNAME.i.vuln.land/g" /opt/app/app.py
echo $HOSTNAME > /tmp/ivan.log

