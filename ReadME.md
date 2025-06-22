Test Technique Pertimm
Description
Ce projet contient trois scripts :

register.py : pour créer un compte utilisateur sur l’API

login.py : pour se connecter et obtenir le token d’authentification

app.py : pour déposer une candidature et la confirmer

Installation
Installer Python 3

Installer la librairie requests:


pip install requests


python3 register.py

Le script te demandera ton email et ton mot de passe.

Connexion



python3 login.py

Le script te demandera ton email et ton mot de passe, puis affichera le token.


CREATE APP

python3 app.py
Le script te demandera :

le token

ton email

ton prénom

ton nom

