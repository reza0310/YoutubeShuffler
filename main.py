import random
import threading
from selenium import webdriver
import keyboard
import json
import time
import googleapiclient.discovery
from urllib.parse import parse_qs, urlparse
from pyvirtualdisplay import Display
import pywin


class Overtimer:

    def __init__(self, duration, callback):
        self.duration = duration
        self.callback = callback
        self.timer = threading.Timer(duration, callback)

    def start(self):
        self.start_time = time.time()
        self.timer.start()

    def stop(self):
        print("STOPPING TIMER")
        self.timer.cancel()
        self.duration -= (time.time() - self.start_time)

    def go(self):
        self.timer = threading.Timer(self.duration, self.callback)
        self.start()

    def cancel(self):
        self.timer.cancel()


class Shuffler:

    def __init__(self):
        self.load()

        # Initialisation du navigateur
        options = webdriver.FirefoxOptions()
        options.add_argument("--headless")
        self.driver = webdriver.Firefox(options=options)
        if self.CONFIG["DOC"]:
            self.driver.get("https://github.com/reza0310/YoutubeShuffler/blob/main/README.md#utilisation")
            self.driver.execute_script("window.open('');")
            self.driver.switch_to.window(self.driver.window_handles[1])
        self.driver.get("https://www.youtube.com/")
        self.driver.maximize_window()
        self.driver.find_element_by_css_selector('ytd-button-renderer.style-primary:nth-child(1) > a:nth-child(1) > tp-yt-paper-button:nth-child(1)').click()

        self.set_hotkeys()

        # Automatisation
        if self.AUTO_PLAYLIST != None:
            self.driver.get("https://www.youtube.com/playlist?list=" + self.AUTO_PLAYLIST)
            self.preparer()

        self.loop()

    def set_hotkeys(self):
        # Ajout des raccourcis pour exécuter les fonctions de manipulation du script
        keyboard.add_hotkey(self.TOUCHE_SPECIALE + "+" + self.TOUCHE_QUITTER, self.quitter)
        keyboard.add_hotkey(self.TOUCHE_SPECIALE + "+" + self.TOUCHE_LANCER, self.preparer)
        keyboard.add_hotkey(self.TOUCHE_SPECIALE + "+" + self.TOUCHE_SKIP, self.skip)
        keyboard.add_hotkey(self.TOUCHE_SPECIALE + "+" + self.TOUCHE_PAUSE, self.pauser)
        keyboard.add_hotkey(self.TOUCHE_SPECIALE + "+" + self.TOUCHE_CACHER, self.cacher)

    def loop(self):
        # Bloquer la fermeture du script (Merci SPEEDY)
        while self.QUITTER:
            if self.pause:
                continue
            elif self.go:
                self.go = False
                self.timer = Overtimer(self.lancer() + 8, self.rego)  # Le +7 c'est pour la pub
                self.timer.start()

    def load(self):
        # Chargement des configs
        self.CONFIG = json.load(open("config.json"))
        self.TOUCHE_SPECIALE = self.CONFIG["TOUCHES"][0]["SPECIALE"]
        self.TOUCHE_SKIP = self.CONFIG["TOUCHES"][0]["SKIP"]
        self.TOUCHE_LANCER = self.CONFIG["TOUCHES"][0]["LANCER"]
        self.TOUCHE_QUITTER = self.CONFIG["TOUCHES"][0]["QUITTER"]
        self.TOUCHE_PAUSE = self.CONFIG["TOUCHES"][0]["PAUSE"]
        self.TOUCHE_CACHER = self.CONFIG["TOUCHES"][0]["CACHER"]
        self.AUTO_PLAYLIST = self.CONFIG["AUTO_PLAYLIST"]
        self.QUITTER = True
        self.go = False
        self.pause = False
        self.cache = False
        self.playlist_items = {}

    def lancer(self):
        choix = random.choice(list(self.playlist_items.keys()))
        self.driver.get("https://www.youtube.com/watch?v=" + choix)
        try:
            self.driver.find_element_by_css_selector(".ytp-large-play-button").click()
            tmp = threading.Timer(7, self.skip_pub)
            tmp.start()
            print(f"On joue {self.driver.title} ({self.driver.current_url})")
        except:
            print("Vidéo supprimée, nécessitant d'être connecté, interdite aux mineurs, fenêtre en arrière plan ou autre couilleS")
            self.skip()
        return self.playlist_items[choix]["FIN"]

    def rego(self):
        self.go = True

    def skip_pub(self):
        try:
            self.driver.find_element_by_css_selector(".ytp-ad-skip-button-container").click()
            print("Pub passée")
        except:
            print("Pas de pub!")

    # Définition des fonctions de manipulation du script
    def quitter(self):
        try:
            self.driver.stop_client()
            self.driver.close()
            self.driver.quit()
        except:
            print("Navigateur déjà fermé")
        self.QUITTER = False

    def preparer(self):
        print("Début de la préparation")
        PLAYLIST = self.driver.current_url

        # https://stackoverflow.com/questions/62345198/extract-individual-links-from-a-single-youtube-playlist-link-using-python
        query = parse_qs(urlparse(PLAYLIST).query, keep_blank_values=True)
        playlist_id = query["list"][0]
        youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=self.CONFIG["CLEF_API"])
        request = youtube.playlistItems().list(
            part="contentDetails",
            playlistId=playlist_id,
            maxResults=50)
        total = request.execute()['pageInfo']['totalResults']
        self.playlist_items = json.load(open("times.json"))
        k = 1
        while request is not None:
            response = request.execute()

            # https://github.com/CoreyMSchafer/code_snippets/blob/master/Python/YouTube-API/02-Playlist-Duration/playlist.py
            for i in range(len(response["items"])):
                id = response['items'][i]['contentDetails']['videoId']
                if id not in self.playlist_items.keys():
                    try:
                        vid_request = youtube.videos().list(
                            part="contentDetails",
                            id=id
                        )
                        durees = self.formater_durees(vid_request.execute()['items'][0]['contentDetails']['duration'])
                        self.playlist_items[id] = {"DEBUT": 0, "FIN": durees}
                        print("NOUVEAU")
                    except:
                        print("Vidéo supprimée")
                # Afficher une barre sur mon site web
                print(k, "/", total)
                k += 1
            request = youtube.playlistItems().list_next(request, response)
        with open("times.json", "w") as t:
            t.write(json.dumps(self.playlist_items).replace("}, ", "},\n"))
        print("Préparation terminée")
        self.go = True

    def skip(self):
        print("Commande skip reçue")
        self.timer.cancel()
        self.go = False
        self.timer = Overtimer(self.lancer() + 7, self.rego)  # Le +7 c'est pour la pub
        self.timer.start()

    def pauser(self):
        print("Commande pause reçue")
        if self.pause:
            print("Reprise")
            self.timer.go()
            self.pause = False
        else:
            print("Mise en pause")
            self.timer.stop()
            self.pause = True
        self.driver.find_element_by_css_selector(".video-stream").click()

    def cacher(self):
        if self.cache:
            self.cachette.stop()
            print(pywin.EnumWindows())
            self.cache = False
        else:
            self.cachette.start()
            print(pywin.EnumWindows())
            self.cache = True

    # Fonctions utiles
    @staticmethod
    def formater_durees(texte):
        contient_minutes = "M" in texte
        contient_heures = "H" in texte
        if "S" not in texte:
            texte += "0S"
        if contient_heures and not contient_minutes:
            raise Exception("Là mec tu casse les couilles...")
        texte = texte.replace("PT", "").replace("S", "").split("M")
        if contient_heures:
            secondes = int(texte[1])
            heures, minutes = texte[0].split("H")
            secondes += int(heures) * 3600 + int(minutes) * 60
        elif contient_minutes:
            secondes = int(texte[1])
            minutes = int(texte[0])
            secondes += minutes * 60
        else:
            secondes = int(texte[0])
        return secondes

if __name__ == "__main__":
    Shuffler()