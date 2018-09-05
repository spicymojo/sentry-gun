# Raspberry Pi Sentry Gun
Trabajo de Fin de Grado realizado en el Grado de Ingeniería Informática, con mención en Ingeniería del Software, 
cursado en la Universidad de Las Palmas de Gran Canaria
[![Vídeo demostrativo del proyecto](https://img.youtube.com/vi/xNmcc-VBpow/0.jpg)](https://www.youtube.com/watch?v=xNmcc-VBpow)

## Manual de usuario
#### 1. Descarga
Para descargar este proyecto bastará con clonar el repositorio
```sh
$ git clone https://github.com/mrivaj/sentry-gun
$ cd sentry gun
```

#### 2. Comprobaciones
En el repositorio que hemos descargado anteriormente podemos ver una carpeta "tests". En ella, están disponibles algunos pequeños programas para comprobar que los motores funcionan correctamente:
  - `pan_range_test.py`, `tilt_range_test.py`: Realiza una serie de movimientos con los motores para comprobar que todo funciona correctamente

#### 3. Calibración 
Para que el programa funcione correctamente, es necesario calibrar primero ambos motores. para ello, en la carpeta `calibrate` tenemos los siguientes archivos:
  - `calibrate_pan.py`, `calibrate_tilt.py`,`full_calibration.py` : Nos permiten calibrar la posición inicial del sistema utilizando las flechas del teclado
- `usb_camera_target:` Abre una ventana en la que podremos ver la webcam con el centro señalizado mediante un punto, para así facilitar la calibración

#### 4. Ejecución
Una vez calibrado, debemos ejecutar el programa principal
```sh
$ python sentry_gun.py
```
Durante la ejecución se nos mostrarán mensajes informativos por consola.
Una vez esté la cámara lista, se nos abrirán tres ventanas: 
  - **Cámara**: Nos muestra el streaming de vídeo de la cámara
  - **Umbralizado**: Aquí podemos ver la imagen de la cámara despues de haber pasado por un algoritmo de valor umbral, lo que la transforma en una imagen blanco/negro
  - **Frame Delta**: Esta ventana nos muestra el "frame acumulativo", es decir, las diferencias que aparecen entre el frame de referencia y la imagen actual
 
Una vez se detecta un objetivo, se procede a marcarlo en la imagen, así como a señalar su centro. Con los datos de la posición (x,y) de dicho centro, se calcula el número de pasos equivalente, y se mueve el motor para que apunte al objetivo.

#### 5. Salida del programa
Lo ideal es cerrar el programa con la tecla de salida (Por defecto, la tecla `q`). No obstante, como usamos un bloque `try-catch`, el programa siempre se asegurará de liberar correctamente los recursos utilizados
