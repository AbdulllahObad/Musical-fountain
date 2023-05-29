import librosa
import numpy as np
from matplotlib import pyplot as plt, animation
import pygame
from tkinter import Tk, Button
from tkinter.filedialog import askopenfilename
import random
import math

def animate(i):
    for j, b in enumerate(bar_collection):
        b.set_height(hauteurs[i][j])

    return bar_collection

# Fonction pour lancer la chanson avec pygame
def play_music():
    pygame.mixer.music.play()

def dixaine_proche(nombre):
    return round(nombre / 10) * 10

def random_math_function():
    functions = [math.sin, math.cos, math.tan, math.sqrt, math.exp, math.log10]
    return random.choice(functions)

def tri_tableau(tableau):
    tableau.sort(reverse=True)  # tri du tableau dans l'ordre décroissant
    n = len(tableau)
    milieu = n // 2  # indice du milieu du tableau
    resultat = [0] * n  # création d'un tableau vide pour le résultat

    # Placement des valeurs dans le résultat
    for i in range(n):
        distance = abs(i - milieu)
        resultat[i] = dixaine_proche(tableau[i] * (n - distance) / n)

    return resultat

def tri_tableau_croi(tableau):
    tableau.sort()  # tri du tableau dans l'ordre croissant
    n = len(tableau)
    milieu = n // 2  # indice du milieu du tableau
    resultat = [0] * n  # création d'un tableau vide pour le résultat
    
    # Placement des valeurs dans le résultat
    for i in range(n):
        distance = abs(i - milieu)
        resultat[i] = dixaine_proche(tableau[i] * (n - distance) / n)

    return resultat

# Initialiser pygame
pygame.mixer.init()

# Charger le fichier audio
root = Tk()
root.withdraw()
audio_path = askopenfilename()
y, sr = librosa.load(audio_path)

# Charger la chanson avec pygame
pygame.mixer.music.load(audio_path)

# Détecter les onsets dans la chanson
onset_frames = librosa.onset.onset_detect(y=y, sr=sr)

# Nombre d'onsets dans la chanson
n_onsets = len(onset_frames)

# Calcul du chromagramme
chroma = librosa.feature.chroma_stft(y=y, sr=sr, n_fft=2048, hop_length=512)

# Sélection des temps pertinents
temps = librosa.frames_to_time(onset_frames, sr=sr, hop_length=512)

# Sélection des colonnes du chromagramme correspondant aux temps pertinents
chroma = chroma[:, onset_frames]

# Normalisation du chromagramme
chroma_norm = librosa.util.normalize(chroma, norm=2, axis=0)

# Initialiser la liste de hauteurs avec les valeurs du chromagramme
hauteurs = [[] for _ in range(n_onsets)]

for i in range(n_onsets):
    random_number = random.randint(0,9)
    for j in range(12):
        hauteur = int (chroma_norm[j,i]*100)
        hauteurs[i].append(hauteur)
    if random_number==0:
       tri_tableau(hauteurs[i])
    elif random_number==1:
        tri_tableau_croi(hauteurs[i])
    elif random_number==2:
        max_value = sum(hauteurs[i])/len(hauteurs[i])
        fonction = random_math_function()
        hauteurs[i] = [dixaine_proche(hauteurs[i][k]*pow(math.cos(i),hauteurs[i][k])) for k in range(len(hauteurs[i]))]
    else:
        max_value = sum(hauteurs[i])/len(hauteurs[i])
        fonction = random_math_function()
        hauteurs[i] = [dixaine_proche(hauteurs[i][k]*pow(math.sin(i),hauteurs[i][k])) for k in range(len(hauteurs[i]))]

fig, ax = plt.subplots()
plt.ylim(0, 1)
ax.set_ylim(0, 1)
plt.xlim(0, 13)

bar_collection = ax.bar(range(1, 13), [0]*12, align='center', linewidth=0.5)

# La durée d'une frame en millisecondes est égale à la moyenne des intervalles de temps entre chaque onset multipliée par 1000 pour avoir des millisecondes
frame_duration = np.mean(np.diff(temps))*1000

def animate(i):
    for j, b in enumerate(bar_collection):
        b.set_height(hauteurs[i][j])
    return bar_collection

# Fonction pour lancer la chanson avec pygame
def play_music():
    pygame.mixer.music.play()
play_music()

# Définir les paramètres de l'animation
anim = animation.FuncAnimation(fig, animate, frames=n_onsets, interval=frame_duration, blit=True)

anim.repeat = False
plt.show()