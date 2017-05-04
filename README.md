<<<<<<< HEAD
Documentación
===


## SISTEMA INTEGRAL DE GESTIÓN PARA LAS INDUSTRIAS Y EL COMERCIO

   _____ _____________________ __________
  / ___//  _/ ____/ ____/ ___//  _/ ____/
  \__ \ / // / __/ __/  \__ \ / // /     
 ___/ // // /_/ / /___ ___/ // // /___   
/____/___/\____/_____//____/___/\____/



El __SISTEMA INTEGRAL DE GESTIÓN PARA LAS INDUSTRIAS Y EL COMERCIO (SIGESIC)__ es una herramienta tecnológica necesaria para 
implementar el registro de Unidades Económicas, con lo que se busca promover los planes de desarrollo del sector productivo de la 
República y simplificar los trámites administrativos en el ejercicio de sus competencias.

## Licencia

__SIGESIC__, sus carpetas y archivos, se disribuye bajo la Licencia de Software Libre GNU/GPL versión 2, esto implica que
el usuario final de la aplicación esta en la libertad de ejecutarla, modificar su código fuente, copiarla y/o
distribuírla, siempre y cuando al hacerlo se citen las fuentes originales de ésta aplicación.

Para obtener mayor información en torno a los términos de la licencia bajo los cuales se distribuye la
aplicación, lea con atención la [GPLv2](http://www.gnu.org/licenses/gpl-2.0.html).

Así mismo, las librerías y apis de terceros implementadas en esta aplicación, se distribuyen con sus respectivas
licencias y acuerdos particulares de cada una especificadas en los archivos de esas librerías.

## Pre-requisitos

Para el correcto funcionamiento del __SIGESIC__ se requiere tener instalado previamente los siguientes paquetes:

    // Paquetes del Sistema Operativo
    PostgreSQL 9.x
    Python >= 3.4
    PIP3 >= 8.1.1
    
    // Paquetes de Python
    Django >= 1.9.5 <1.10
    Pillow >= 2.8.1
    django-simple-captcha >= 0.5.1
    psycopg2 >= 2.6.1
    
## Proceso de instalación

En el proceso de instalación sobre los requerimientos y herramientas necesarias para el correcto funcionamiento del 
sistema, se deben ejecutar algunas instrucciones desde la consola de comando para lo cual se requiere abrir una terminal 
y ejecutar los siguientes comandos:

    // Para distribuciones ubuntu
    ~$ sudo su -
    
    // Para distribuciones debian
    ~$ su -
    
Lo anterior solicitara la contraseña de administrador del sistema operativo para acceder al usuario root, esto es 
necesario para los procesos de instalación posteriores de la aplicación.

Una vez autenticados como usuario root del sistema operativo, mostrará en la consola el símbolo "#" que identifica que 
el usuario actual es root, esto permitirá instalar en el sistema operativo los requerimientos de funcionamiento del 
sistema para lo cual se ejecutarán los comandos detallados a continuación:

    // Instalación de paquetes del sistema operativo
    ~# apt-get install postgresql python3.4 python3-pip

    // Instalación de paquetes del sistema operativo necesarios para la compilación de los requerimientos
    ~# apt-get install build-essential autoconf libtool pkg-config python-opengl python-imaging python-pyrex python-pyside.qtopengl idle-python3.4 qt4-dev-tools qt4-designer libqtgui4 libqtcore4 libqt4-xml libqt4-test libqt4-script libqt4-network libqt4-dbus python-qt4 python-qt4-gl libgle3 python3.4-dev libpq-dev
    
    // Instalación de paquetes de python (se debe acceder a la ruta principal del proyecto sicp)
    ~# pip install -r requirements/base.txt
    
Esto ejecutara los distintos procesos de instalación sobre los requerimientos del sistema.

Posteriormente se debe crear la base de datos del __SIGESIC__ y el correspondiente usuario que tendrá los privilegios 
necesarios para interactuar con la misa, esto se hace de la siguiente forma:

    // Acceso al usuario postgres
    ~# su postgres
    
    // Acceso a la interfaz de comandos de postgresql
    postgres@xxx:$ psql template1 
    
    // Creación del usuario de a base de datos
    temlate1=# CREATE USER nombre_usuario_bd WITH ENCRYPTED PASSWORD 'contraseña' createdb;
    temlate1=# \q
    
    // Desautenticar el usuario postgres y regresar al usuario root
    postgres@xxx:$ exit
    
    // Creación de la base de datos
    ~# createdb nombre_bd -E 'UTF-8' -O nombre_usuario_bd -h localhost -p 5432 -U nombre_usuario_bd
    
    // Salir del usuario root
    ~# exit
    

## Configuración y ejecución de la aplicación

Una vez instalados todos los requerimientos previos del sistema, se procede a la configuración del mismo, para esto se 
debe editar el archivo settings.py dentro de la carpeta __sigesic__ y modificar los datos por defecto de la variable DATABASES, 
en donde se especificarán los datos de acceso a las bases de datos de la aplicación.

Al tener ya configurado los parámetros de acceso a la base de datos, se ejecutan los siguiente comandos:

    // Para construir las migraciones de la base de datos en caso de que no existan

    ~$ python manage.py makemigrations

    // Para crear la estructura de la base de datos

    ~$ python manage.py migrate

Lo anterior crea la estructura de la base de datos e incorpora los registros básicos de la aplicación.

Para ejecutar la aplicación en modo de desarrollo, se debe ejecutar el siguiente comando:

    ~$ python manage.py runserver
    
Lo anterior ejecutará el servidor de desarrollo de django bajo la URL [http://localhost:8000](http://localhost:8000), 
para lo cual deberemos acceder a un navegador web y escribir dicha dirección URL.


## Documentación

Para acceder a la documentación del sistema, en donde se especifican las clases, funciones, atributos y métodos 
utilizados en la aplicación, debe abrir el archivo index.html ubicado en static/docs/sistema

=======
# sigesic_v2
SIGESIC
>>>>>>> 452bb7bb042baa8e1b7ad7f470c22773ac6c76f7
