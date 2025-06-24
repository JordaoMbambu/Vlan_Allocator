# VLAN Allocator - Calculateur de Sous-Réseaux VLSM

Un outil en ligne de commande interactif pour planifier et allouer des sous-réseaux IP en utilisant la méthode VLSM (Variable Length Subnet Masking), optimisant ainsi l'utilisation de l'espace d'adressage.

![Aperçu du programme](Vlan_Allocator.png)

---

## ➤ Fonctionnalités

* **Interface Interactive** : Un guide pas-à-pas en ligne de commande pour une utilisation simple et intuitive.
* **Calcul VLSM Automatisé** : Alloue les sous-réseaux de la manière la plus efficace possible pour minimiser le gaspillage d'adresses.
* **Saisie Dynamique** : Entrez autant de LANs (ou VLANs) que nécessaire, avec des noms personnalisés et le nombre d'hôtes requis.
* **Rapport Clair** : Affiche les résultats dans un tableau bien formaté et facile à lire, avec des séparateurs pour plus de clarté.
* **Gestion Robuste des Erreurs** : Valide les entrées pour prévenir les erreurs (format du réseau, capacité, nombre d'hôtes).
* **Exécutable Autonome** : Distribué sous forme de fichier `.exe` pour Windows, ne nécessitant aucune installation de Python.

---

## ➤ Installation

Choisissez la méthode qui correspond à votre besoin.

### Pour les Utilisateurs (Fichier `vlan_allocator.exe`)

Aucune installation n'est requise.

1.  Rendez-vous dans la section [**Releases**](https://github.com/JordaoMbambu/Vlan_Allocator/releases) de ce projet.
2.  Téléchargez la dernière version du fichier `vlan_allocator.exe`.
3.  Placez le fichier où vous le souhaitez et double-cliquez dessus pour le lancer.

### Pour les Développeurs (Code Source)

Si vous souhaitez modifier le code ou l'exécuter avec Python.

1.  **Clonez le dépôt** :
    ```bash
    git clone https://github.com/JordaoMbambu/Vlan_Allocator.git
    cd Vlan_Allocator
    ```

2.  **Créez un environnement virtuel** :
    ```bash
    python -m venv venv
    ```

3.  **Activez l'environnement** :
    * Sur Windows :
        ```bash
        .\venv\Scripts\activate
        ```
    * Sur macOS/Linux :
        ```bash
        source venv/bin/activate
        ```

4.  **Installez les dépendances** :
    ```bash
    pip install -r requirements.txt
    ```
    > **Note** : Si le fichier `requirements.txt` n'existe pas, créez-le avec `pip freeze > requirements.txt` après avoir installé `rich`.

---

## ➤ Utilisation

1.  Lancez le programme (en double-cliquant sur `vlan_allocator.exe` ou via `python Vlan_Allocator.py`).
2.  Suivez les instructions :
    * Entrez l'adresse réseau principale au format CIDR (ex: `192.168.0.0/16`).
    * Pour chaque LAN/VLAN, entrez un nom descriptif et le nombre d'hôtes requis.
    * Laissez le champ "Nom du LAN" vide et appuyez sur `Entrée` pour terminer la saisie.
3.  Le programme affichera le tableau récapitulatif des sous-réseaux alloués et attendra que vous appuyiez sur `Entrée` pour se fermer.

---

## ➤ Compiler depuis la source

Si vous avez modifié le code et souhaitez (re)créer le fichier `.exe`.

1.  Assurez-vous d'être dans l'environnement virtuel activé où `pyinstaller` est installé.
    ```bash
    pip install pyinstaller
    ```

2.  Lancez la commande suivante depuis la racine du projet :
    ```bash
    pyinstaller --onefile --icon="Vlan_Allocator.ico" Vlan_Allocator.py
    ```

3.  L'exécutable final `vlan_allocator.exe` se trouvera dans le dossier `dist/`.

---

## ➤ Licence

Ce projet est distribué sous la licence MIT. Voir le fichier `LICENSE` pour plus d'informations.

---
*Projet créé par [JordaoMbambu](https://www.linkedin.com/in/jordao-mbambu-alternance-cybersecurit%C3%A9-it-r%C3%A9seau-t%C3%A9l%C3%A9com/)*
