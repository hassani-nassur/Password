import hashlib
import random,string
import json

# list des caracter necessaire pour faire un mot de pass
char = list(string.ascii_letters + string.digits + "!@#$%^&*")

# fonction de generation de mot de pass
def passwordAleatoire():
    
    random.shuffle(char)
    motAleatoire = []
    
    for i in range(10):
        motAleatoire.append(random.choice(char))
    random.shuffle(motAleatoire)
    
    return ''.join(motAleatoire)

# fonction verifiant la validation du mot de pass
def validPassword(password):
    
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


wordpass = passwordAleatoire() #recuperation du mot de passe aleatoire
validPassword(wordpass) #verification de cretaire d'exigence

while(not number or not charSpecial or not maj or not minuscule): #recuperation d'un nouveau mot de pass tant que les exigence ne sont pas respecter
    wordpass = passwordAleatoire()
    validPassword(wordpass)

print("\nNous vous proposons ce mot de pass : ",wordpass)

reponse = input("\nvoulez vous utilisez ce mot de pass? Tapez O:Oui ou N:non : ") #choix de l'utilisateur vis à vis du mot de passe proposer

while(reponse.lower() !="o" and reponse.lower() != 'n'):
    reponse = input("veullez Tapez O:Oui ou N:non : ")

if(reponse.lower() == 'o'):
    password = wordpass
else:
    password = str(input("Veillez entre votre mot de pass : "))

# verification de criter du mot de pass
while(password != "" or password ==""):
    validPassword(password)           
    if len(password) < 8:
        password = str(input("Entrez un mot de pass avec plus de 8 caractere : " ))
    elif not maj:
        print("Le mot de passe doit au moin avoir une Lettre majuscule")
        password = str(input("Entrez à nouveau un mot de pass : " ))
    elif not number:
        print("Le mot de pass doit comporter au moin un chiffre")
        password = str(input("Entrez à nouveau un mot de pass : : " )) 
    elif not charSpecial:
        print("Le mot de pass doit au moin comporter une caractere speciale (!@#$%^&*)")
        password = str(input("Entrez à nouveau un mot de pass : " ))
    elif not minuscule :
        print("Le mot de passe doit au moin avoir une Lettre minuscule")
        password = str(input("Entrez à nouveau un mot de pass : " ))
    else:
        break

hashpassword = hashlib.sha256( password.encode("utf-8")).hexdigest()# hachage du mot de passe

# lecture du fichier json
with open("conservepassword.json",'r') as line:
    contenue = json.load(line)
id = len(contenue)

exist = False #variable de comparaison de l'existance
# verifion que le mot de pass n'existe pas déjà dans le fichier
for element in contenue:
    if hashpassword == element["password"]:
        exist = True

if not exist:
    data = {
        "id":id,
        "password":hashpassword
    }
    contenue.append(data)
    fichier = open("conservepassword.json","w")
    fichier.write(json.dumps(contenue,indent=True))
    print("Le mot de pass est correcte et à bien été enregistrez")
else:
    print("Mot de pass non disponible")
    

        