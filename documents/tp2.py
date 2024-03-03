# Auteur : Dawson Zhang et Cedric Guevremont
# Date : 12 Décembre 2023

# Ce programme web vise à reproduire le jeu "Addiction Solitaire", où le joueur doit disposer 
# initialement les cartes sur une grille, retirer les as, puis déplacer les cartes pour remplir 
# les trous en alignant les cartes du 2 au roi de chaque couleur en séquence. Le joueur gagne en 
# réussissant à placer toutes les cartes correctement sur les rangées et perd s'il ne peut plus 
# déplacer de cartes après trois mélanges

chances = 3

def init():
  # changer le contenu HTML de l'élément racine
  racine = document.querySelector("#cb-body")
  # Debut du code HTML
  html = """
    <style>
      #jeu table { float:none; }
      #jeu table td { border:0; padding:1px 2px; height:auto; width:auto; }
      #jeu table td img { height:140px; }
    </style>
    <div id="jeu">
      <div>
        <table id="table">"""
  
  # Écrire toutes les cartes avec Python 
  ordre = ['A','2','3','4','5','6','7','8','9','1','J','Q','K']   # les 13 numéraux de cartes
  signe = ['C','D','H','S']                                       # les 4 signes
  for rangee in range (1,5):
    html += '<tr>'
    for colonne in range(1,14):
        html += '<td id="case'+ str(colonne) +"-"+ str(rangee) +'"><img src="cards/'+ordre[colonne-1]+signe[rangee-1]+'.svg"></td>'
    html += '</tr>'

  # Fin du code HTML        
  html +="""
        </table>
      </div>
      <div id="menu">
        <p id="texte">Vous pouvez encore <button onclick="boutonBrasser()">Brasser les cartes</button><span id="chance">3</span> fois</p>
        <button onclick="premierBrasser()">Nouvelle partie</button>
      </div>
    </div>"""
  racine.innerHTML = html
  premierBrasser()



# Cette fonction permet de mélanger TOUTES les cartes, c'est à dire seulement le premier brasser d'une partie
def premierBrasser():
  testGagner()
  testContenir()
  global chances
  # Ensemble des cartes d'un jeu de 52 cartes
  carte = ['AC', '2C', '3C', '4C', '5C', '6C', '7C', '8C', '9C', '10C','JC', 'QC', 'KC',
          'AD', '2D', '3D', '4D', '5D', '6D', '7D', '8D', '9D', '10D', 'JD', 'QD', 'KD',
          'AH', '2H', '3H', '4H', '5H', '6H', '7H', '8H', '9H', '10H', 'JH', 'QH', 'KH',
          'AS', '2S', '3S', '4S', '5S', '6S', '7S', '8S', '9S', '10S', 'JS', 'QS', 'KS']
  effacer()
  cartePosition = []                                              # liste de toutes les cartes mélangées
  chances = 3                                                     # nouvelle partie on revient à 3 chances
  for _ in range (52):                                            # mélanger les cartes aléatoirement    
    indice = len(carte)                                           # liste réduite donc indice aussi
    carteAleatoire = int(random()*indice)                         # choisir une carte aléatoire
    cartePosition.append(carte[carteAleatoire])                   # ajouter à la liste mélangée
    carte.pop(carteAleatoire)                                     # retirer de la liste de base
  ecrire(cartePosition,[])

# Cette fonction va dessiner toutes les cartes selon l'argument cartePosition (liste de la position des cartes) qu'elle reçoit
def ecrire(cartePosition,coloriage):
  effacer()                                                       # effacer les couleurs des cartes avant d'écrire nouvelle liste (sauf première fois inutile)                              
  nonCouleur = 0                                                  # plus tard, variable utilisée pour détecter qu'il n'y a plus de pas à jouer
  liste = ",".join(cartePosition)                                 # puisqu'on a pas trouver comment mettre une liste en argument d'une fonction HTML (joindre et défaire lors d'utilisation)
  if int(chances)>0:                                              # si le joueur a au moins une chance encore
    bouton = document.querySelector("#texte")                     # ajouter à la fonction boutonBrasser l'argument liste pour qu'il puisse brasser dès le debut
    bouton.innerHTML = 'Vous pouvez encore <button onclick="boutonBrasser(\''+liste+'\')">Brasser les cartes</button> <span id="chance">'+str(chances)+'</span> fois'  
  for k in range(1,5):
    for p in range(1,14):
      carteChercher = ''                                          # la carte qui devrait se retrouver dans le trou
      carteCetteBoucle = cartePosition[((k-1)*13)+(p-1)]          # la carte de cette boucle
      carteDocument = document.querySelector("#case"+str(p)+"-"+str(k)) 

      if carteCetteBoucle[0] == "A":                              # si la première lettre egal à 'A', c'est donc un trou
        carteDocument.innerHTML = ''                              # créer le trou dans HTML
        gauche = cartePosition[((k-1)*13)+(p-1)-1]                # retenir valeur de la carte à sa gauche
        symb = ['A','','2','3','4','5','6','7','8','9','1','J','Q','K','']
        indice = 0
        if p != 1:                                                # si p = 1, alors trou première rangée, donc on passe
          for symbole in symb:                         
            if gauche[0] == '9':                                  # Si on a un 9 à gauche, cas special, puisque 10 (deux caractères)
              carteChercher = '10'+gauche[-1]           
            elif gauche[0] == symbole:                            # sinon on applique la prochaine valeur concaténée au même signe
              carteChercher = symb[indice+1] + gauche[-1]
            indice += 1
        else:  
          carteChercher = True                                    # si p = 1, CarteChercher devient True pour colorier tous les '2'
        deux = ["2C","2D","2H","2S"]                   
        for i in range(52):
          if carteChercher == True:                  
              for carteDeux in deux:                        
                if carteDeux == cartePosition[i]:                 # trouver position des '2' pour colorier
                  couleur(carteDeux,cartePosition,i,coloriage,gauche) 
          elif carteChercher == cartePosition[i]:                 # trouver position carteChercher pour colorier
            couleur(carteChercher,cartePosition,i,coloriage,gauche)
          else:                                                   # sinon pas de carteChercher (trou devant 'K' ou 'A')
            nonCouleur += 1                                       # ajouter à nonCouleur pour garder une trace du nombre de cartes pas coloriées

      else:                                                       # si la carte n'est pas un trou 
        if contenir(cartePosition[((k-1)*13)+(p-1)],coloriage):                                    # vérifier qu'il n'est pas deja colorier
          carteDocument.innerHTML = "<img src="+"cards/"+cartePosition[((k-1)*13)+(p-1)]+".svg>"   # déssiner la carte sans couleur

      if nonCouleur == 208:                                       # si nonCouleur arrive à 208 alors aucune carte est coloriée
        if chances != 0:                                          # si joueur a encore des vies l'obliger de brasser
          plusDePas = document.querySelector("#texte")
          plusDePas.innerHTML = 'Vous devez <button onclick="boutonBrasser(\''+liste+'\')">Brasser les cartes</button>'
        else:
          plusDePas = document.querySelector("#texte")            # sinon perdu :C
          plusDePas.innerHTML = "Vous n'avez pas réussi à placer toutes les cartes... Essayez à nouveau!" 
  if gagner(cartePosition):                                       # Savoir joueur a gagné :D
    plusDePas.innerHTML = "Vouz avez réussi! Bravo!"
  else:
    pass
  


# Cette fonction s'occupe de colorier les cartes en vert
def couleur(cardToV,liste,i,couleurAjouter,gauche):          
    couleurAjouter.append(cardToV)                                # ajouter à une liste pour éviter des doublons lors du dessin des cartes
    rangee = (i%13)+1                                    
    colonne = (i//13)+1
    liste1 = ",".join(liste)
    surligner = document.querySelector("#case"+str(rangee)+"-"+str(colonne))                       # colorier cette carte ainsi qu'ajouter fonctionalité pour cliquer dessus
    surligner.innerHTML = '<img onclick="bougerCarte(\''+cardToV+'\',\''+gauche+'\',\''+liste1 +'\')" src="cards/'+ liste[i] + '.svg">' 
    surligner.setAttribute("style", "background-color: lime")                           



# Cette fonction se déclenche lorsqu'un utilisateur clique sur une image, et elle est responsable
# de déplacer la carte vers la bonne position tout en réorganisant l'ordre des cartes.
def bougerCarte(carteChercher,gauche,liste1):
  reinitialiser = []                                              # remettre liste des cartes coloriées à zero, car on créer une nouvelle liste dans cette fonction
  listeToutesCarte = liste1.split(',')                            # l'argument liste1 vien d'une fonction où l'on n'avait joint en un seul string pour le rentrer dans HTML
  listeCopie = listeToutesCarte.copy()                            # on crée une nouvelle copie pour stocker la nouvelle liste 
  for i in range (52):
    if carteChercher == listeToutesCarte[i]:                      # trouver la carte qui est supposé être dans le trou (carteChercher)
      for j in range(52):  
        rangee = (j%13)+1
        colonne = (j//13)+1     
        if gauche == listeToutesCarte[j]:                         # trouver la gauche du trou (+1 pour dessiner dans le trou)
          premiereCol = [listeCopie[0],listeCopie[13],listeCopie[26],listeCopie[39]]
          if carteChercher[0] == "2":                             # si la carte qu'on deplace est un '2'
            for evaluer in range (4):                  
              if premiereCol[evaluer][0] == "A":                  # chercher quelle case dans la première colonne est vide
                bouger = document.querySelector("#case1-"+str(evaluer+1))                          # déplacer dans le premier trou disponible de la première colonne
                bouger.innerHTML = '<img onclick="bougerCarte(\''+gauche+'\',\''+liste1 +'\')" src="cards/'+ carteChercher + '.svg">'
          bouger = document.querySelector("#case"+str(rangee+1)+"-"+str(colonne))                  # sinon dessiner dans le trou assigné
          bouger.innerHTML = '<img onclick="bougerCarte(\''+gauche+'\',\''+liste1 +'\')" src="cards/'+ carteChercher + '.svg">'
          if rangee == 13 and colonne == 4:                       # lors débordement de un indice
            rangee = 0                                   
            colonne = 1
          trouAncien = (colonne-1)*13+(rangee)                    # l'emplacement du vieux trou
          trouPresent = listeToutesCarte[(colonne-1)*13+(rangee)] # l'emplacement du nouveau trou
          listeCopie.remove(carteChercher)                        # retirer et insérer la carte bouger
          listeCopie.insert(trouAncien,carteChercher)
          listeCopie.remove(trouPresent)                          # déplacer le trou de position
          listeCopie.insert(i,trouPresent)
  ecrire(listeCopie,reinitialiser)                                # déssiner la nouvelle liste avec la carte déplacée



# Cette fonction se charge de mélanger les cartes tout en maintenant l'ordre actuel des cartes bien positionnées.
def nouveauBrasser(liste):                                    
  compteur = 0                                                    # compteur pour l'indice de la carte et du signe à utiliser                           
  listeUtiliser = liste.split(',')                                # défaire le string qui vient d'une fonction dans une ligne de HTML 
  nouvelleListe = listeUtiliser.copy()                            # créer une copie pour stocker la nouvelle liste
  ordre = ['2','3','4','5','6','7','8','9','1','J','Q','K','A']
  nePasBouger = [[],[],[],[]]                                     # la liste des cartes à ne pas bouger
  for i in range(4):
    compteur = (i)*13                                             # indice de la première carte de chaque rangée
    signe = listeUtiliser[compteur][1]                            # touver le signe de la première carte
    for j in range(13):
      carte = listeUtiliser[compteur]                             # la carte utilisée pour cette itération de la boucle
      if carte[0] == ordre[j] and carte[-1] == signe:             # si elle correspond à l'ordre selon son indice [2,3,4,...] + le bon signe pour cette rangée
        nePasBouger[i].append(carte)                              # l'ajouter à la liste à ne pas bouger
        nouvelleListe.remove(carte)                               # retirer de la liste à brasser
      else:
        break
      compteur += 1    
  cartePosition = []                                              # repris cette partie
  for _ in range (len(nouvelleListe)):                            # brasser les cartes restantes qui ne sont pas en ordre
    indice = len(nouvelleListe)                                 
    carteAleatoire = int(random()*indice)
    cartePosition.append( nouvelleListe[carteAleatoire])
    nouvelleListe.pop(carteAleatoire)
  compteur = 0
  for k in range(4):
    compteur = (k*13)
    for p in range(13):
      if nePasBouger[k] == []:
        break
      elif nePasBouger[k][0][0] == ordre[p]:
        cartePosition.insert(compteur,(nePasBouger[k][0]))
        nePasBouger[k].remove(nePasBouger[k][0])
      else:
        break
      compteur += 1
  ecrire(cartePosition,[])



# Cette fonction s'active dès que l'utilisateur clique sur le bouton 'Brasser les cartes'
# Elle a pour effet de décrémenter le nombre de chances restantes tout en appelant la fonction de nouveauBrasser
def boutonBrasser(liste):
    global chances
    chances -= 1
    liste1 = ",".join(liste)
    nouveau = document.querySelector("#texte")
    nouveau.innerHTML = '<p id="texte">Vous pouvez encore <button onclick="boutonBrasser(\''+liste1+'\')">Brasser les cartes</button> <span id="chance">3</span> fois</p>'
    chance = document.querySelector("#chance")
    if chances == 0:
      fin = document.querySelector("#texte")
      fin.innerHTML = "Vous ne pouvez plus brasser les cartes"
    chance.innerHTML = chances
    nouveauBrasser(liste)



# Cette fonction prend en entrée une liste et une variable, puis vérifie si la variable est présente dans la liste
def contenir(x, liste):
  for i in liste:
    if str(x) == str(i):
      return False
  return True


# Cette fonction efface toutes les couleurs                      
def effacer():
  for k in range(1,5):
      for p in range(1,14):
        carte = document.querySelector("#case"+str(p)+"-"+str(k))
        carte.setAttribute("style","background-color: none")

# Cette fonction vérifie si le joueur a gagné
def gagner(liste):
  ordre = ['2','3','4','5','6','7','8','9','10','J','Q','K']
  for i in range(4):
    signe = liste[i*13][-1]
    for j in range(12):
      if liste[(i*13)+j] != ordre[j] +signe:
        return False    
  return True

    
    
# Test Unitaires ============================================================================================================   
def testGagner():
  assert(gagner(['2C', '3C', '4C', '5C', '6C', '7C', '8C', '9C', '10C','JC', 'QC', 'KC','AC',
             '2D', '3D', '4D', '5D', '6D', '7D', '8D', '9D', '10D', 'JD', 'QD', 'KD','AD',
             '2H', '3H', '4H', '5H', '6H', '7H', '8H', '9H', '10H', 'JH', 'QH', 'KH','AH',
             '2S', '3S', '4S', '5S', '6S', '7S', '8S', '9S', '10S', 'JS', 'QS', 'KS','AS'])) == True
  
  assert(gagner(['2C', '3C', '4C', '5C', '6C', '7C', '8C', '9C', '10C','JC', 'QC', 'KC','AD',
             '2D', '3D', '4D', '5D', '6D', '7D', '8D', '9D', '10D', 'JD', 'QD', 'KD','AC',
             '2H', '3H', '4H', '5H', '6H', '7H', '8H', '9H', '10H', 'JH', 'QH', 'KH','AH',
             '2S', '3S', '4S', '5S', '6S', '7S', '8S', '9S', '10S', 'JS', 'QS', 'KS','AS'])) == True
  
  assert(gagner(['2D', '3D', '4D', '5D', '6D', '7D', '8D', '9D', '10D', 'JD', 'QD', 'KD','AC',
             '2C', '3C', '4C', '5C', '6C', '7C', '8C', '9C', '10C','JC', 'QC', 'KC','AD',
             '2H', '3H', '4H', '5H', '6H', '7H', '8H', '9H', '10H', 'JH', 'QH', 'KH','AS',
             '2S', '3S', '4S', '5S', '6S', '7S', '8S', '9S', '10S', 'JS', 'QS', 'KS','AH'])) == True
  
  assert(gagner(['AD', '3D', '8D', '5D', '7D', '10C', '8D', '10D', '8D', 'JD', '2D', 'QD','AC',
             '6C', 'AC', '8S', '3C', '6C', '9S', '5C', '9C', '10C','JC', 'QC', 'kC','2D',
             '4H', '3H', '4H', '5H', '6H', '3H', '8H', '9H', '10H', 'KH', 'QH', 'KH','AH',
             '2S', '3S', '4D', '5S', '2C', '2S', '9S', '2D', '10S', 'JS', 'QS', 'KS','AS'])) == False
  
  assert(gagner(['AC', '2C', '3C', '4C', '5C', '6C', '7C', '8C', '9C', '10C','JC', 'QC', 'KC',
            'AD', '2D', '3D', '4D', '5D', '6D', '7D', '8D', '9D', '10D', 'JD', 'QD', 'KD',
            'AH', '2H', '3H', '4H', '5H', '6H', '7H', '8H', '9H', '10H', 'JH', 'QH', 'KH',
            'AS', '2S', '3S', '4S', '5S', '6S', '7S', '8S', '9S', '10S', 'JS', 'QS', 'KS'])) == False
  
def testContenir():
  assert(contenir('4C',['2C', '3C', '4C', '5C', '6C', '7C'])) == False

  assert(contenir('AC',['2C', '3C', '4C', '5C', '6C', '7C'])) == True

  assert(contenir('3D',['2C', '3C', '4C', '5C', '6C', '7C'])) == True

  assert(contenir('4C',[])) == True

  assert(contenir('4C',[''])) == True