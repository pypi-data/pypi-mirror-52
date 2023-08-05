# Pedimos la IP y el puerto y nos conectamos
read -r -p 'Introduce la IP: ' ip
read -r -p 'Introduce el puerto: ' puerto
nc $ip $puerto
