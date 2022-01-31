# EMR22
Repsitorium zum Modul "Embedded Robotics" - EMR22 ab dem SS22.
Stichworte:  ROS1 - Noetic, Python, openCV, Gazebo, MoveIt!, UR3, UR5e

Wird in den ~/ws_moveit/src geclont und mit catkin build kompiliert


Nachdem Ubuntu Focal Fossa 20.4 (LTS) installiert wurde 
als erstes einen Workspace Ordner erstellen

Terminal öffnen mit STRG+ALT+T. Hinter dem Prompt $ die Befehle eingeben

>$ cd ~

>$ mkdir ws_moveit

>$ cd ws_moveit

>$ mkdir src

Klone das Repositorium nach catkin_ws/src
>$ cd ~/ws_moveit/src/

>$ git clone https://github.com/ProfJust/emr22.git

ggf. ist es vorher erforderlich noch git zu installieren:
>$ sudo apt install git

Jetzt sollte der Ordner emr22 geclont worden sein.


Erstellen des Moveit-Workspace mit Shellskript
>$ cd ~/ws_moveit/emr22/_install_script/

Nun ggf. erstmal ROS-Noetic installieren, dazu dem Skript 
die Ausführungsrechte geben und dann ausführen
>$ chmod +x ros_noetic_install_skript.sh

>$ ./ros_noetic_install_skript.sh 

Danach sämtliche für unseren Roboter benötigte Software-
Pakete installieren

>$ chmod +x  Install_MoveIt_on_ROS1.sh

>$ ./Install_MoveIt_on_ROS1.sh

ggf. noch die .bashrc - Datei konfigurieren
>$ gedit ~/.bashrc

Ergänze die Zeile
source ~/ws_moveit/devel/setup.bash

Kompilieren mit dem catkin-Build-System
>cd ~/ws_moveit

>catkin build

Falls catkin build nicht bekannt ist, 
versuchen Sie den Befehl in einem neuen Terminal zu starten.

Nun sollte man die Panda Arm - Demo in RViZ starten können

>$ roslaunch panda_moveit_config demo.launch rviz_tutorial:=true


