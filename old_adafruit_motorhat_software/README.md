# Raspberry Pi Sentry Gun
## Manual de usuario
### 1. Descarga
Para descargar este proyecto bastará con clonar el repositorio
```sh
$ git clone https://github.com/mrivaj/sentry-gun
$ cd sentry-gun
```

### 2. Comprobaciones
En el repositorio que hemos descargado anteriormente podemos ver una carpeta "tests". En ella, están disponibles los archivos de prueba proporcionados por Adafruit ("tests/adafruit_motor_hat"), así como dos archivos de prueba propios:
  - `motor_test.py`: Realiza una serie de movimientos con los motores para comprobar que todo funciona correctamente
  - `usb_cam_test.py`: Nos muestra la imagen captada por la cámara, comprobando así que es compatible con nuestro setup
 
### 3. Ejecución
Una vez hayamos comprobado que todo va correctamente, debemos proceder a calibrar la torreta:
```sh
$ python calibrate_motors.py
```
Con este programa podremos calibrar la torreta utilizando las flechas del teclado. Nuestro objetivo es alinear el mecanismo de disparo con el centro de la torreta, así como dejarlo recto en el eje horizontal.
Una vez calibrado, ejecutamos el programa principal:
```sh
$ python sentry_gun.py
```
Durante la ejecución se nos mostrarán mensajes informativos por consola.
Una vez esté la cámara lista, se nos abrirán tres ventanas: 
  - **Cámara**: Nos muestra el streaming de vídeo de la cámara
  - **Umbralizado**: Aquí podemos ver la imagen de la cámara despues de haber pasado por un algoritmo de valor umbral, lo que la transforma en una imagen blanco/negro
  - **Frame Delta**: Esta ventana nos muestra el "frame acumulativo", es decir, las diferencias que aparecen entre el frame de referencia y la imagen actual
 
Una vez se detecta un objetivo, se procede a marcarlo en la imagen, así como a señalar su centro. Con los datos de la posición (x,y) de dicho centro, se calcula el número de pasos equivalente, y se mueve el motor para que apunte al objetivo.

#### ¿Qué ocurre cuando detectamos un objetivo?

- **Modo amigo activado:** No se dispara el mecanismo, sólo se muestra un aviso por consola
-  **Modo torreta:** Se dispara el mecanismo en cuanto el objetivo está al alcance

### 4. Salida del programa
Es necesario cerrar el programa con la tecla de salida configurada. Si utilizamos una combinación de teclas para terminar el proceso (como `CTRL + C`), la cámara no se liberará correctamente, lo cual puede darnos problemas en futuras ejecuciones
