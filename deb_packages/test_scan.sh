#!/bin/bash

APP_NAME="$1"
SCANNER_APP="$2"


# Test baratos
if [ $SCANNER_APP == "lintian" ]; then
	echo "Corriendo lintian en package/$APP_NAME.deb"
	echo
	lintian package/$APP_NAME.deb
	echo 
	echo "Lintian finalizó."
fi

if [ $SCANNER_APP == "trivy" ]; then
	echo "Corriendo trivy en busca de cochinadas"
	echo
	trivy fs $APP_NAME/
	echo 
	echo "trivy finalizó."
fi
