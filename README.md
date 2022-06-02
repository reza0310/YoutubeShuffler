# YoutubeShuffler

# Description
Un patch pour lire des playlist Youtube de façon réellement aléatoire

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
1) L'affichage dans la console est problématique
2) Marche pas en arrière plan
3) La fonction de préparation rame sa mère même quand on a déjà les données
4) J'ai claqué mon quotat d'API
5) Geckodriver ouvre une console inutile
6) Fermer avec la croix ferme pas tout
7) Pause pas testée
8) Interagir directement avec le navigateur après lancement peut tout casser
