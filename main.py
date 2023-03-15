import tkinter as tk
import json
import hashlib
import string
import random
from tkinter import messagebox,Frame,StringVar,ttk,END

char = list(string.ascii_letters + string.digits + "!@#$%^&*")

# fonction de generation de mot de pass
def passwordAleatoire():
    
    random.shuffle(char)
    motAleatoire = []
    
    for i in range(10):
        motAleatoire.append(random.choice(char))
    random.shuffle(motAleatoire)
    
    return ''.join(motAleatoire)


def affichePass():
    wordpass = passwordAleatoire()
    validPassword(wordpass)
    while(not number or not charSpecial or not maj or not minuscule): #recuperation d'un nouveau mot de pass tant que les exigence ne sont pas respecter
        wordpass = passwordAleatoire()
        validPassword(wordpass)
    
    return wordpass

def setpassword():
    valeur_default.set(intermediaire)

# fonction d'affichage du mot de pass
def getListElements():
    # recuperation des donnée dans le fichier json
    with open("conservepassword.json") as contenues:
        fileElements = json.load(contenues)
    
    # information de la fenetre
    fenetre1 = tk.Tk()
    fenetre1.geometry("500x400")
    fenetre1.iconbitmap("images/iconApp.ico")
    fenetre1.title("Liste des mot de pass enregistrer")
    
    # creation du treeview permetant l'arrangement du tableau
    Tablelement = ttk.Treeview(fenetre1,columns=(1,2,3),height=5,show='headings')
    Tablelement.place(x=30,y=20,width=450,height=300) 
    
    Tablelement.heading(1,text="ID")
    Tablelement.heading(2,text="Name user")
    Tablelement.heading(3,text="Password")
    
    Tablelement.column(1,width=20)
    Tablelement.column(2,width=100)
    Tablelement.column(3,width=90)
    
    for element in fileElements :
        id = element['id']
        nameUser = element['nameUser']
        password = element['password']
        tab = [id,nameUser,password]
        Tablelement.insert("",END,values=tab)
    
    fileElements.close() #fermeture du fichier

   
# fonction de verification du mot de passe
def validPassword(password):
    
    # definition de variable global
    global number
    global charSpecial
    global maj
    global minuscule
    
    number = False
    charSpecial = False
    maj = False
    minuscule = False    

    for i in password:
        c = i
        if i in '1234567890':
            number = True
        if i in "!@#$%^&*":
            charSpecial = True
        if i == c.upper() and i not in '1234567890' and not i in "!@#$%^&*":
            maj = True
        if i == c.lower() and i not in '1234567890' and not i in "!@#$%^&*":
            minuscule = True


# fonction de traitement des donée du formulaire
def getEntry():
    nameUser = nameUserinput.get()
    password = passWordinput.get()
    validPassword(password)
    if nameUser =='':
        messagebox.showerror("Error","Veuillez renseigner un nom d'utilisateur : " ,parent=fenetre)
    
    if(password != "" or password ==""):
        validPassword(password)           
        if len(password) < 8:
            messagebox.showerror("Error","Entrez un mot de pass avec plus de 8 caractere : " ,parent=fenetre)
        elif not maj:
            messagebox.showerror("Error","Le mot de passe doit au moin avoir une Lettre majuscule" ,parent=fenetre)
        elif not number:
             messagebox.showerror("Error","Le mot de pass doit comporter au moin un chiffre " ,parent=fenetre)
        elif not charSpecial:
            messagebox.showerror("Error","Le mot de pass doit au moin comporter une caractere speciale (!@#$%^&*)" ,parent=fenetre)
        elif not minuscule :
            messagebox.showerror("Error","Le mot de passe doit au moin avoir une Lettre minuscule" ,parent=fenetre)
        else:
            
            
            hashpassword = hashlib.sha256( password.encode("utf-8")).hexdigest()# hachage du mot de passe
            try:
                with open("conservepassword.json",'r') as line:
                    contenue = json.load(line)
            except Exception:
                messagebox.showerror("Error",f"le fichier Password.json n'existe pas" ,parent=fenetre)
                open("conservepassword.json",'x')

            if contenue == None:
                contenue = []
            exist = False #variable de comparaison de l'existance
            # verifion que le mot de pass n'existe pas déjà dans le fichier
            for element in contenue:
                if hashpassword == element["password"] or nameUser == element["nameUser"]:
                    exist = True

            if not exist:
                data = {
                    "id":len(contenue),
                    "nameUser":nameUser,
                    "password":hashpassword
                }
                contenue.append(data)
                fichier = open("conservepassword.json","w")
                fichier.write(json.dumps(contenue,indent=True))
                fichier.close()
                messagebox.showinfo("Success","Le mot de pass est correcte et à bien été enregistrez",parent=fenetre)
            else:
                messagebox.showerror("Error","Mot de passe et/ou Nom d'utilisateur non disponible" ,parent=fenetre)
            
            
            
# debut du programme


fenetre = tk.Tk()
fenetre.geometry("400x370")
    
fenetre.iconbitmap("images/iconApp.ico")
fenetre.title("Enregistrement d'un mot de pass")

# formulaire
form = Frame(fenetre, bg="gray")
form.place(x=57, y= 65, width =300, height = 200)

# champs name user
labelNameUser = tk.Label(form,text ="Entrez votre nom d'utilisateur",fg='black', bg="gray",font=("times new roman",12)).place(x=30, y=10)
nameUserinput = tk.Entry(form, width=30,font=('times new roman',12))
nameUserinput.place(x=30,y=40)

# champs mot de pass
valeur_default = StringVar()
labelPassword = tk.Label(form,text ="Entrez un mot de pass",fg='black',bg="gray",font=("times new roman",12)).place(x=30, y=65)
passWordinput = tk.Entry(form, width=30,font=('times new roman',12),textvariable=valeur_default)
passWordinput.place(x=30,y=95)

intermediaire = affichePass() #suggestion du mot de passe

# affichage du mot de passe suggerer
labelPassword = tk.Label(form,text ="Poposition d'un mot de pass : ",fg='black',bg="gray",font=("times new roman",8)).place(x=30, y=125)
btn = tk.Button(form, height=1, width=10, text=intermediaire, command=setpassword).place(x=200,y=125)

# button de souission du formulaire
btn = tk.Button(form, height=1, width=10, text="Enregistrez", command=getEntry).place(x=100,y=160)

# boutton d'affichage de la liste d'element
btn = tk.Button(fenetre, height=1, width=10, text="liste des mot de pass", command=getListElements,bg="#0088ff",fg='white').place(x=140,y=20,width=140)
fenetre.mainloop()