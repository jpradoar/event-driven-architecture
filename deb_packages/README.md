# Generación de un paquete .deb usando buenas practicas

### Asignar permisos
	sudo chmod +x base-debian-package.sh new-app.sh

### Ejecutar el creador de estructura
	sudo ./base-debian-package.sh demo-app  

### Crear una app de demo
	sudo ./new-app.sh demo-app

### Correr test de paquete .deb
	./test_scan.sh demo-app lintian

### Fixear la app
	sudo ./new-app.sh demo-app fix     # Aplica el fix del manpage

### Correr test de seguridad
	./test_scan.sh demo-app trivy

### Fix leak de aws
	sudo ./new-app.sh demo-app fix-aws     # Aplica el fix del aws secret

### Correr test de seguridad
	./test_scan.sh demo-app trivy
