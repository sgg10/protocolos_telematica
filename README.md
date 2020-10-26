# Protocolos Telematica

## Comandos del cliente
- ls "nameBucket" : lista los buckets y archivos del usuario
-  create "nameBucket" : crea un nuevo bucket con el nombre especificado
- delete "nameBucket" : elimina el bucket especificado
- upload "nameBucket"  "fullFilePath" : sube un archivo (con la ruta completa) al bucket especificado
- dowload "bucketPath" "dowloadPath" : descarga el archivo desde el servidor a una ruta especificada
- drop "bucketPath" : elimina un archivo de un bucket
- help : muestra este menu
- exit : termina la conexion con el servidor

## Inicio
### Servidor
Para correr el archivo servidor, basta con abrir una consola en la crapeta donde esta ubicado el archivo y ejecutarlo
`python Servidor.py`
Esto ejecutara el programa con los valores iniciales de host = localhost y port = 4000, pero si se desean editar, basta con añadirlos antes de la ejecucion, como por ejemplo
`python Servidor.py localhost 4500`
Si se desea estabalcer una ruta especifica donde el servidor almacenara los buckets, entonces se puede añadir despues del puerto, por ejemplo 
`python Servidor.py localhost 4500 C:\\users\\user\\Documents`
### Cliente
Al igual que con el servidor, basta con ejecutarlo en una nueva consola, pero hay que tener en cuenta que tanto sevidor como cliente deben correr bajo el mismo host y puerto para entablar la conexion. Para ejecutarlo con los valores por defecto, basta con usar
`python Cliente.py`
Y para usarlo con parametros personalizados
`python Cliente.py localhost 4500`
Podra abrir cuantos clientes quiera, pero recuerde que deben estar operando bajo el mismo host y puerto.

## Uso
A partir de este momento, podra usar los comandos explicados al inicio en las terminales de tipo cliente, para interactuar con el servidor y manejar los buckets y archivos que desee.
### Ejemplos
`create myBucket`

`ls`

`upload myBucket C:\\users\\myUser\\Download\\hola.txt`

`download myBuket/hola.txt C:\\users\\myUser\\Documents\\myFolder`

`ls myBucket`