#!/bin/bash
set -euo pipefail

if [ "$EUID" -ne 0 ]; then
  echo "Please run with sudo"
  echo "sudo ./new-app.sh demo-app [fix]"
  exit 1
fi

# Argumentos
APP_NAME="${1:-}"
FIX="${2:-none}"

# Validación de APP_NAME
if [ -z "$APP_NAME" ]; then
  echo "Uso: sudo ./new-app.sh <app-name> [fix]"
  exit 1
fi

WORKDIR="$(pwd)/$APP_NAME"

# -------------------------------------
# Opción: aplicar fix para el manpage
# -------------------------------------
if [ "$FIX" == "fix" ]; then
  echo "Aplicando fix: creando página de manual..."
  mkdir -p $WORKDIR/usr/share/man/man1/
  cat <<EOF | gzip -9 > "$WORKDIR/usr/share/man/man1/demo-app.1.gz"
.TH demo-app 1 "Junio 2025" "0.0.1" "Página de manual demo-app"
.SH NAME
demo-app \- Aplicación demo escrita en Python
.SH SYNOPSIS
.B demo-app
.SH DESCRIPTION
Aplicación de ejemplo empaquetada como .deb.
Muestra un mensaje en consola al ejecutarse.
.SH AUTHOR
Jonathan Prado <jpradoar@gmail.com>
EOF
  echo "Página de manual instalada en: $WORKDIR/usr/share/man/man1/demo-app.1.gz"
else
  echo "No se aplicó el fix (modo: '$FIX')"
fi



# -------------------------------------
# Opción: aplicar fix para aws secret
# -------------------------------------
if [ "$FIX" == "fix-aws" ]; then
  echo "Aplicando fix de aws.  Borrando las cochinadas"
  sed -i 's/fnrwej3norgu3nu4u3on4uo5ouuesalj1dngvjls/aaaaaaaaaaaaa/g' demo-app/lib/demo-app/main.py
  exit 0
else
  echo "No se aplicó el fix de aws (modo: '$FIX')"
fi



# Creación de directorios
sudo mkdir -p $WORKDIR/usr/bin/
sudo mkdir -p $WORKDIR/lib/$APP_NAME


# Creación de archivos 
cat <<EOF > "$WORKDIR/lib/$APP_NAME/main.py"
def main():
    aws_access_key_id = "AKF34GERSGERS54GREGHERGER"                     # FAKE
    aws_secret_access_key = "fnrwej3norgu3nu4u3on4uo5ouuesalj1dngvjls"  # FAKE para que detecte Trivy
    print("¡Hola desde $APP_NAME!")
EOF


cat <<EOF > "$WORKDIR/lib/$APP_NAME/__init__.py"
  # __init__.py: necesario para que Python lo trate como un paquete
  # básicamente puede estar vacío.
EOF


cat <<EOF > "$WORKDIR/usr/bin/$APP_NAME"
#!/usr/bin/env python3
import sys
sys.path.insert(0, "/usr/lib/$APP_NAME")

from main import main

if __name__ == "__main__":
    main()
EOF

chmod +x "$WORKDIR/usr/bin/$APP_NAME"


cat <<EOF > "$WORKDIR/DEBIAN/control"
Package: $APP_NAME
Version: 0.0.1
Section: utils
Priority: optional
Architecture: all
Maintainer: Jonathan Prado <jpradoar@gmail.com>
Depends: python3
Description: Aplicación demo empaquetada como .deb
 Esta es una aplicación de ejemplo escrita en Python.
EOF


cat <<EOF > "$WORKDIR/DEBIAN/preinst"
#!/bin/bash
set -e

echo "preinst: preparando la instalación de $APP_NAME"

# Ejemplo: eliminar una instalación anterior manual si existiera
[ -f /usr/bin/$APP_NAME ] && rm -f /usr/bin/$APP_NAME

exit 0
EOF


cat <<EOF > "$WORKDIR/DEBIAN/postinst"
#!/bin/bash
set -e

echo "postinst: $APP_NAME instalada correctamente"

# Actualizar base de datos de menús (opcional)
if command -v update-desktop-database >/dev/null 2>&1; then
  update-desktop-database || true
fi

# Asegurar permisos correctos (ya deberían estar, pero por si acaso)
chmod +x /usr/bin/$APP_NAME

exit 0
EOF


cat <<EOF > "$WORKDIR/DEBIAN/postrm"
#!/bin/bash
set -e

echo "postrm: limpieza tras desinstalar $APP_NAME"

# Eliminar archivos de configuración si los hubiera creado postrm
rm -f \
	/usr/lib/$APP_NAME
	/lib/$APP_NAME/__init__.py
	/lib/$APP_NAME/main.py

exit 0
EOF


# Crear e changelog de la documentación.  (requerido para buenas practicas)
cat <<EOF | gzip -9 > "$WORKDIR/usr/share/doc/$APP_NAME/changelog.gz"
$APP_NAME (0.0.1) stable; urgency=med

  * Versión inicial del paquete.

 -- Jonathan Prado <jpradoar@gmail.com>  $(date -R)
EOF


# Asignación de owner y ejecución
chown -R root:root "$WORKDIR"
chmod -R a+rX "$WORKDIR"


mkdir -p package/
dpkg-deb --build --root-owner-group $WORKDIR package/$APP_NAME.deb

tree
