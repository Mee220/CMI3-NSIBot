import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from neuronal_network import *
#from io_data import *

xAll = np.array([ [0, 0, 0],
                  [0, 0, 1],
                  [0, 1, 0],
                  [0, 1, 1],
                  [1, 0, 0],
                  [1, 0, 1],
                  [1, 1, 0],
                  [1, 1, 1]
                  ])

xAll = xAll/np.amax(xAll, axis=0) # scaling input data
# scaling output data (max test score is 100)

# split data
X = np.split(xAll, [8])[0] # training data
xPredicted = np.split(xAll, [8])[0] # testing data

test=np.array([[0, 1, 1]])

stop = False

def create_numpy_array():
    # Récupérer les valeurs sélectionnées dans les Combobox
    values = []
    for row in range(8):
        mg_value = combo_vars[row][0].get()
        md_value = combo_vars[row][1].get()
        values.append([float(mg_value), float(md_value)])

    # Créer le tableau NumPy
    y = np.array(values)
    return y

def train():
    global stop
    stop = False
    try:
        log("Starting training...\n")

        # Create NN and user-defined output array
        NN = Neural_Network()
        y = create_numpy_array()

        log("Using user-defined output from table:\n")
        log(str(y) + "\n")

        i = 0
        loss = np.mean(np.square(y - NN.forward(X)))

        while i < 200000 and loss > 0.00004:
            if i % 1000 == 0:
                log(f"Iteration {i} | Loss: {loss:.6f}\n")
            NN.train(X, y)
            i += 1
            loss = np.mean(np.square(y - NN.forward(X)))

        if loss <= 0.00004:
            log(f"Training completed in {i} iterations.\n")
            log(f"Final Loss: {loss:.6f}\n")
            NN.saveWeights()
            log("Weights saved to Weights.h\n")
            log("Predicted output (for verification):\n")
            log(str(NN.forward(X)) + "\n")
        else:
            log("Training failed to converge. Try different values.\n")

        del NN
    except Exception as e:
        log(f"Error during training: {e}\n")

def stop_train():
    #global stop
    stop = True  # Mettre stop à True pour arrêter l'entraînement
    log("Training stop requested.\n")

def log(message):
    # Ajouter un message au champ de texte des logs
    log_text.config(state=tk.NORMAL)  # Activer l'édition
    log_text.insert(tk.END, message)
    log_text.config(state=tk.DISABLED)  # Désactiver l'édition
    log_text.see(tk.END)  # Faire défiler jusqu'au dernier message


def create_table(root):
    global combo_vars
    combo_vars = []

    # Créer un cadre pour contenir la table
    frame = tk.Frame(root)
    frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
    # Créer les en-têtes de colonne
    headers = ["G", "A", "D", "MG", "MD"]
    for col, header in enumerate(headers):
        label = tk.Label(frame, text=header, relief=tk.RIDGE, width=15)
        label.grid(row=0, column=col, sticky="nsew")

    # Ajouter les combinaisons binaires et les options pour MG et MD
    for i in range(8):
        binary_combination = format(i, '03b')  # Convertir l'entier en binaire sur 3 bits
        row_vars = []
        for col, value in enumerate(binary_combination):
            label = tk.Label(frame, text=value, relief=tk.RIDGE, width=15)
            label.grid(row=i+1, column=col, sticky="nsew")

        # Ajouter des menus déroulants pour MG et MD
        for col, header in enumerate(headers[3:], start=3):
            var = tk.StringVar(value="0.0")
            combo = ttk.Combobox(frame, textvariable=var, values=["0.0", "0.5", "1.0"], width=13)
            combo.grid(row=i+1, column=col, sticky="nsew")
            row_vars.append(var)

        combo_vars.append(row_vars)

def create_interface():
    global log_text

    # Créer la fenêtre principale
    root = tk.Tk()
    root.title("Interface d'Entraînement")
    root.geometry("750x600")  # Définir la taille initiale de la fenêtre

    # Créer la table
    create_table(root)

    # Ajouter un champ de texte pour les logs
    log_frame = tk.Frame(root)
    log_frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=5)
    log_text = tk.Text(log_frame, height=10, state=tk.DISABLED)
    log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Ajouter une barre de défilement pour le champ de texte
    scrollbar = tk.Scrollbar(log_frame, command=log_text.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    log_text['yscrollcommand'] = scrollbar.set

    # Ajouter les boutons Entrainer et Stop
    button_frame = tk.Frame(root)
    button_frame.pack(pady=20)

    train_button = tk.Button(button_frame, text="Entrainer", command=train)
    train_button.pack(side=tk.LEFT, padx=5)

    stop_button = tk.Button(button_frame, text="Stop", command=stop_train)
    stop_button.pack(side=tk.LEFT, padx=5)

    # Lancer la boucle principale de l'interface
    root.mainloop()


# Exécuter la fonction pour créer l'interface
create_interface()