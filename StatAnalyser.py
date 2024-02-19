

diagrammes = True
try:
    import matplotlib.pyplot as plt
except ImportError:
    print("L'opption des diagrammes indisponible")
    diagrammes = False

try:
    import numpy as np
except ImportError:
    print("L'opption des diagrammes indisponible")
    diagrammes = False

try:
    import kandinsky as kd
except ImportError:
    print("L'opption des diagrammes indisponible")
    diagrammes = False

class Tab:
    def __init__(self, total, size, coef, MoyenneClasses, masse_salariale) -> None:
        self.classes = {}
        self.total = total
        self.size = size
        self.coef = coef
        self.moyenneClasses = MoyenneClasses
        self.masse_salariale = masse_salariale

    def remplirClasses(self) -> None:
        print("Remplissage des extrémités")
        for i in range(self.size):
            exmin_input = input("min["+str(i)+"]? ")
            exmax_input = input("max["+str(i)+"]? ")
            
            ni_input = input("n["+str(i)+"]: ")
            ni = float(ni_input) if ni_input.isdigit() else None

            masse_salariale_classe = self.masse_salariale[i]

            if exmin_input.lower() == "min":
                exmax = float(exmax_input) if exmax_input.replace('.', '', 1).isdigit() else None
                exmin = (masse_salariale_classe * 2 / ni) - exmax
            elif exmax_input.lower() == "max":
                exmin = float(exmin_input) if exmin_input.replace('.', '', 1).isdigit() else None
                exmax = (masse_salariale_classe * 2 / ni) - exmin
            else:
                exmin = None if exmin_input == "?" else float(exmin_input)
                exmax = None if exmax_input == "?" else float(exmax_input)
                exmin = float(exmin_input) if exmin_input.replace('.', '', 1).isdigit() else None
                exmax = float(exmax_input) if exmax_input.replace('.', '', 1).isdigit() else None
            


            self.classes[(exmin, exmax)] = [ni]


    def ci(self) -> None:
        for plage, data in self.classes.items():
            exmin, exmax = plage
            ni = data[0]
            ci = (exmax + exmin) / 2
            data.append(ci)  

    def fi(self) -> None:
        for data in self.classes.values():
            ni = data[0]
            fi = ni / self.total
            data.append(fi)  

    def ai(self) -> None:
        for plage, data in self.classes.items():
            exmin, exmax = plage
            ai = exmax - exmin
            data.append(ai)  

    def Fi(self) -> None:
        somme = 0
        for data in self.classes.values():
            fi = data[2]  
            somme += fi
            data.append(somme)  

    def hi(self) -> None:
        for data in self.classes.values():
            fi = data[2]  
            ai = data[3]  
            hi = (fi / ai) * self.coef
            data.append(hi)  

    def calculer(self):
        
        self.estimerPlagesManquantes()
        
        
        self.ci()
        self.fi()
        self.ai()
        self.Fi()
        self.hi()


    def verifsomme(self)->bool:
        
        somme = 0
        for plage in self.classes.keys():
            somme += self.classes[plage] 

        return somme == self.total

    def verifplage(self)->bool:
        
        for plage in self.classes.keys():
            x,y = plage
            if x > y:
                return False
        return True

    def verif(self) -> bool:
        return self.verifsomme() and self.verifplage()

    def verifierPlagesConsécutives(self):
        plages_triees = sorted(self.classes.keys(), key=lambda plage: plage[0])
        
        for i in range(1, len(plages_triees)):
            max_precedent = plages_triees[i-1][1]
            min_suivant = plages_triees[i][0]

            if min_suivant < max_precedent:
                return False

        return True

    def checkplage(self) -> bool:
        for plage in self.classes.keys():
            x,y = plage
            if x == None or y == None:
                return False
            
                
        return self.verifierPlagesConsécutives()
    
    def calculerMoyennePonderee(self) -> float:
        somme_ci_ni = 0
        ni_total = 0
        for plage, data in self.classes.items():
            ni = data[0]  
            if plage[0] is not None and plage[1] is not None:  
                ci = (plage[0] + plage[1]) / 2  
                somme_ci_ni += ci * ni
                ni_total += ni
        if ni_total > 0:
            return somme_ci_ni / ni_total
        else:
            return None

        
    def estimerPlagesManquantes(self):
        moyenne_globale = self.calculerMoyennePonderee()
        
        for plage, data in list(self.classes.items()):
            exmin, exmax = plage
            ni = data[0]
            
            if exmin is None and exmax is not None:
                
                exmin_estime = 2 * moyenne_globale - exmax
                self.classes[(exmin_estime, exmax)] = self.classes.pop((exmin, exmax))
            
            if exmax is None and exmin is not None:
                
                exmax_estime = 2 * moyenne_globale - exmin
                self.classes[(exmin, exmax_estime)] = self.classes.pop((exmin, exmax))

    def variance(self) -> float:
        try:
            somme = 0
            moy = self.calculerMoyennePonderee()  
            for plage, data in self.classes.items():
                ni = data[0]  
                ci = data[1]  
                somme += ni * (ci - moy) ** 2
            return somme / self.total
        except Exception as e:
            print("Erreur dans les données : "+str(e))
            self.AfficherFormules()
            return None

    def Findni(self) -> None :
        try:
            somme = 0

            for plage in self.classes.keys():
                somme += self.classes[plage]

            for plage in self.classes.keys():
                ni = self.classes[plage]
                if ni == None:
                    self.classes[plage] = self.total - somme
                    break
        except Exception as e:
            print("Erreur dans les données : "+str(e))
    
    def Findplage(self) -> None:
        try:
            for plage in self.classes.keys():
                x,y = plage
                if x == None:
                    self.classes[plage] = (self.total - y, y)
                    break
                elif y == None:
                    self.classes[plage] = (x, self.total - x)
                    break
        except Exception as e:
            print("Erreur dans les données : "+str(e))

    def moyenne(self) -> float:
        try:
            somme = 0
            for plage, data in self.classes.items():
                ni = data[0]  
                ci = data[1]  
                somme += ni * ci
            return somme / self.total
        except Exception as e:
            print("Erreur dans les données : "+str(e))
            return None

    def diagramme_differentiel(self):
        try:
            valeurs = [data[0] for _, data in self.classes.items()]  
            plt.hist(valeurs, bins=len(self.classes))
            plt.show()
        except Exception as e:
            print("Erreur dans les données : "+str(e))

    def diagramme_integral(self):
        try:
            valeurs = [float(data[0]) for _, data in self.classes.items()]
            valeurs_cumulees = []
            somme_cumulee = 0
            for valeur in valeurs:
                somme_cumulee += valeur
                valeurs_cumulees.append(somme_cumulee)

            indices = [i for i in range(len(valeurs_cumulees))]

            plt.plot(valeurs_cumulees)
            plt.show()
        except Exception as e:
            print("Erreur dans les données : "+str(e))

    def diagramme_en_barres(self):
        print("Diagramme en barres...")
        # Supposons que `categories` et `valeurs` sont définies comme dans ton code
        categories = [i for i, _ in enumerate(self.classes.keys())]
        valeurs = [ni for _, (ni, _, _, _, _, _) in self.classes.items()]
        
        # Définition des couleurs
        couleur_barre = kd.color(255, 0, 0)  # Rouge
        
        # Dimensions de l'écran NumWorks
        ecran_largeur, ecran_hauteur = 320, 240  # Ajuster selon les spécifications exactes
        
        # Dessiner chaque barre
        for i, val in enumerate(valeurs):
            print("Dessin de la barre", i)
            # Calculer la position et la hauteur de la barre
            x = 10 + i * 20  # Exemple de positionnement, à ajuster
            y = ecran_hauteur - val  # Ajuster la hauteur
            kd.fill_rect(int(x), int(y), 10, int(val), couleur_barre)



    def calculer_coefficients(self):
        moy = self.calculerMoyennePonderee()
        s = self.variance() ** 0.5  # Écart-type
        n = self.total
        m3 = sum([(data[1] - moy) ** 3 * data[0] for _, data in self.classes.items()]) / n
        m4 = sum([(data[1] - moy) ** 4 * data[0] for _, data in self.classes.items()]) / n
        skewness = m3 / (s ** 3)  # Coefficient d'asymétrie
        kurtosis = m4 / (s ** 4) - 3  # Coefficient d'aplatissement (Fisher)
        return skewness, kurtosis
    
    def quartiles_interpolation(self):

        total = sum([data[0] for data in self.classes.values()])  # Recalculer au cas où
        q_positions = [total * 0.25, total * 0.5, total * 0.75]
        quartiles = []

        sorted_classes = sorted(self.classes.items(), key=lambda x: x[0][0])
        cumul = 0  # Fréquence cumulée
        for pos in q_positions:
            for (exmin, exmax), (ni, _, _, ai, Fi, _) in sorted_classes:
                cumul += ni
                if cumul >= pos:
                    prev_cumul = cumul - ni
                    delta = (pos - prev_cumul) / ni
                    quartile = exmin + delta * ai
                    quartiles.append(quartile)
                    break

        if len(quartiles) == 3:
            return quartiles
        else:
            return [None, None, None]  # Retourne une liste de None si les quartiles ne peuvent pas être calculés

    
    def dessiner_box_plot(self):
        quartiles = self.quartiles_interpolation()
        if not all(quartiles):
            print("Erreur lors du calcul des quartiles")
            return

        q1, mediane, q3 = quartiles
        sorted_classes = sorted(self.classes.keys(), key=lambda plage: plage[0])
        min_val, _ = sorted_classes[0]
        _, max_val = sorted_classes[-1]

        x_start, y_start = 50, 100
        box_width = 20
        scale = 2

        # Adaptez cette section en fonction de votre interface graphique
        # Dessiner la boîte
        kd.fill_rect(int(x_start + q1*scale), y_start, int((q3-q1)*scale), box_width, kd.color(200, 200, 200))
        # Dessiner la médiane
        kd.fill_rect(int(x_start + mediane*scale) - 1, y_start, 3, box_width, kd.color(255, 0, 0))
        # Dessiner les whiskers (optionnel)
        # Ajouter du texte pour les labels (optionnel)
    
    def AfficherFormules(self)->None:
        
        print("ci = (exmax + exmin)/2")
        print("ci = min + max /2, c'est la moyenne des extrémités")
        print("fi = ni/total fi")
        print("fi = ni/n, c'est la fréquence de la classe")
        print("ai = exmax - exmin")
        print("ai = max - min, c'est la largeur de la classe")
        print("Fi = somme(fi), simga fi, du genre f1 f2 f3 ... fn")
        print("Fi = somme(fi), simga fi, c'est la fréquence cumulée de la classe")
        print("hi = (fi/ai)*" + str(self.coef) + "hi")
        print("hi = (fi/ai)*"+str(self.coef)+"HI, c'est la densité de la classe")
        print("Moyenne = somme(ci*ni)/total")
        print("Moyenne = somme(ci*ni)/total, c'est la moyenne pondérée")
        print("Variance = somme(ni*(ci-moyenne)^2)/total")
        print("Variance = somme(ni*(ci-moyenne)^2)/total, c'est la variance pondérée")
        print("Quartiles = interpolation des quartiles, exmin + (((pos - prev_Fi) / fi) * ai)")
        print("Calcul des coefficients d'asymétrie et d'aplatissement formule: skewness = m3 / (s ** 3) et kurtosis = m4 / (s ** 4) - 3")

    def toString(self)-> None:
        try:
            for plage, (ni, ci, fi, ai, Fi, hi) in self.classes.items():
                print("Plage: "+str(plage)+"ni: "+str(ni)+"ci: "+str(ci)+"fi: "+str(fi)+"ai: "+str(ai)+"Fi: "+str(Fi)+"hi: "+str(hi))
        except Exception as e:
            print("Erreur dans les données : "+str(e))
        try:
            print("Moyenne: "+str(self.moyenne()))
        except Exception as e:
            print("Erreur dans la moyenne : "+str(e))

        try:
            q1, median, q3 = self.quartiles_interpolation()
            print("Quartiles: Q1: "+str(q1)+" Median: "+str(median)+" Q3: "+str(q3))
        except Exception as e:
            print("Erreur dans les quartiles : "+str(e))

        try:
            print("Variance: "+str(self.variance()))
        except Exception as e:
            print("Erreur dans la variance : "+str(e))
        
        try:
            skewness, kurtosis = self.calculer_coefficients()
            print("Coefficients: Skewness: "+str(skewness)+" Kurtosis: "+str(kurtosis))
        except Exception as e:
            print("Erreur dans les coefficients : "+str(e))


def main():
    print("Configuration de la table des classes")

    while True:
        try:
            total = float(input("total : "))
            break
        except ValueError:
            print("Veuillez entrer un nombre entier pour le total.")
    while True:
        try:
            size = int(input("nombre de classes : "))
            break
        except ValueError:
            print("Veuillez entrer un nombre entier pour le nombre de classes.")
    while True:
        try:
            coef = float(input("coefficient (coef) : "))
            break
        except ValueError:
            print("Veuillez entrer un nombre pour le coefficient.")
    
    
    masse_salariale = []
    for i in range(size):
        while True:
            try:
                masse = float(input("masse du sujet pour la classe "+str(i+1)+" : "))
                masse_salariale.append(masse)
                break
            except ValueError:
                print("Veuillez entrer un nombre pour la masse salariale.")
    

    tab = Tab(total, size, coef, None, masse_salariale)
    while True:
        i = 1 
        print("\nMenu:")
        print("{}. Remplir classes".format(i)); i += 1
        print("{}. Calculer statistiques".format(i)); i += 1
        print("{}. Verifier Données".format(i)); i += 1
        print("{}. Afficher formules".format(i)); i += 1
        print("{}. Afficher données".format(i)); i += 1
        if diagrammes:
            print("{}. Diagrammes".format(i)); i += 1
        print("{}. Quitter".format(i))
        
        choix = input("Entrez votre choix: ")
        
        if choix == '1':
            tab.remplirClasses()
        elif choix == '2':
            tab.calculer()
            print("Calculs effectués.")
        elif choix == '3':
            if tab.verif() and tab.verifierPlagesConsécutives():
                print("Toutes les vérifications sont passées.")
            else:
                print("Erreur dans les données.")
        elif choix == '4':
            tab.AfficherFormules()
        elif choix == '5':
            tab.toString()
        elif choix == '6' and diagrammes:
            print("Diagrammes:")
            print("1. Diagramme différentiel")
            print("2. Diagramme intégral")
            print("3. Diagramme en barres")
            print("4. Diagramme circulaire")
            print("5. Box plot")
            print("6. Retour au menu principal")
            diagramme_choix = input("Entrez votre choix: ")
            if diagramme_choix == '1':
                tab.diagramme_differentiel()
            elif diagramme_choix == '2':
                tab.diagramme_integral()
            elif diagramme_choix == '3':
                tab.diagramme_en_barres()
            elif diagramme_choix == '4':
                #tab.diagramme_circulaire()
                print("Non implémenté.")
            elif diagramme_choix == '5':
                tab.dessiner_box_plot()
            elif diagramme_choix == '6':
                continue
            else:
                print("Choix invalide, veuillez réessayer.")
        elif choix == str(i):
            print("Fin.")
            break
        else:
            print("Choix invalide, veuillez réessayer.")
            

main()