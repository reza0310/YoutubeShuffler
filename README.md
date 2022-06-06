# YoutubeShuffler

# Description
Un patch pour lire des playlist Youtube de façon réellement aléatoire

# Important
Si vous utilisez une version non compilée, dans [environnement python]\site-packages\selenium\webdriver\common\service.py ajoutez "+0x08000000" après "self.creationflags" ligne 76 pour vous débarasser de la console (https://stackoverflow.com/questions/57984953/how-to-hide-geckodriver-console-window).

# Utilisation
Flemme de faire une bonne doc donc je vais être conçis: Tout se contrôle depuis le fichier config.json et avec des raccourcis clavier.
1) DOC: Booléenne en fonction de si vous voulez que le programme vous ouvre cette doc à côté ou pas
2) AUTO_PLAYLIST: Mettez l'identifiant d'une playlist si vous voulez y être redirigé automatiquement à l'ouverture de l'app sinon mettez "null"
3) CLEF_API: Mettez-y une clef d'API Youtube (déso mais mes quotats sont trop limités pour être publiée) (https://console.cloud.google.com/apis/dashboard)
4) TOUCHES:
   - SPECIALE: La touche à appuyer en plus des autres (pour savoir quels raccourcis lire et lesquels ignorer)
   - LANCER: La touche à appuyer quand vous êtes sur la page de votre playlist (page sur laquelle envoie le truc automatique) pour l'analyser et lancer le mode aléatoire
   - SKIP: La touche à appuyer pour passer la musique actuelle
   - PAUSE: La touche à appuyer pour mettre en pause / reprendre la vidéo (et faire suivre le timer)
   - QUITTER: La touche à appuyer pour tout quitter proprement

# Problèmes
1) Fiabilité
2) Choisir la playlist plus simplement qu'en modifiant du JSON
