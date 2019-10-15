import os
import subprocess
import random
import time
import threading
import tkinter as tk
import tkinter.ttk
from tkinter import *
from tkinter import filedialog
from collections import namedtuple
from PIL import Image, ImageTk
import pandas as pd

initw = 1000
inith = 450

contents = []
input_field = ""
max_field = ""
size_field = ""
result_field = ""
time_field = ""
file_path = ""
v = ""
heuristic_variable = ""
meta_variable = ""

hyper = ""

meta_options = [
    "Choisir Une Méta",
    "AG",
    "RS"
]

heuristic_options = [
    "Choisir Une Heuristique",
    "First Fit",
    "Next Fit",
    "Best Fit",
    # "Worst Fit",
    "Max Rest",
    # "Full Bin",
    "Random"
]


def binPacking(n, tab, Poid_Max, minBoites):
    Node = namedtuple("Node", "level conf poidRest")
    Nodes = []
    u = Node(1, [1], [Poid_Max - tab[0]])  # le premier noeud on met le premier objet
    Nodes.append(u)
    while len(Nodes) > 0:
        u = Nodes.pop()
        if u.level == n and max(
                u.conf) < minBoites:  # si il s'agit d'un noeud feuille et que cette configuration contient moins de boites que les configurations trouvé jusqu'à à present alors je sauvegarde
            minBoites = max(u.conf)
            minConf = u.conf.copy()
        if u.level < n and max(
                u.conf) < minBoites:  # sinon si ce n'est pas un noeud feuille et que cette configuration est suscéptible de contenir la solution optimal
            nbFils = max(
                u.conf)  # ce noeud en réalité va créer nbFils+1 , mais le dernier fils étant un cas particulier(car dans ce fils l'element va se mettre dans un nouveau bin) alors je traiterais ce cas en dehors de la boucle
            element = u.level  # le niveau courant represente l'index de l'element(l'objet) courant
            for j in range(nbFils):
                if tab[element] <= u.poidRest[
                    j]:  # si il ya assez de place pour l'element dans le bin je le met et je crée un nouveau noeud
                    a = u.conf.copy()
                    a.append(j + 1)
                    if max(a) < minBoites:
                        poidRest = u.poidRest.copy()
                        poidRest[j] -= tab[element]
                        v = Node(u.level + 1, a, poidRest)
                        Nodes.append(v)

            if max(u.conf) + 1 < minBoites:
                u.conf.append(max(u.conf) + 1)
                u.poidRest.append(Poid_Max - tab[element])
                v = Node(u.level + 1, u.conf,
                         u.poidRest)  # dans ce noeud je met l'element ( objet ) dans un nouveau bin d'ou le (u.conf.append(max(u.conf)+1))
                Nodes.append(v)
    return minBoites  # l'algorithme branch and bound


def first_fit(tab):
    cpt = 1
    c = int(tab[cpt])
    cpt += 1
    bins = []
    continuer = True
    bin = 1
    bins.append(c)
    while continuer:
        x = int(tab[cpt])
        cpt += 1
        i = 0
        while i < bin:
            if bins[i] >= x:
                bins[i] = bins[i] - x
                break
            i += 1
        if i == bin:
            bin += 1
            bins.append(c - x)
        if cpt > tab[0] + 1:
            continuer = False
    return bin


def next_fit(tab):
    cpt = 1
    c = int(tab[cpt])
    cpt += 1
    bins = []
    continuer = True
    bin = 1
    bins.append(c)
    i = 0
    while continuer:
        x = int(tab[cpt])
        # print(x, end =' ')
        cpt += 1
        if bins[i] >= x:
            bins[i] = bins[i] - x
        else:
            i += 1
            bin += 1
            bins.append(c - x)
        if cpt > tab[0] + 1:
            continuer = False
    return bin


def best_fit(tab):
    cpt = 1
    c = int(tab[cpt])
    cpt += 1
    bins = []
    continuer = True
    bin = 1
    bins.append(c)
    while continuer:
        x = int(tab[cpt])
        cpt += 1
        bi = 0
        min = c + 1
        for i in range(0, bin):
            if bins[i] >= x and bins[i] - x < min:
                bi = i
                min = bins[i] - x
        if min == c + 1:
            bins.append(c - x)
            bin += 1
        else:
            bins[bi] = bins[bi] - x
        if cpt > tab[0] + 1:
            continuer = False
    return bin


def worst_fit(tab):
    cpt = 1
    c = int(tab[cpt])
    cpt += 1
    bins = []
    continuer = True
    bin = 1
    bins.append(c)
    while continuer:
        x = int(tab[cpt])
        cpt += 1
        bi = 0
        max = -1
        for i in range(0, bin):
            if bins[i] >= x and bins[i] - x > max:
                bi = i
                max = bins[i] - x
        if max == -1:
            bins.append(c - x)
            bin += 1
        else:
            bins[bi] = bins[bi] - x
        if cpt > tab[0] + 1:
            continuer = False
    return bin


def max_rest(tab):
    nb_objects = tab[0]
    max_size = tab[1]
    bins = 0
    rests = []
    objects = []
    for i in range(0, nb_objects):
        objects.append(0)
        rests.append(0)
    rests[bins] = max_size
    index_max = 0
    for i in range(2, len(tab)):
        objects[i - 2] = tab[i]
    for i in range(0, len(objects)):
        max_value = 0
        for j in range(0, len(rests)):
            if rests[j] > max_value:
                max_value = rests[j]
                index_max = j
        if objects[i] <= rests[index_max]:
            rests[index_max] = rests[index_max] - objects[i]
        else:
            bins += 1
            rests[bins] = max_size - objects[i]
    return bins + 1


def randomize(tab):
    bins = []
    c = int(tab[1])
    bins.append(c)
    random_list = []

    def not_browsed_yet(i):
        for single_random in random_list:
            if single_random == i: return False
        return True

    def gen_random():
        i = random.randint(2, len(tab) - 1)
        while not not_browsed_yet(i):
            i = random.randint(2, len(tab) - 1)
        return i

    while len(random_list) < tab[0]:
        index = gen_random()
        random_list.append(index)
        fit = False
        for j in range(0, len(bins)):
            if bins[j] > tab[index]:
                bins[j] -= tab[index]
                fit = True
        if not fit:
            bins.append(c)
            bins[len(bins) - 1] -= tab[index]
    return len(bins)


def open_file(event):
    global choose_instance
    global file_path
    global contents
    path = os.getcwd() + "\Scholl"
    # path = "D:\\Desktop\\bin-packing-hyper-heuristics\\datasets"
    file_path = filedialog.askopenfilename(initialdir=path, title='Choose Instance',
                                           filetypes=[("Text Files", "*.txt *.csv *.bpp")])
    if file_path == "":
        print("Empty File")
    else:
        # form = os.path.splitext(file_path)[1]
        choose_instance.config(text=os.path.split(file_path)[1])
        f = open(file_path, "r")
        contents = list(map(int, f.read().splitlines()))
        tab = contents[2:]
        max_field.config(state=NORMAL)
        size_field.config(state=NORMAL)
        input_field.config(state=NORMAL)
        result_field.config(state=NORMAL)
        time_field.config(state=NORMAL)
        max_field.delete('1.0', END)
        size_field.delete('1.0', END)
        input_field.delete('1.0', END)
        result_field.delete('1.0', END)
        time_field.delete('1.0', END)
        non_optimal_label.place_forget()
        optimal_label.place_forget()
        optimal_result_label.place_forget()
        chosen_heuritic_label.place_forget()
        max_field.insert(END, contents[1])
        size_field.insert(END, contents[0])
        str = ''
        for i in tab:
            if len(str) % 80 > 75:
                for j in range(len(str) % 80, 80):
                    str += ' '
            str += '%d' % i + ' '
        input_field.insert(END, str)
        max_field.config(state=DISABLED)
        size_field.config(state=DISABLED)
        input_field.config(state=DISABLED)
        result_field.config(state=DISABLED)
        time_field.config(state=DISABLED)


def show_result(result, timing):
    time_field.config(state=NORMAL)
    result_field.config(state=NORMAL)
    # time_field.delete('1.0', END)
    # result_field.delete('1.0', END)
    time_field.insert(END, '%.3f' % timing + ' s')
    if not result.isdigit():
        result_field.insert(END, result)
    else:
        result = int(result)
        result_field.insert(END, '%d' % result)
    time_field.config(state=DISABLED)
    result_field.config(state=DISABLED)
    data = pd.read_csv('datasets.csv')
    if v.get() == 4:
        non_optimal_label.place_forget()
    else:
        for index, row in data.iterrows():
            if row['file_name'] == choose_instance.cget('text').split('.')[0]:
                # print(row['value'])
                if row['value'] == result:
                    non_optimal_label.place_forget()
                    optimal_label.config(text="OPTIMAL!", fg="green")
                    optimal_label.place(x=570, y=280)
                    optimal_result_label.config(text="Résultat Optimal : " + str(row['value']))
                    optimal_result_label.place(x=570, y=340)
                    if v.get() == 4:
                        chosen_heuritic_label.config(text="Heuritique Choisie: " + hyper[-2:])
                        chosen_heuritic_label.place(x=500, y=360)
                else:
                    non_optimal_label.config(text="Non", fg="red")
                    non_optimal_label.place(x=600, y=250)
                    optimal_label.config(text="OPTIMAL!", fg="red")
                    optimal_label.place(x=570, y=290)
                    optimal_result_label.config(text="Résultat Optimal : " + str(row['value']))
                    optimal_result_label.place(x=570, y=340)
                    if v.get() == 4:
                        chosen_heuritic_label.config(text="Heuritique Choisie: " + hyper[-2:])
                        chosen_heuritic_label.place(x=500, y=360)
                break


def do_exact_method():
    start_time = time.time()
    minimum = binPacking(contents[0], contents[2:], contents[1], contents[2])
    end_time = time.time()
    show_result(str(minimum), end_time - start_time)


def do_heuristic_method():
    if heuristic_variable.get() == 'First Fit':
        start_time = time.time()
        minimum = first_fit(contents)
        end_time = time.time()
        show_result(str(minimum), end_time - start_time)
    elif heuristic_variable.get() == 'Next Fit':
        start_time = time.time()
        minimum = next_fit(contents)
        end_time = time.time()
        show_result(str(minimum), end_time - start_time)
    elif heuristic_variable.get() == 'Best Fit':
        start_time = time.time()
        minimum = best_fit(contents)
        end_time = time.time()
        show_result(str(minimum), end_time - start_time)
    elif heuristic_variable.get() == 'Max Rest':
        # args = 'main3.exe '
        # for arg in contents:
        #     args += str(arg) + ' '
        # start_time = time.time()
        # out = subprocess.getoutput(args)
        # end_time = time.time()
        # minimum = int(out)
        # print(minimum)
        # show_result(str(minimum), end_time - start_time)
        start_time = time.time()
        minimum = max_rest(contents)
        end_time = time.time()
        show_result(str(minimum), end_time - start_time)
    # elif heuristic_variable.get() == "Worst Fit":
    #     start_time = time.time()
    #     minimum = worst_fit(contents)
    #     end_time = time.time()
    #     show_result(str(minimum), end_time - start_time)
    # elif heuristic_variable.get() == "Full Bin":
    #     start_time = time.time()
    #     minimum = full_bin(contents)
    #     end_time = time.time()
    #     show_result(str(minimum), end_time - start_time)
    elif heuristic_variable.get() == "Random":
        start_time = time.time()
        minimum = randomize(contents)
        end_time = time.time()
        show_result(str(minimum), end_time - start_time)


def do_meta_method():
    if meta_variable.get() == "AG":
        f = open("AG/Constants.py", "w+")
        f.write("C=" + str(contents[1]) + "\n")
        f.write("Weights=" + str(contents[2:]) + "\n")
        f.write("n=" + str(contents[0]) + "\n")
        f.write("PopulationBegin=" + population_size.get() + "\n")
        f.write("Pm=" + mutation_rate.get() + "\n")
        f.write("nb_iteration=" + nb_iteration.get() + "\n")
        f.close()
        args = "python AG/index.py"
        start_time = time.time()
        minimum = subprocess.getoutput(args)
        end_time = time.time()
        show_result(str(minimum), end_time - start_time)
    if meta_variable.get() == "RS":
        f = open("RC/Constants.py", "w+")
        f.write("C=" + str(contents[1]) + "\n")
        f.write("Weights=" + str(contents[2:]) + "\n")
        f.write("n=" + str(contents[0]) + "\n")
        f.write("T=" + str(23194) + "\n")
        f.write("nb_iteration=" + nb_iteration.get() + "\n")
        f.close()
        args = "python RC/index.py"
        start_time = time.time()
        minimum = subprocess.getoutput(args)
        end_time = time.time()
        show_result(str(minimum), end_time - start_time)


def do_hyper_method():
    global hyper
    args = "python HH/prediction.py "
    args += str(contents[1]) + " "
    for c in contents[2:]:
        args += str(c) + " "
    start_time = time.time()
    hyper = subprocess.getoutput(args)
    end_time = time.time()
    show_result(hyper[-2:], end_time - start_time)


def exact_method_label(event):
    v.set(1)


def hyper_heuristic_label(event):
    v.set(4)


def start(event):
    global result_field
    global time_field
    if file_path != "":
        if v.get() != 0:
            non_optimal_label.config(text="Entrain de Calcule", fg="black")
            non_optimal_label.place(x=500, y=250)
            optimal_label.place_forget()
            optimal_result_label.place_forget()
            time_field.config(state=NORMAL)
            result_field.config(state=NORMAL)
            time_field.delete('1.0', END)
            result_field.delete('1.0', END)
            time_field.config(state=DISABLED)
            result_field.config(state=DISABLED)
        if v.get() == 1:
            threading.Thread(target=do_exact_method).start()
        if v.get() == 2:
            threading.Thread(target=do_heuristic_method).start()
        if v.get() == 3:
            threading.Thread(target=do_meta_method).start()
        if v.get() == 4:
            threading.Thread(target=do_hyper_method).start()


def exiting():
    os._exit(0)
    # sys.exit(0)


def callback(*args):
    if args[0] == "PY_VAR1":
        if heuristic_variable.get() != heuristic_options[0]:
            v.set(2)
        elif v.get() == 2:
            v.set(0)
    elif args[0] == "PY_VAR2":
        if meta_variable.get() != meta_options[0]:
            v.set(3)
            update_meta_params(True)
        else:
            update_meta_params(False)
            if v.get() == 3:
                v.set(0)
    # else:
    #     v.set(0)


def callback_two(*args):
    if v.get() == 2:
        if heuristic_variable.get() == heuristic_options[0]:
            v.set(0)
    if v.get() == 3:
        if meta_variable.get() == meta_options[0]:
            v.set(0)


def update_meta_params(meta):
    population_size_label.place_forget()
    mutation_rate_label.place_forget()
    nb_iteration_label.place_forget()
    temperature_label.place_forget()
    population_size.place_forget()
    mutation_rate.place_forget()
    nb_iteration.place_forget()
    if meta:
        y = 220
        if meta_variable.get() == "AG":
            population_size_label.place(x=10, y=y)
            mutation_rate_label.place(x=90, y=y)
        elif meta_variable.get() == "RS":
            temperature_label.place(x=30, y=y)
        nb_iteration_label.place(x=170, y=y)
        y += 20
        if meta_variable.get() == "AG":
            population_size.delete(0, END)
            population_size.insert(END, 8)
            population_size.place(x=20, y=y)
            mutation_rate.delete(0, END)
            mutation_rate.insert(END, 0.1)
            mutation_rate.place(x=100, y=y)
            nb_iteration.delete(0, END)
            nb_iteration.insert(END, 100)
            nb_iteration.place(x=180, y=y)
        elif meta_variable.get() == "RS":
            population_size.delete(0, END)
            population_size.insert(END, 23194)
            population_size.place(x=20, y=y)
            nb_iteration.delete(0, END)
            nb_iteration.insert(END, 2000)
            nb_iteration.place(x=180, y=y)
        y += 40
        hyper_radiobutton.place(x=10, y=y)
        hyper_label.place(x=30, y=y)
        y += 40
        separator.place(x=0, y=y, width=320, height=1)
        y += 20
        start_button.place(x=100, y=y)
        y += 50
        clear_button.place(x=125, y=y)
    else:
        y = 230
        # param.place_forget()
        hyper_radiobutton.place(x=10, y=y)
        hyper_label.place(x=30, y=y)
        y += 40
        separator.place(x=0, y=y, width=320, height=1)
        y += 20
        start_button.place(x=100, y=y)
        y += 50
        clear_button.place(x=125, y=y)


def clear(event):
    global file_path
    v.set(0)
    meta_variable.set(meta_options[0])
    heuristic_variable.set(heuristic_options[0])
    choose_instance.config(text='Choisir Une Instance')
    file_path = ""
    max_field.config(state=NORMAL)
    size_field.config(state=NORMAL)
    input_field.config(state=NORMAL)
    result_field.config(state=NORMAL)
    time_field.config(state=NORMAL)
    max_field.delete('1.0', END)
    size_field.delete('1.0', END)
    input_field.delete('1.0', END)
    result_field.delete('1.0', END)
    time_field.delete('1.0', END)
    max_field.config(state=DISABLED)
    size_field.config(state=DISABLED)
    input_field.config(state=DISABLED)
    result_field.config(state=DISABLED)
    time_field.config(state=DISABLED)
    non_optimal_label.place_forget()
    optimal_label.place_forget()


if __name__ == '__main__':
    y = 10
    top = tk.Tk()
    image = Image.open("bg.jpg")
    photo = ImageTk.PhotoImage(image)
    image = Label(top, image=photo)
    image.place(x=0, y=0, relheight=1, relwidth=1)
    top.title('Projet Optim')
    top.geometry(str(initw) + 'x' + str(inith) + '+150+150')
    top.protocol("WM_DELETE_WINDOW", exiting)
    # top.overrideredirect(1)
    top.resizable(0, 0)
    choose_instance = Label(top, text="Choisir Une Instance", bg="green", font=("Helvetica", 14, "bold"))
    choose_instance.place(x=10, y=y)
    open_file_button = Button(top, text="Parcourir", font=("Helvetica", 12, "bold"))
    open_file_button.bind('<Button-1>', open_file)
    open_file_button.place(x=220, y=y - 2)
    y += 40
    tk.ttk.Separator(top, orient=HORIZONTAL).place(x=0, y=y, width=320, height=1)
    tk.ttk.Separator(top, orient=VERTICAL).place(x=320, y=0, width=1, height=inith)
    v = IntVar()
    v.trace("w", callback_two)
    y += 20
    choose_method = Label(top, text="Choisir Une Méthode", bg="green", font=("Helvetica", 14, "bold"))
    choose_method.place(x=10, y=y)
    y += 40
    tk.Radiobutton(top,
                   text="",
                   variable=v,
                   value=1).place(x=10, y=y)
    exact_label = Label(top, text="Méthode Exacte", font=("Helvetica", 12, "bold"))
    exact_label.place(x=30, y=y)
    exact_label.bind('<Button-1>', exact_method_label)
    y += 40
    r = tk.Radiobutton(top,
                       text="",
                       variable=v,
                       value=2).place(x=10, y=y)
    heuristic_variable = StringVar(top)
    heuristic_variable.set(heuristic_options[0])
    heuristic_variable.trace("w", callback)
    choose_heuristic = OptionMenu(top, heuristic_variable, *heuristic_options)
    choose_heuristic.config(font=("Helvetica", 12, "bold"))
    choose_heuristic.place(x=30, y=y - 5)
    y += 40
    tk.Radiobutton(top,
                   text="",
                   variable=v,
                   value=3).place(x=10, y=y)
    meta_variable = StringVar(top)
    meta_variable.set(meta_options[0])
    meta_variable.trace("w", callback)
    choose_meta = OptionMenu(top, meta_variable, *meta_options)
    choose_meta.config(font=("Helvetica", 12, "bold"))
    choose_meta.place(x=30, y=y - 5)
    population_size_label = Label(top, text="Pop Size", font=("Helvetica", 10, "bold"))
    mutation_rate_label = Label(top, text="Mut Prob", font=("Helvetica", 10, "bold"))
    temperature_label = Label(top, text="T", font=("Helvetica", 10, "bold"))
    nb_iteration_label = Label(top, text="Nb Ite", font=("Helvetica", 10, "bold"))
    population_size = tk.Entry(top, width=5)
    mutation_rate = Entry(top, width=5)
    nb_iteration = Entry(top, width=5)
    y += 40
    hyper_radiobutton = tk.Radiobutton(top,
                                       text="",
                                       variable=v,
                                       value=4)
    hyper_radiobutton.place(x=10, y=y)
    hyper_label = Label(top, text="Hyper Heuristique", font=("Helvetica", 12, "bold"))
    hyper_label.place(x=30, y=y)
    hyper_label.bind('<Button-1>', hyper_heuristic_label)
    y += 40
    separator = tk.ttk.Separator(top, orient=HORIZONTAL)
    separator.place(x=0, y=y, width=320, height=1)
    y += 20
    start_button = Button(top, text="Commencer", font=("Helvetica", 12, "bold"), bg="green")
    start_button.bind('<Button-1>', start)
    start_button.place(x=100, y=y)
    y += 50
    clear_button = Button(top, text="Vider", font=("Helvetica", 12, "bold"))
    clear_button.bind('<Button-1>', clear)
    clear_button.place(x=125, y=y)
    # exit_button = Button(top, text="Quitter", font=("Helvetica", 12, "bold"))
    # exit_button.bind('<Button-1>', exiting)
    # exit_button.place(x= 50, y= y)
    y = 0
    bin_label = tk.Label(top, text="Problème de Bin Packing", font=("Helvetica", 20, "bold"), fg="green")
    bin_label.place(x=650, y=y)
    y += 10
    input_label = tk.Label(top, text="DataSet", font=("Helvetica", 12, "bold"))
    input_label.place(x=330, y=y)
    y += 30
    input_field = tk.Text(top, height=10, width=80)
    input_field.place(x=330, y=y)
    input_field.config(state=DISABLED)
    y += 170
    max_label = tk.Label(top, text="Maximum Valeur", font=("Helvetica", 12, "bold"))
    max_label.place(x=350, y=y)
    size_label = tk.Label(top, text="Taille de l'instance", font=("Helvetica", 12, "bold"))
    size_label.place(x=800, y=y)
    y += 30
    max_field = tk.Text(top, height=1, width=8, font=("Helvetica", 12, "bold"))
    max_field.place(x=370, y=y)
    max_field.config(state=DISABLED)
    size_field = tk.Text(top, height=1, width=8, font=("Helvetica", 12, "bold"))
    size_field.place(x=830, y=y)
    size_field.config(state=DISABLED)
    y += 50
    result_label = tk.Label(top, text="Résultat", font=("Helvetica", 12, "bold"))
    result_label.place(x=370, y=y)
    time_label = tk.Label(top, text="Temps d'exécution", font=("Helvetica", 12, "bold"))
    # , relief = tk.RIDGE
    time_label.place(x=800, y=y)
    y += 30
    result_field = tk.Text(top, height=1, width=8, font=("Helvetica", 12, "bold"))
    result_field.place(x=370, y=y)
    result_field.config(state=DISABLED)
    time_field = tk.Text(top, height=1, width=8, font=("Helvetica", 12, "bold"))
    time_field.place(x=830, y=y)
    time_field.config(state=DISABLED)
    non_optimal_label = tk.Label(top)
    non_optimal_label.config(font=("Helvetica", 20, "bold"))
    optimal_label = tk.Label(top)
    optimal_label.config(font=("Helvetica", 20, "bold"))
    optimal_result_label = Label(top)
    optimal_result_label.config(font=("Helvetica", 10, "bold"))
    chosen_heuritic_label = Label(top)
    chosen_heuritic_label.config(font=("Helvetica", 10, "bold"))
    y += 70
    copy_label = tk.Label(top, text="Tous Droits Réservés", font=("Helvetica", 14, "bold"), fg="green")
    copy_label.place(x=550, y=y)
    y += 25
    team_label = tk.Label(top,
                          text="Chabane            Bouchama            Lefgoum            Hammouche            Hammia",
                          font=("Helvetica", 12, "bold"))
    team_label.place(x=370, y=y)
    tk.mainloop()
