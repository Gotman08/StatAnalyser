

diagrammes = True
try:
    import matplotlib.pyplot as plt
except ImportError:
    print("L'option des diagrammes indisponible")
    diagrammes = False

try:
    import numpy as np
except ImportError:
    print("L'option des diagrammes indisponible")
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
        self.ci()
        self.ai()
        self.fi()
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

    def verifierPlagesConsecutives(self):
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
            
                
        return self.verifierPlagesConsecutives()
    
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
            print("Erreur dans les donnees : "+str(e))
            self.AfficherFormules()
            return None


    def moyenne(self) -> float:
        try:
            somme = 0
            for plage, data in self.classes.items():
                ni = data[0]  
                ci = data[1]  
                somme += ni * ci
            return somme / self.total
        except Exception as e:
            print("Erreur dans les donnees : "+str(e))
            return None


    def calculer_coefficients(self):
        moy = self.calculerMoyennePonderee()
        s = self.variance() ** 0.5  
        n = self.total
        m3 = sum([(data[1] - moy) ** 3 * data[0] for _, data in self.classes.items()]) / n
        m4 = sum([(data[1] - moy) ** 4 * data[0] for _, data in self.classes.items()]) / n
        skewness = m3 / (s ** 3)  
        kurtosis = m4 / (s ** 4) - 3  
        return skewness, kurtosis
    
    def quartiles_interpolation(self):
        # Calculer les positions des quartiles
        Q1_pos = self.total / 4
        Median_pos = self.total / 2
        Q3_pos = 3 * self.total / 4
        
        # Initialisation des variables pour stocker les resultats des quartiles
        Q1 = None
        Median = None
        Q3 = None
        
        # Frequence cumulee precedente
        F_prev = 0
        
        # Trier les classes par leur limite inferieure pour s'assurer de l'ordre
        sorted_classes = sorted(self.classes.items(), key=lambda x: x[0][0])
        
        for (exmin, exmax), data in sorted_classes:
            ni = data[0]  # Nombre d'appareils dans la classe
            Fi = F_prev + ni  # Frequence cumulee jusqu'à cette classe
            ai = exmax - exmin  # Amplitude de la classe
            
            # Calcul de Q1 si pas encore trouve et que la position est atteinte
            if Q1 is None and Fi >= Q1_pos:
                Q1 = exmin + ((Q1_pos - F_prev) / ni) * ai
            
            # Calcul de la Mediane
            if Median is None and Fi >= Median_pos:
                Median = exmin + ((Median_pos - F_prev) / ni) * ai
            
            # Calcul de Q3
            if Q3 is None and Fi >= Q3_pos:
                Q3 = exmin + ((Q3_pos - F_prev) / ni) * ai
            
            F_prev = Fi  # Mise à jour de la frequence cumulee pour la prochaine iteration
            
            # Arrêter les calculs si tous les quartiles sont trouves
            if Q1 is not None and Median is not None and Q3 is not None:
                break
        
        return Q1, Median, Q3
        
    #! ecart type
    def ecart_type(self):
        try:
            return self.variance() ** 0.5
        except Exception as e:
            print("Erreur dans les donnees : "+str(e))
            return None

    #! coefficient de variation
    def coefficient_variation(self):
        try:
            return self.ecart_type() / self.moyenne()
        except Exception as e:
            print("Erreur dans les donnees : "+str(e))
            return None
        

    
    def AfficherFormules(self)->None:
        
        print("ci = (exmax + exmin)/2")
        print("ci = min + max /2, c'est la moyenne des extremites")
        print("fi = ni/total fi")
        print("fi = ni/n, c'est la frequence de la classe")
        print("ai = exmax - exmin")
        print("ai = max - min, c'est la largeur de la classe")
        print("Fi = somme(fi), simga fi, du genre f1 f2 f3 ... fn")
        print("Fi = somme(fi), simga fi, c'est la frequence cumulee de la classe")
        print("hi = (fi/ai)*" + str(self.coef) + "hi")
        print("hi = (fi/ai)*"+str(self.coef)+"HI, c'est la densite de la classe")
        print("Moyenne = somme(ci*ni)/total")
        print("Moyenne = somme(ci*ni)/total, c'est la moyenne ponderee")
        print("Variance = somme(ni*(ci-moyenne)^2)/total")
        print("Variance = somme(ni*(ci-moyenne)^2)/total, c'est la variance ponderee")
        print("Quartiles = interpolation des quartiles, exmin + (((pos - prev_Fi) / fi) * ai)")
        print("Calcul des coefficients d'asymetrie et d'aplatissement formule: skewness = m3 / (s ** 3) et kurtosis = m4 / (s ** 4) - 3")
        print("""
    Interpolation Lineaire = L + (((N / 2) - F) / f) * C

    * L est la limite inferieure de la classe mediane,
     
    * N est le nombre total d'observations,
    
    * F est la frequence cumulee avant la classe mediane,
    
    * f est la frequence de la classe mediane,
    
    * C est l'amplitude de la classe mediane.
    """)

    def toString(self)-> None:
        
        # dict_items([((15000.0, 35000.0), [8160.0, 25000.0, 20000.0, 20000.0, 10000.0]), ((85000.0, 103905.60875512997), [3655.0, 94452.80437756499, 18905.60875512997, 38905.60875512997, 4859.353023909987])])

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

        try:
            print("Ecart type: "+str(self.ecart_type()))
        except Exception as e:
            print("Erreur dans l'ecart type : "+str(e))
        
        try:
            print("Coefficient de variation: "+str(self.coefficient_variation()))
        except Exception as e:
            print("Erreur dans le coefficient de variation : "+str(e))


#! definition de la classe Tab2 en deduire quels fonction sont utilisable
    def Type(self):
        print("Variables qualitatives : Representent des caracteristiques non numeriques, comme le genre, la couleur, etc.")
        print("Variables quantitatives : Representent des mesures numeriques ou des quantites.")
    
    def Paremetre(self):
        print("Moyenne (ou espérance) : Indique la valeur moyenne d'une distribution de données.")
        print("Médiane : La valeur médiane sépare l'échantillon en deux parties égales.")
        print("Mode : La valeur qui apparaît le plus fréquemment dans un ensemble de données.")
        print("Écart-type : Mesure la dispersion des valeurs autour de la moyenne.")
        print("Variance : La moyenne des carrés des écarts par rapport à la moyenne.")
        print("Minimum et maximum : Les valeurs les plus petites et les plus grandes dans un ensemble de données.")
        print("Quartiles : Les valeurs qui divisent un ensemble de données ordonné en quatre parties égales.")
        print("Étendue : La différence entre la valeur maximale et la valeur minimale.")
        print("Skewness (asymétrie) : Mesure l'asymétrie de la distribution des données par rapport à la moyenne.")
        print("Kurtosis (aplatissement) : Mesure à quel point la distribution des données est concentrée autour de la moyenne.")
    
    def Cours(self):
        print("fi/j = (fij)/(f.j)")
        print("fj/i = (fji)/(fi.)")
        print("Lorsque X et Y indépendants")
        print("fij = (f.i)^fi/j = fi.*fj/i = f.j*fi.")
        print("nij/n = n.j/n * ni./n <=> nij = ni.*n.j/n")
        print("Khi-deux = somme((ni,j - n_i.n_.j)^2 / (n_i.n_.j))")
        print("ni,j: Fréquence observée dans la cellule (i, j).")
        print("n_i. et n_.j: Totaux marginaux de la ligne i et de la colonne j.")
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
                masse = float(input("masse classe "+str(i+1)+" : "))
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
        print("{}. Verifier Donnees".format(i)); i += 1
        print("{}. Afficher formules".format(i)); i += 1
        print("{}. Afficher donnees".format(i)); i += 1
        print("{}. Afficher definition".format(i)); i += 1
        if diagrammes:
            print("{}. Diagrammes".format(i)); i += 1
        print("{}. Quitter".format(i))
        
        choix = input("Entrez votre choix: ")
        
        if choix == '1':
            tab.remplirClasses()
        elif choix == '2':
            tab.calculer()
            print("Calculs effectues.")
        elif choix == '3':
            if tab.verif() and tab.verifierPlagesConsecutives():
                print("Toutes les verifications sont passees.")
            else:
                print("Erreur dans les donnees.")
        elif choix == '4':
            tab.AfficherFormules()
        elif choix == '5':
            tab.toString()
        elif choix =='6':
            print("1. Type")
            print("2. Parametre")
            print("3. Cours")
            print("4. Retour au menu principal")
            definition_choix = input("Entrez votre choix: ")
            if definition_choix == '1':
                tab.Type()
            elif definition_choix == '2':
                tab.Paremetre()
            elif definition_choix == '3':
                tab.Cours()
            elif definition_choix == '4':
                continue
            else:
                print("Choix invalide, veuillez reessayer.")
        elif choix == '7' and diagrammes:
            print("Diagrammes:")
            print("1. Diagramme differentiel")
            print("2. Diagramme integral")
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
                print("Non implemente.")
            elif diagramme_choix == '5':
                tab.dessiner_box_plot()
            elif diagramme_choix == '6':
                continue
            else:
                print("Choix invalide, veuillez reessayer.")
        elif choix == str(i):
            print("Fin.")
            break
        else:
            print("Choix invalide, veuillez reessayer.")

            

main()
