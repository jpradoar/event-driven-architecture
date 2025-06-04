#!/bin/bash

# RUN WITH: ---------
# 
#  sudo ./base-debian-package.sh
# 
# ------------------

if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  echo "sudo ./base-debian-package.sh demo-app"
  exit
fi

set -euo pipefail

# Configuración del paquete
APP_NAME="$1"
PACKAGE_VERSION="0.0.1"
PACKAGE_SECTION="utils"
PACKAGE_PRIORITY="optional"
PACKAGE_ARCH="all"
PACKAGE_DESCRIPTION="Base Debian package for demo y deb buildings"
OWNER_NAME="Jonathan Prado"
OWNER_MAIL="mail@gmail.com"
DATE="$(date -R)"

# Ruta de trabajo
WORKDIR="$(pwd)/$APP_NAME"
DOC_DIR="$WORKDIR/usr/share/doc/$APP_NAME"

echo "Creando estructura del paquete en: $WORKDIR"

# Crear estructura de directorios estándar
mkdir -p  $WORKDIR
mkdir -p "$WORKDIR/DEBIAN"
mkdir -p "$DOC_DIR"

# === Archivos de control ===
cat <<EOF > "$WORKDIR/DEBIAN/control"
Package: $APP_NAME
Version: $PACKAGE_VERSION
Section: $PACKAGE_SECTION
Priority: $PACKAGE_PRIORITY
Architecture: $PACKAGE_ARCH
Maintainer: $OWNER_NAME <$OWNER_MAIL>
Description: $PACKAGE_DESCRIPTION
 .
EOF


# preinst
cat <<'EOF' > "$WORKDIR/DEBIAN/preinst"
#!/bin/bash
set -e

#------------------------
#  TODA LA LOGICA ACÁ
#------------------------

touch /opt/preinst.test

exit 0
EOF

# postinst
cat <<'EOF' > "$WORKDIR/DEBIAN/postinst"
#!/bin/bash
set -e

#------------------------
#  TODA LA LOGICA ACÁ
#------------------------

touch /opt/postinst.test

exit 0
EOF

# postrm
cat <<'EOF' > "$WORKDIR/DEBIAN/postrm"
#!/bin/bash
set -e

#------------------------
#  TODA LA LOGICA ACÁ
#------------------------

rm -f /opt/postinst.test 
rm -f /opt/preinst.test

exit 0
EOF


chmod +x "$WORKDIR/DEBIAN/"{preinst,postinst,postrm}


# === Documentación obligatoria y copyright===
cat <<EOF > "$DOC_DIR/copyright"
Format: https://www.debian.org/doc/packaging-manuals/copyright-format/1.0/
Upstream-Name: $APP_NAME
Source: http://url_o_repo/$APP_NAME

Files: *
Copyright: $DATE $OWNER_NAME
License: GPL-3

License: GPL-3
 This package is free software; you can redistribute it and/or modify
 it under the terms of the GNU General Public License version 3,
 as published by the Free Software Foundation.

 On Debian systems, the complete text of the GNU General Public License
 version 3 can be found in "/usr/share/common-licenses/GPL-3".
EOF

# changelog.gz
cat <<EOF | gzip -9 > "$DOC_DIR/changelog.gz"
$APP_NAME ($PACKAGE_VERSION) stable; urgency=med

  * Initial release

 -- $OWNER_NAME <$OWNER_MAIL>  $DATE
EOF

# === Permisos y propietarios ===
chown -R root:root "$WORKDIR"
chmod 0755 $WORKDIR/usr


# Mostrar el arbol de directorios
tree
