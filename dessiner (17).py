# auteurs:Ali Radwan 
# Gedeon Tsheteya Mubenga 
# date:31/10/2025

"""
Ce programme est une application de dessin simple qui permet aux utilisateurs de dessiner sur un canevas numérique.
Il fournit un menu de palette de couleurs avec des couleurs sélectionnables (blanc, noir, rouge, jaune, vert, bleu, magenta)
et un bouton gomme. Les utilisateurs peuvent cliquer et glisser pour dessiner sur le canevas avec leur couleur choisie,
et utiliser la gomme pour effacer les pixels. L'interface se compose d'une zone de dessin et d'une barre de menu latérale
contenant les boutons de couleur et de gomme.
"""

# variable globales:
largeur_ecran=240
taille_barre_menu=24 
largeur_champs_dessin=largeur_ecran-taille_barre_menu
hauteur_ecran=180
couleur_barre_menu="#888"   
couleur_courante="#000"    
tab_couleurs=["#fff","#000","#f00","#ff0","#0f0","#00f","#f0f"]
    
# la fonction cords trouve les coordonnees cartesiens de n'importe quelle
# pixel.Elle prend en parametre deux entiers (une longueur et une hauteur)
# et retourne une structure avec les coordonnees x,y du pixel
def cords(l,h):
    cord=struct(x=l,y=h) 
    return cord      

# fonction qui va assigner a chaque pixel la couleur blacnhe qui prend en  
# parametres deux entiers ,la longueur et la hauteur de la grille de pixels
def afficher_ecran(h,l):
    pixel=cords(get_screen_width(),get_screen_height())
    set_screen_mode(h,l)
    for i in range(pixel.x):                
        for j in range(pixel.y):         
            set_pixel(i,j,"#fff")
            
# fonction retourne un tableau d'enregistrements représentant les boutons 
# disponibles dans la barre de menu. Elle prend en parametre la couleur
# du boutton en format hexadecimal ,un entier qui represente la taille,
# un entier qui represente l'espace entre chaque boutton ,et une booleene 
# qui indique si  c'est le boutton effacer
def creer_boutons(couleurs,taille,espace,couleur_effacer):    
    t=[]
    coin_efface=cords(largeur_ecran-taille_barre_menu+espace,espace)
    coin_efface2=struct(x=coin_efface.x+taille,y=coin_efface.y+taille)
    # verifier si le boutton depasse les bordures de la grille sioui retourne-1
    if( coin_efface.x+taille>get_screen_width()
        or coin_efface.y+taille>get_screen_height()):
        return -1               
    # creer le bouton effacer                           
    bout1=struct(
        coin1=coin_efface,
        coin2=coin_efface2,
        couleur=couleur_effacer,
        effacer=True
    )
    t.append(bout1)    
    delta_y=coin_efface.y+espace+taille
    
    # pour chaque couleur dans le tableau couleurs on cree un boutton 
    # correspondant a la couleur pour le reste des boutons  
    for couleur in couleurs:
        coin_a=struct(x=coin_efface.x,y=delta_y)
        coin_b=struct(x=coin_a.x+taille,y=coin_a.y+taille)
        bouton=struct(
            coin1=coin_a,
            coin2=coin_b,
            couleur=couleur,
            effacer=False
        )
            
        delta_y+=espace+taille
        t.append(bouton)
              
    return t 

# fonction qui retourne True si un boutton existe dans une certaine position
# et retourne None si aucun boutton existe dans cette position, Elle prend en
# parametre le tableau retourner par la fonction creer_boutton, et les 
# coordonnes cartesiennes d'un certain point
def trouver_bouton(boutons,position): 
    if boutons!=-1:
        for i in range (len(boutons)):
            # le coin en haut a droite
            coin3=struct(x=boutons[i].coin2.x,y=boutons[i].coin1.y)
            # le coin en bas a gauche
            coin4=struct(x=boutons[i].coin1.x,y=boutons[i].coin2.y)
       
            # verifier si x et y de position fait partie dans l'air du boutton
            if(
                position.x>=boutons[i].coin1.x        
                and position.x>=coin4.x               
                and position.x<=coin3.x 
                and position.x<=boutons[i].coin2.x
            ):
           
                if(
                    position.y>=boutons[i].coin1.y   
                    and position.y<=coin4.y           
                    and position.y>=coin3.y 
                    and position.y<=boutons[i].coin2.y
                ):
               
                    return boutons[i]
            else:
                return None
    
# fonction qui retourne image_originale qui est un tableau de tableaux 
# ou les sous tableaux representent une rangee de pixels. Elle prend en 
# parametre un tableau vide qu'elle va le remplir pour arriver a image_originale

def couleur_de_rangee(t):
    pixel=cords(0,0) 
    # chaque iteration ajoute un sous tableau jusqu'on arrive a la fin 
    # du chanps dessin
    for i in range(largeur_champs_dessin):   
        temp=[]
        # chaque iteration ajoute une rangee de pixels    
        for j in range(get_screen_height()):     
            temp.append(get_pixel(pixel.x+i,pixel.y+j))
        t.append(temp)
    return t


# restaure dans l'écran simulé les pixels qui se trouvent dans la zone
# rectangle à partir du contenu correspondant de image_originale.Elle prend
# en parametre le tableau image_originale et le rectangle qu'on va restaurer
def restaurer_image(image_originale,rectangle):
    for i in range(len(rectangle)):           
        point_x=rectangle[i][0]              
        point_y=rectangle[i][1]
        ancienne_couleur=rectangle[i][2]
        set_pixel(point_x,point_y,ancienne_couleur)
    rectangle.clear()
# fonction qui calcul la position de l'ellipse d'apres le point debut et fin
# et ajoute l'ellipse si mise a jour est vraie.Elle prend en parametre l'image
# originale,la couleur de l'ellipse,un tableau temporaire qui garde les anciens
# pixels modifiés,et une booleene mise_a_jour
def ajouter_ellipse(image,couleur,ellipse,mise_a_jour):
    global s    
    debut=struct(x=get_mouse().x,y=get_mouse().y)
    fin=struct(x=s.x,y=s.y)
    # calcul ellipse
    centre_x=(debut.x+fin.x)//2
    centre_y=(debut.y+fin.y)//2
    rayon_x=abs(fin.x-debut.x)//2
    rayon_y=abs(fin.y-debut.y)//2
    
    if rayon_x>0 and rayon_y>0 :
        #parcourir tous les pixels dans l'ellipse
        for i in range(centre_x-rayon_x,centre_x+rayon_x+1):
            for j in range(centre_y-rayon_y,centre_y+rayon_y+1):
                #verifier si il est dans le champs dessin
                if i < largeur_champs_dessin:
                    # equation d'une ellipse
                    if(((i-centre_x)**2)/(rayon_x**2)+
                       ((j-centre_y)**2)/(rayon_y**2)<=1):
                        ellipse.append((i,j,get_pixel(i,j)))
                        set_pixel(i,j,couleur)
                        
                    if mise_a_jour==True :                          
                        image[i][j]=couleur
                        
# fonction qui simule l'ellipse a dessiner sur l'ecran depandant de le 
# positionnement de la souris.Elle prend en parametre le tableau image_originale
# retourne par couleur_de_rangee(),le point de debut du click de la souris,
# et la couleur de l'ellipse flottante.
def dessiner_ellipse_flottante(image_originale,debut,couleur):
    global s
    img_precedente=[] 
    while True:
        s=get_mouse()
        sleep(0.01)         
        while get_mouse().button==1:             
            debut=struct(x=get_mouse().x,y=get_mouse().y)                       
            restaurer_image(image_originale,img_precedente)            
            ajouter_ellipse(image_originale,couleur,img_precedente,False)
               
        if get_mouse().button==0 and len(img_precedente)>0:
            ajouter_ellipse(image_originale,couleur,img_precedente,True)
            restaurer_image(image_originale,img_precedente)
            break            
        restaurer_image(image_originale,img_precedente)
        
        
        
# cette fonction attend que l'utilisateurs appuie sur le bouton de la souris 
# traite l'action, et finalement retourne le nouvel état du programme.Elle 
# prend en parametre l'etat du programme une structure contenant la couleur
# courante et l'image courante,et  la liste des boutons.      
def traiter_prochain_clic(etat, boutons):
    global couleur_courante
    while True:
        s=get_mouse()
        sleep(0.01)           
        if s.button==1:
            position=struct(x=s.x,y=s.y)           
            bouton = trouver_bouton(boutons,position)  #verifier si on click
            if bouton !=None:                          #sur un bouton                
                if bouton.effacer==True:
                    fill_rectangle(0,0,get_screen_width()-taille_barre_menu,
                                   get_screen_height(),bouton.couleur)
                else:
                    couleur_courante=bouton.couleur
            elif s.x<=get_screen_width()-taille_barre_menu:
                dessiner_ellipse_flottante(couleur_de_rangee([]),0,couleur_courante)
       
    
# fonction qui va afficher l'interface utilisateur                                            
def creer_interface():
    #afficher la barre verticale en gris
    fill_rectangle(get_screen_width()-taille_barre_menu,
                   0,taille_barre_menu,get_screen_height(),
                   couleur_barre_menu)
    
    #afficher les boutons 
    boutons=creer_boutons(tab_couleurs,12,6,"#fff")   
    for i in range(8):
         carre(boutons[i].coin1.x,boutons[i].coin1.y,12,boutons[i].couleur,False)
    carre(boutons[0].coin1.x,boutons[0].coin1.y,12,boutons[0].couleur,True)
    
# fonction qui cree un carre avec un contour noir dans un certain point x,y ,
# de cote ,et de couleur choisis par l'utilisateur.Sauf s'il sagit du bouton 
# effacer ou elle ajoute aussi une crois rouge sur le bouton.Elle prend en
# parametre les coordonnees des entier x,y du point,un entier cote,sa couleur
# en format hexadecimal et unebooleene pour verifier si c'est le boutton effacer.
def carre(x,y,cote,couleur,effacer):
    # dessiner un grand carre noir de cote=cote 
    fill_rectangle(x,y,cote,cote,"#000")
    # dessiner un carre plus petit avec la couleur du bouton
    fill_rectangle(x+1,y+1,cote-2,cote-2,couleur) 
    # dessiner les barres rouges sur le bouton effacer
    if effacer==True:
        for i in range(1,cote-1):            
            set_pixel(x+i,y+i,"#f00")
            set_pixel(x+i,y+cote-i-1,"#f00")   
            
# procedure qui demarre l'editeur graphique        
def dessiner():  
    afficher_ecran(largeur_ecran,hauteur_ecran)
    creer_interface()
    traiter_prochain_clic(struct(couleur=couleur_courante,image=couleur_de_rangee([])), creer_boutons(tab_couleurs,12,6,"#fff"))
    
    
            
def test_dessiner():
    
    boutons=creer_boutons(tab_couleurs,12,6,"#fff") 
    # tests pour creer_boutons
    assert len(boutons)==len(tab_couleurs)+1
    assert boutons[0].effacer == True
    assert boutons[1].couleur == "#fff"
    assert boutons !=-1
    assert boutons[1].coin1.y== boutons[0].coin1.y +12+6
    
    # tests pour trouver_boutons
    assert trouver_bouton(boutons,cords(1000,1))==None
    assert trouver_bouton(boutons,cords(boutons[0].coin1.x,
                                        boutons[0].coin1.y))==boutons[0]
    assert trouver_bouton(-1,cords(100,1))==None
    assert trouver_bouton(boutons,cords(boutons[0].coin1.x,
                                        boutons[0].coin1.y)).effacer==True
    assert trouver_bouton([],cords(11,5))==None
    
    # tests pour restaurer_image
    
    
    print("tests reussis")
    
            
            
test_dessiner()            
dessiner()           



