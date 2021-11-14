# Camino aleatorio de una fuerza en una estructura de ladrillos
Camino aleatorio (random walk) que sigue una fuerza aplicada en una estructura de ladrillos. Se trata de un proceso aleatorio, ya que se elije aleatoriamente los puntos de apoyo, y con restricciones, ya que esos puntos tienen que satisfacer las ecuaciones de equilibrio. 

![Estructura de ladrillos](./img/esquema_03.pdf)

El programa principal es [ladrillos_fuerzas](./v1/ladrillos_fuerzas_v1.py), el cual realiza una simulación del recorrido de una fuerza en un estructura de ladrillos. Este funciona de la siguiente manera:\ 
1 - En la hilada x. Se detectan las fuerzas aplicadas al ladrillo\
2 - Se calcula la resultante de esas fuerzas\
3 - Se genera un trio de posibles puntos de apoyos aleatoriamente; desde aquí se pueden dar dos opciones:\
  3a - Ese trio de posibles puntos de apoyo no satisface las condiciones de equilibrio. Entonces se retrocede una hilada y se empieza por el punto 1.\
  3b - Ese trio de posibles puntos de apoyo satisface las condiciones de equilibrio. Entonces se avanza una hilada y se vuelve a empezar por el punto 1.
  
![Diagrama de flujo del programa](./img/diagrama_flujo.pdf)

Para más información sobre cómo funciona el código ver las anotaciones en el archivo .py\

De este programa se pueden modificar los parámetros iniciales (el número de hiladas, la discretización de los ladrillos y la fuerza inicial). El programa devuelve una matriz localicada en resultados.txt
