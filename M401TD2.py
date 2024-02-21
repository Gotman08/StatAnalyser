class Tab2:
    def __init__(self, sizeX, sizeY, total) -> None:
        self.Tableau = {}
        self.sizeX = sizeX  # ligne
        self.sizeY = sizeY  # colonne
        self.total = total

    def remplir(self):
        valeurs_y = []  # Liste pour stocker temporairement les valeurs Y
        print("Entrez les valeurs de Y (colonnes) :")
        for _ in range(self.sizeY):
            y = input("Y = ")  # Pas de conversion en int
            valeurs_y.append(y)

        print("Entrez les valeurs pour chaque X et Y :")
        for _ in range(self.sizeX):
            x = input("X = ")  # Pas de conversion en int
            self.Tableau[x] = {}
            for y in valeurs_y:
                valeur = input(" X={} et Y={} : ".format(x,y))  # Pas de conversion en int, supposer que l'utilisateur entre une valeur numerique en chaine
                self.Tableau[x][y] = int(valeur)  # Convertir en int pour permettre des calculs si necessaire


    def toString(self):
        # Recuperer les valeurs de Y
        valeurs_y = list(next(iter(self.Tableau.values())).keys())
        # Entête pour Y
        header = "X/Y | "
        for y in valeurs_y:
            header += "{:>3} | ".format(y)
        print(header)
        print("-" * len(header))

        # Afficher les lignes de donnees
        for x, sous_tableau in sorted(self.Tableau.items()):
            row = "{:>3} | ".format(x)
            for y in valeurs_y:
                row += "{:>3} | ".format(sous_tableau[y])
            print(row.rstrip())  # rstrip() pour enlever l'espace supplementaire à la fin
    
    def distribution_marginalesX(self):
        # Calcul des distributions marginales
        distribution_x = {x: sum(self.Tableau[x].values()) for x in self.Tableau}
        return distribution_x
    
    def frequence_marginalesX(self) -> dict:
        print({x: str(sum(self.Tableau[x].values())) + "/{}".format(self.total) for x in self.Tableau})
        return {x: sum(self.Tableau[x].values())/self.total for x in self.Tableau}
    
    def distribution_marginalesY(self):
        # Calcul des distributions marginales
        distribution_y = {}
        for x in self.Tableau:
            for y in self.Tableau[x]:
                distribution_y[y] = distribution_y.get(y, 0) + self.Tableau[x][y]
        return distribution_y
    
    def moyenneX(self):
        # Calcul des distributions marginales de X
        distribution_x = self.distribution_marginalesX()
        # Calcul du total des frequences pour X
        total_x = sum(distribution_x.values())
        # Calcul de la moyenne de X en utilisant les valeurs de X et leurs frequences
        moyenne_x = sum(int(x) * freq for x, freq in distribution_x.items()) / total_x
        return moyenne_x

    
    def varianceX(self):
        # Calcul des distributions marginales de X
        distribution_x = self.distribution_marginalesX()
        # Conversion des cles en entiers et calcul du total des frequences pour X
        total_x = sum(distribution_x.values())
        # Calcul de la moyenne de X
        moyenne_x = sum(int(x) * freq for x, freq in distribution_x.items()) / total_x
        # Calcul de la variance de X
        variance_x = sum((int(x) - moyenne_x) ** 2 * freq for x, freq in distribution_x.items()) / total_x
        return variance_x

    
    def moyenneY(self):
        distribution_y = self.distribution_marginalesY()
        total_y = sum(distribution_y.values())
        moyenne_y = sum(float(y) * freq for y, freq in distribution_y.items()) / total_y
        return moyenne_y


    
    def varianceY(self):
        distribution_y = self.distribution_marginalesY()
        total_y = sum(distribution_y.values())
        moyenne_y = sum(int(y) * freq for y, freq in distribution_y.items()) / total_y
        variance_y = sum((int(y) - moyenne_y) ** 2 * freq for y, freq in distribution_y.items()) / total_y
        return variance_y

    
    def moyenne_conditionnelleY(self):
        moyennes_conditionnelles = {}
        # Calculer la distribution marginale de X pour connaître les totaux par X
        distribution_x = self.distribution_marginalesX()
        for x in distribution_x:
            total_freq_x = distribution_x[x]
            moyenne_y_given_x = {}
            for y in self.Tableau[next(iter(self.Tableau))]:  # Utilisez la première clé Y pour parcourir toutes les valeurs de Y
                if x in self.Tableau and y in self.Tableau[x]:
                    freq = self.Tableau[x][y]
                    moyenne_y_given_x[y] = int(y) * freq / total_freq_x  # Modifier ici pour inclure la pondération par la fréquence
            # Calculer la moyenne conditionnelle de Y sachant X
            moyennes_conditionnelles[x] = sum(moyenne_y_given_x.values())
        return moyennes_conditionnelles

        
    def variance_conditionnelleY(self):
        variances_conditionnelles = {}
        moyennes_conditionnelles = self.moyenne_conditionnelleY()  # Recuperer les moyennes conditionnelles une seule fois pour eviter de recalculer
        for x in self.Tableau:
            total_freq_x = sum(self.Tableau[x].values())
            moyenne_y_sachant_x = moyennes_conditionnelles[x]
            # Convertir y en flottant avant de proceder aux calculs
            variance_y_sachant_x = sum((float(y) - moyenne_y_sachant_x) ** 2 * freq for y, freq in self.Tableau[x].items()) / total_freq_x
            variances_conditionnelles[x] = variance_y_sachant_x
        return variances_conditionnelles



    def variance_conditionnelleX(self):
        variances_conditionnelles = {}
        # Assurez-vous d'avoir une methode pour calculer les moyennes conditionnelles de X sachant Y
        moyennes_conditionnelles = self.moyenne_conditionnelleX()  # Hypothetique, à implementer
        distribution_y = self.distribution_marginalesY()
        
        for y in distribution_y:
            # Initialiser la somme des carres des ecarts et le total pour cette valeur de Y
            somme_ecarts = 0
            total_freq_y = distribution_y[y]
            
            # Parcourir chaque X pour cette Y
            for x in self.Tableau:
                if y in self.Tableau[x]:
                    freq = self.Tableau[x][y]
                    ecart = (x - moyennes_conditionnelles[y]) ** 2
                    somme_ecarts += ecart * freq
            
            # Calculer la variance conditionnelle pour cette valeur de Y
            variance_x_sachant_y = somme_ecarts / total_freq_y
            variances_conditionnelles[y] = variance_x_sachant_y
        
        return variances_conditionnelles


    # x sachant y
    def distribution_conditionnelleX(self):
        distribution_cond = {}
        # Calculer la distribution marginale de Y pour connaître les totaux par Y
        distribution_y = self.distribution_marginalesY()
        for y in distribution_y:
            total_freq_y = distribution_y[y]
            freq_x_given_y = {}
            for x in self.Tableau:
                if y in self.Tableau[x]:
                    freq_x_given_y[x] = self.Tableau[x][y]
            # Calculer la distribution conditionnelle de X sachant Y
            distribution_cond[y] = {x: freq / total_freq_y for x, freq in freq_x_given_y.items()}
        return distribution_cond


    # y sachant x
    def distribution_conditionnelleY(self):
        distribution_cond = {}
        for x in self.Tableau:
            total_freq_x = sum(self.Tableau[x].values())
            distribution_cond[x] = {y: freq / total_freq_x for y, freq in self.Tableau[x].items()}
        return distribution_cond
    
    def moyenne_conditionnelleX(self):
        moyennes_conditionnelles = {}
        # Calculer la distribution marginale de Y pour connaître les totaux par Y
        distribution_y = self.distribution_marginalesY()
        for y in distribution_y:
            total_freq_y = distribution_y[y]
            moyenne_x_given_y = {}
            for x in self.Tableau:
                if y in self.Tableau[x]:
                    freq = self.Tableau[x][y]
                    moyenne_x_given_y[x] = int(x) * freq / total_freq_y  # Modifier ici pour inclure la pondération par la fréquence
            # Calculer la moyenne conditionnelle de X sachant Y
            moyennes_conditionnelles[y] = sum(moyenne_x_given_y.values())
        return moyennes_conditionnelles
    
    def frequence_marginalesY(self) -> dict:
        print({y: str(sum(self.Tableau[x][y] for x in self.Tableau)) + "/{}".format(self.total) for y in self.Tableau[next(iter(self.Tableau))]})
        return {y: sum(self.Tableau[x][y] for x in self.Tableau)/self.total for y in self.Tableau[next(iter(self.Tableau))]}

    def frequence_Theroique(self):
        #frequnence theorique = frequnence marginale de x * frequnence marginale de y
        freqX = self.frequence_marginalesX()
        freqY = self.frequence_marginalesY()
        freqTheorique = {}
        for y in freqY:
            for x in freqX:
                freqTheorique["[{} : ({})]".format(y,x)] = freqY[y] * freqX[x]

        print(freqTheorique)


# Creation et utilisation de l'instance de Tab2
def main():
    sizeX = int(input('sizeX = '))
    sizeY = int(input('sizeY = '))
    total = float(input('total = '))

    tab2 = Tab2(sizeX, sizeY, total)  # Créer une instance de Tab2
    tab2.remplir()  # Remplir le tableau avec des données
    tab2.toString()  # Afficher le contenu du tableau

    while True:
        print("\nMenu:")
        print("1. Distribution marginales")
        print("2. Moyenne global")
        print("3. Variance global")
        print("4. Moyenne conditionnelle")
        print("5. Variance conditionnelle")
        print("6. Distribution conditionnelle")
        print("7. Afficher Tableau")
        print("8. fréquence")
        print("9. Quitter")

        choix = input("\nEntrez votre choix : ")

        if choix == '1':
            print("1. X")
            print("2. Y")
            print("3. Retour au menu principal")
            margianal_choix = input("Entez votre choix : ")
            if margianal_choix == '1':
                print(tab2.distribution_marginalesX())
            elif margianal_choix == '2':
                print(tab2.distribution_marginalesY())
            elif margianal_choix == '3':
                continue
            else:
                print("Choix invalide, veuillez reessayer.")
        elif choix == '2':
            print("1. X")
            print("2. Y")
            print("3. Retour au menu principal")
            moyenne_choix = input("Entez votre choix : ")
            if moyenne_choix == '1':
                print(tab2.moyenneX())
            elif moyenne_choix == '2':
                print(tab2.moyenneY())
            elif moyenne_choix == '3':
                continue
            else:
                print("Choix invalide, veuillez reessayer.")
        elif choix == '3':
            print("1. X")
            print("2. Y")
            print("3. Retour au menu principal")
            variance_choix = input("Entez votre choix : ")
            if variance_choix == '1':
                print(tab2.varianceX()) 
            elif variance_choix == '2':
                print(tab2.varianceY())
            elif variance_choix == '3':
                continue
            else:
                print("Choix invalide, veuillez reessayer.")
        elif choix == '4':
            print("1.X sachant Y :")
            print("2.Y sachant X :")
            print("3. Retour au menu principal")
            choix_con = input("Entez votre choix : ")
            if choix_con == '1':
                print(tab2.moyenne_conditionnelleX())
            elif choix_con == '2':
                print(tab2.moyenne_conditionnelleY())
            elif choix_con == '3':
                continue
            else:
                print("Choix invalide, veuillez reessayer.")
        elif choix == '5':
            print("1.X sachant Y :")
            print("2.Y sachant X :")
            print("3. Retour au menu principal")
            choix_var = input("Entez votre choix : ")
            if choix_var == '1':
                print(tab2.variance_conditionnelleX())
            elif choix_var == '2':
                print(tab2.variance_conditionnelleY())
            elif choix_var == '3':
                continue
            else:
                print("Choix invalide, veuillez reessayer.")
        elif choix == '6':
            print("1.X sachant Y :")
            print("2.Y sachant X :")
            print("3. Retour au menu principal")
            choix_var = input("Entez votre choix : ")
            if choix_var == '1':
                print(tab2.distribution_conditionnelleX())
            elif choix_var == '2':
                print(tab2.distribution_conditionnelleY())
            elif choix_var == '3':
                continue
            else:
                print("Choix invalide, veuillez reessayer.")

        elif choix == '7':
            tab2.toString()
        elif choix == '8':
            print("1. Marginale de X")
            print("2. Marginale de Y")
            print("3. Theorique")
            print("4. Retourner au menu principal")
            choix_marg = input("Entez votre choix : ")
            if choix_marg == '1':
                tab2.frequence_marginalesX()
            elif choix_marg == '2':
                tab2.frequence_marginalesY()
            elif choix_marg == '3':
                tab2.frequence_Theroique()
            elif choix_marg == '4':
                continue
            else:
                print("Choix invalide, veuillez reessayer.")
        elif choix == '9':
            print("Fin.")
            break
        else:
            print("Choix invalide, veuillez reessayer.")

main()
