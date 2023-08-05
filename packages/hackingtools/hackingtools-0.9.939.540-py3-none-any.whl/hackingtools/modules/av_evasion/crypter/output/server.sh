#/bin/sh

# Variables para iniciar
host_name=host
client_name=client

# Si no se define como parametro un puerto, se le da por defecto el 9999
if [ $# -ge 1 ]; then
  port=$1
else
  port=9999
fi

# Directorios temporales para los mensajes
input=/tmp/chat-receive-$port
output=/tmp/chat-sending-$port

# Borramos los temportales si habia
rm -f $input
rm -f $output
mkfifo $input
mkfifo $output

# Funcion para limpiar la linea
clear_line() {
  printf '\r\033[2K'
}

# Al pulsar con la tecla hacia arriba
move_cursor_up() {
  printf '\033[1A'
}

# Iniciamos el server con la IP y el puerto especificado
server() {
  echo "Iniciando en el puerto $port"
  tail -f $output | nc -l -p $port > $input
  echo server ending
}

# Funcion para recibir los mensajes
receive() {
  printf '%s: ' "$client_name" > $output
  local message
  while IFS= read -r message; do
    clear_line
    printf '\033[0;36m%s: \033[0;39m%s\n%s: ' "$client_name" "$message" "$host_name"
    move_cursor_up > $output
    clear_line > $output
    printf '\033[0;37m%s: \033[0;39m%s\n%s: ' "$client_name" "$message" "$client_name" > $output
  done < $input
  echo receive ending
}

# Funcion para iniciar el chat
chat() {
  printf '%s: ' "$host_name"
  local message
  while [ 1 ]; do
    IFS= read -r message
    clear_line > $output
    printf '\033[0;36m%s: \033[0;39m%s\n%s: ' "$host_name" "$message" "$client_name" > $output
    move_cursor_up
    clear_line
    printf '\033[0;37m%s: \033[0;39m%s\n%s: ' "$host_name" "$message" "$host_name"
  done;
  echo chat ending
}

# Inicio del Script: se pide el Nick
read -r -p 'Introduce tu Nick: ' host_name
# Se deja en segundo plano el server arrancado
server &
echo 'Esperando a que se una alguien...'
printf 'Introduce tu Nick: ' > $output
read -r client_name < $input
# Se muestra mensajes de bienvenida
echo "$client_name se ha unido al chat"
echo "Te has unido al chat de $host_name" > $output
receive &
chat
