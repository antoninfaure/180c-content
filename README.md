# 180°C Content

Bienvenue sur le Git qui gére le contenu du site de 180°C ! 

Pour toute question, contactez [@antonin_faure](@antonin_faure) sur Telegram ;)

## Table des matières
 - [General](#general) 
    - [Préface - How to Git](#préface---how-to-git) 
    - [Cloner ce Git](#cloner-ce-git)
    - [Organisation](#organisation)
    - [Fonctionnement](#fonctionnement)
- [Crieur](#crieur)
    - [Ajouter un établissement](#ajouter-un-établissement)
        - [`place.json`](#placejson)
            - [Variables](#variables)
                - [Paramètre `top`](#paramètres-top)
                - [Paramètres `link`](#paramètres-link)
                - [Paramètres `location`](#paramètres-location)
        - [Ajouter des images](#ajouter-des-images)
    - [Modifier un établissement](#supprimer-un-établissement)
    - [Supprimer un établissement](#supprimer-un-établissement)
    - [Paramètres du Crieur](#paramètres-du-crieur)
        - [Types](#types)
            - [Paramètres](#paramètres-types)
        - [Tags](#tags)
            - [Paramètres](#paramètres-tags)
        - [Links](#links)
            - [Paramètres](#paramètres-links)
        - [priceTag](#pricetag)
        - [Ajouter un icône](#ajouter-un-icône)
- [Articles](#articles)
    - [Ajouter un article](#ajouter-un-article)
        - [Variables](#variables)
    - [Supprimer un article](#supprimer-un-article)

## General

### Préface - How to Git

Pour plus d'informations sur le fonctionnement de Git voir [ce lien](https://www.freecodecamp.org/news/how-to-use-basic-git-and-github-commands/).

### Installer Git

Dans un premier temps il faut installer Git sur son ordinateur : [Comment installer Git](https://github.com/git-guides/install-git).

Il faut ensuite configurer une clé ssh pour votre ordi. Voir ce [tutoriel détaillé](https://docs.github.com/fr/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent).

### Cloner ce Git

Pour cloner ce Git sur son ordi exécuter dans le dossier de votre choix la commande :
```
git clone https://github.com/antoninfaure/180c-content
```
Pour rester à jour des dernières modifications actualisées sur le Github il faut `pull` la dernière version depuis ce dernier. Dans votre dossier du Git exécutez :
```
git pull
```
Pour enregistrer ses modifications il faut `commit`. Dans votre dossier du Git exécutez :
```
git add . # ajouter tous les fichiers du dossier au commit
git commit -m "description de la modification"
```
Pour envoyer ses modifications sur github il faut `push`. Dans votre dossier du Git exécutez :
```
git push origin main
```
### Organisation

Le git est organisé selon plusieurs dossiers :
- `crieur` : gestion du Crieur (établissements, paramètres, ...)
- `membres` : gestion de la liste des membres
- `articles` : gestion des articles

Plusieurs scripts Python sont utilisés par la suite par Github Actions pour les pipelines de déploiements :
- `update_crieur.py` : actualise la base de données en fonction des établissements listés dans le dossier `crieur`
- `move_imgs.py` : copie les images des établissements sur le Git de l'app
- `utils.py` : définie des fonctions utilisées par les autres scripts

### Fonctionnement

Le site est basé sur une web application NodeJS dont le [Git](https://github.com/antoninfaure/node-180) est séparé de celui-ci. La gestion du contenu étant sur ce Git tandis que toute la machinerie se fait sur le Git de l'application donc pas besoin de la connaître ;).

Dès qu'un contenu est push sur la branche `main` du Github un pipeline GitHub Actions est lancé afin d'update la base de données et le Git de l'application avec les nouvelles données.

Tous les jours à 22h le Git de l'application passe la branche `main` sur la branche `prod`. Cette dernière est la version mise en production ce qui signifie que toute modification ne prendra effet qu'à 22h (sauf exécution manuelle de la part d'un admin).

Le site est quant à lui hébergé sur [Heroku](https://heroku.com) ([lien de l'application](https://dashboard.heroku.com/apps/epfl-180)) et relié à la branche `prod` du Git de l'application. Dès qu'une modification est effectuée sur cette branche, Heroku redéploie l'application avec la dernière version.

## Crieur

### Ajouter un établissement

Rien de plus simple, il faut juste créer un dossier avec le code de l'établissement souhaité (ex: `brasserie-du-chateau`). Ce dernier sera le même que dans le lien `https://.../crieur/{code}` donc attention aux charactères spéciaux.

La structure d'un établissement est la suivante : 

    code
    ├── place.json
    └── images
        ├── image1.webp
        └── image2.png

#### `place.json`

C'est le fichier qui décrit l'établissement. Il est au format json donc attention à bien entourer les valeurs avec des " et non '.

Un exemple `place_template.json` peut être trouvé dans le dossier `crieur`.

    place.json
        ├── available
        ├── name
        ├── style
        ├─ ─ banner
        ├─ ─ front
        ├─ ─ description
        ├── types
        |   ├── type1
        |   ├── type2
        ├── priceTag
        ├── price
        ├─ ─ tags
        ├─ ─ tips
        ├─ ─ tops
        ├─ ─ links
        └── locations
            ├── location1
                ├── adresse
            |   ├── latitude
                ├── longitude
            |   ├── map
                └── horaires
            |       ├── day1
                        ├── name
            |       |   └── creneaux
                            ├── creneau1
            |       |           ├── start
                            |   └── end
            |       |       
            


##### Variables
| Nom | Obligatoire | Type | Description |
| --- | --- | --- | --- |
| `available` | `true` | boolean | Page disponible si `true`, cachée si `false`  |
| `name`| `true` | text | Nom de l'établissement |
| `style` | `true` | text | Style de l'établissemnt (résumé) Exemple : "Bar à tacos" ou "Pizzeria"  | 
| `banner` | `false` | text | Nom du fichier de l'image de la bannière de la page (en haut) |
| `front` | `false` | text | Nom du fichier de l'image de la devanture (affichée sur la page et dans le slider des établissements) |
| `description`| `false` | text | Description de l'établissement |
| `types`| `true` | list of text | Liste des types de l'établissemnt (au moins un) (voir [Paramètres du Crieur - Types](#types)) ex : ["restaurant", "bar"] |
| `priceTag`| `true` | int | Catégorie de prix de l'établissemnt (voir [Paramètres du Crieur - priceTag](#pricetag)) ex : 2 |
| `price`| `true` | text | Valeur textuelle au choix qui décrit la fourchette de prix. ex : "~25 CHF" ou "10-15 CHF"  |
| `tags`| `false` | list of text | Liste des tags de l'établissemnt (voir [Paramètres du Crieur - Tags](####tags)) ex : ["vege", "takeaway"] |
| `tips`| `false` | text | Paragraphe donnant des conseils/astuces |
| `tops`| `false` | list of tops | Liste de recommandations (voir [Paramètres top](#parametres-top)) |
| `links`| `false` | list of links | Liste des liens de l'établissement (voir [Paramètres link](#parametres-link)) |
| `locations`| `true` | list of location | Liste des localisations de l'établissement (voir [Paramètres location](#parametres-location)) |


###### Paramètres `top`
| Nom | Obligatoire | Type | Description |
| --- | --- | --- | --- |
| `social` | `true` | text | Nom du réseau social. ex : "facebook"  |
| `url`| `true` | text | Lien |

###### Paramètres `link`
| Nom | Obligatoire | Type | Description |
| --- | --- | --- | --- |
| `social` | `true` | text | Nom du réseau social. ex : "facebook"  |
| `url`| `true` | text | Lien |


###### Paramètres `location`
| Nom | Obligatoire | Type | Description |
| --- | --- | --- | --- |
| `adresse` | `true` | text | Nom de la recommandation. ex : "Tiramisu"  |
| `latitude`| `true` | float  | Nom du fichier de l'image de la recommandation |
| `longitude` | `true` | float | Description de la recommandation  | 
| `map` | `true` | text | Lien de la source de la Google Map (voir ci-dessous) |
| `horaires` | `true` | list of horaire | Liste des horaires par jour (exemple ci-dessous) |

**Exemple de liste d'horaires**
```
"horaires": [
    {
        "name": "Lundi",
        "creneaux": [
            {
                "start": "12:00",
                "end": "15:30"
            },
            {
                "start": "19:00",
                "end": "22:30"
            }
        ]
    },
    ...
]
```


**Lien source Google Map**

Allez sur [Google Maps](https://maps.google.com), chercher l'adresse voulue puis cliquez sur "Partager" -> "Intégrer une carte" -> "Copier le contenu HTML". Dans le contenu copier il ne faut garder que l'url de l'attribut src.

Exemple de contenu HTML :
```
<iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d1089.5689930661053!2d6.628094727093368!3d46.51717774664765!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x478c2fe53ca8db4b%3A0xebd2430627039f06!2stibits!5e0!3m2!1sfr!2sch!4v1677016573711!5m2!1sfr!2sch" width="600" height="450" style="border:0;" allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
```
et le lien à copier dans `place.json` :  
```
https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d1089.5689930661053!2d6.628094727093368!3d46.51717774664765!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x478c2fe53ca8db4b%3A0xebd2430627039f06!2stibits!5e0!3m2!1sfr!2sch!4v1677016573711!5m2!1sfr!2sch
```

#### Ajouter des images

Pour ajouter des images pour l'établissement il faut simplement les mettre dans un dossier `images` dans le dossier de l'établissement et ensuite référencer leurs noms dans `place.json`.

MERCI de bien les compresser avant x_x

Tous les formats sont pris en charges néanmoins de recommande le format `.webp` qui est mieux pris en charge par les navigateurs.

### Supprimer un établissement

Pour retirer un établissement rien de plus simple, il faut juste supprimer le fichier `place.json` ou carrément supprimer le dossier de l'établissement !

### Paramètres du Crieur

Les paramètres du Crieur sont modifiables dans le fichier `config_crieur.json`.

    config_crieur.json
    ├── types
    ├── links
    └── tags

#### Types
Liste les différents types possibles d'établissement. Utilisé notamment pour les filtres de la carte.

##### Paramètres types
| Nom | Obligatoire | Type | Description |
| --- | --- | --- | --- |
| `code` | `true` | text | Code utilisé pour référencer le type (celui à mettre dans `place.json`)  |
| `name` | `true` | text | Nom affiché  |
| `icon` | `true` | text | Code HTML de l'icône (voir [Ajouter un icône](#ajouter-un-icone)) |

#### Tags
Liste les différents tags possibles d'établissement.

##### Paramètres tags
| Nom | Obligatoire | Type | Description |
| --- | --- | --- | --- |
| `code` | `true` | text | Code utilisé pour référencer le tag (celui à mettre dans `place.json`)  |
| `name` | `true` | text | Nom affiché  |
| `icon` | `true` | text | Code HTML de l'icône (voir [Ajouter un icône](#ajouter-un-icone)) |

#### Links
Liste les différents réseaux sociaux possibles.

##### Paramètres links
| Nom | Obligatoire | Type | Description |
| --- | --- | --- | --- |
| `social` | `true` | text | Code utilisé pour référencer le social (celui à mettre dans `place.json`)  |
| `icon` | `true` | text | Code HTML de l'icône (voir [Ajouter un icône](#ajouter-un-icone)) |

#### priceTag
Liste les différentes fourchettes de prix possibles.

- 1 = $
- 2 = $$
- 3 = $$$
- 4 = $$$$

#### Ajouter un icône 

Les icônes utilisés sont ceux de Font Awesome (version 6.3.0) et uniquement ceux *gratuits*, et *solid* ou *brand*. Pour voir la liste c'est à ce [lien](https://fontawesome.com/search?o=r&m=free).

Il suffit ensuite de copier le code HTML. Exemple : "<i class='fa-solid fa-user'></i>" (attention à bien mettre des ' ' à l'intérieur des " ")


## Articles

### Ajouter un article

Rien de plus simple, il faut juste créer un fichier `.yaml` avec le code de l'article souhaité (ex: `recette-02-2023`).

Attention le format .yaml est sensible aux tabulations des valeurs (voir [Synthaxe YAML](https://docs.ansible.com/ansible/latest/reference_appendices/YAMLSyntax.html)).

Il existe 2 types d'articles :
- Article de contenu : article avec une page dédiée (et donc avec contenu)
- Article de redirection : article sans page dédiée (et donc sans contenu) qui redirige juste vers une url

#### Variables
| Nom | Obligatoire | Type | Description |
| --- | --- | --- | --- |
| `available` | `true` | boolean | Article disponible si `true`, cachée si `false`  |
| `title`| `true` | text | Titre de l'article |
| `date`| `true` | text | Valeur de la date au format YYYY-MM-DDTHH:mm:ss.ms+01:00  |
| `code`| `true` | text | Code de l'article |
| `thumbnail` | `true` | text | Nom du fichier de l'image associée à l'article |
| `summary`| `true` | text | Description courte de l'article |
| `content`| `false` | text | Contenu HTML de l'article (inutile si article de redirection) |
| `url`| `false` | text | Url de redirection (inutile si article de contenu) |

### Supprimer un article

Pour retirer un article rien de plus simple, il faut juste supprimer le fichier `.yaml` ou alors le rendre indisponible avec `available` égal à `false`.
