# SubGit 📦

**SubGit** est un outil CLI minimaliste et performant conçu pour extraire et télécharger des sous-dossiers spécifiques de dépôts GitHub sans avoir à cloner l'intégralité du projet.

Optimisé pour la rapidité, il propose une interface terminal moderne et épurée.

## Caractéristiques

- **Extraction Sélective** : Économisez du temps et de la bande passante en ne téléchargeant que le nécessaire.
- **Interface Minimaliste** : Barre de progression en temps réel, calcul précis de la taille et rapport final.
- **Dépôts Privés** : Support complet via les Personal Access Tokens de GitHub.
- **Récursivité** : Préserve intégralement la structure des dossiers et sous-dossiers.
- **Léger** : Un seul script Python, facile à installer et à transporter.

## Installation

### 1. Dépendances
Assurez-vous d'avoir Python 3 installé, puis installez les bibliothèques requises :
```bash
pip install -r requirements.txt
```

### 2. Configuration du script
Téléchargez subgit.py, rendez-le exécutable et créez un lien symbolique pour y accéder de n'importe où :
```bash
chmod +x subgit.py
sudo ln -s $(pwd)/subgit.py /usr/local/bin/subgit
```

## Configuration du Token (Accès aux dépôts privés)

Pour accéder à vos dépôts privés ou éviter les limitations de l'API GitHub, vous devez configurer un Personal Access Token (PAT).

### 1. Créer votre Token
1. Rendez-vous dans [GitHub > Settings > Tokens](https://github.com/settings/tokens).
2. Cliquez sur **Generate new token (classic)**.
3. Donnez-lui un nom et cochez la case **`repo`**.
4. Copiez le token généré.

### 2. Ajouter le Token à votre environnement
Pour que **SubGit** utilise ce token automatiquement, ajoutez-le à votre fichier de configuration shell (`.zshrc`, `.bashrc`, ou `.profile`) :

```bash
# Exemple pour Zsh 
echo 'export GITHUB_TOKEN="votre_token_ici"' >> ~/.zshrc

# Appliquer la modification immédiatement
source ~/.zshrc
```

Note : Une fois configuré, le statut de la session passera de `ANONYMOUS` à `AUTHENTICATED` au lancement de SubGit.


## Utilisation

Lancez simplement la commande dans votre terminal :

```bash
subgit
```

L'outil vous demandera alors de coller l'URL du dossier GitHub. Le format attendu est l'URL complète copiée depuis votre navigateur, par exemple : `https://github.com/user/repo/tree/branch/path/to/folder`


## License

Ce projet est sous licence **MIT**. Vous êtes libre de l'utiliser, de le modifier et de le distribuer. Consultez le fichier [LICENSE](LICENSE) pour plus de détails.

---


# 🐚 SubGit Bash Edition (Alternative)

Pour les puristes ou les environnements minimalistes, une version Bash ultra-rapide est également disponible. Elle ne nécessite que `curl` et `jq`.

## Installation rapide
```bash
cd subgit
chmod +x subgit.sh
sudo ln -sf $(pwd)/subgit.sh /usr/local/bin/subgit-bash
```

## Pourquoi l'utiliser ?

* **Performance** : Temps de démarrage quasi nul.
* **Portabilité** : Une seule dépendance externe (`jq`).

> [!IMPORTANT]
> Cette version nécessite **jq** pour traiter les données JSON de l'API GitHub.  
> Sur Arch Linux / EndeavourOS / Distro Arch-based : `sudo pacman -S jq`