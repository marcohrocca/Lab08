from database.distributore_DAO import DistributoreDAO
'''
    MODELLO:
    - Rappresenta la struttura dati
    - Si occupa di gestire lo stato dell'applicazione
    - Interagisce con il database
'''

class Model:
    def __init__(self):
        self._distributori = None
        self.load_distributori()

        self.__sequenza_ottima = []
        self.__costo_ottimo = -1

    def load_distributori(self):
        """ Carica tutti i distributori e li setta nella variabile self._distributori """
        self._distributori = DistributoreDAO.get_distributori()


    def get_prezzo_medio(self, mese:int):
        """
        Calcola, per ogni distributore, il prezzo medio al litro per il mese selezionato.
        :param mese: Mese selezionato (un intero da 1 a 12)
        :return: lista di tuple --> (nome del distributore, media), es. (Distributore A, 1.789)
        """
        risultato=[]
        for distributore in self._distributori:
            prezzi=distributore.get_prezzi()#Metodo che abbiamo definito nel Distributore DTO, in questa maniera ottengo
                                      #i prezzi per ogni distributore
            # dai prezzi estraggo il mese con date.month,se il numero è uguale al mese parametro quel prezzo è valido,
            # a quel punto aggiungo tutti i prezzi validi a una lista per distributore e successivamente ne calcolo la media
            validi=[]
            for p in prezzi:
                if p.data.month==mese:
                    validi.append(p.prezzo_litro) #Unico valore che ci serve, mese già impostato e visto che sto facendo
                                                 #Ciclo per ogni distributore ho già nome del distributore
            if validi:
                media=round(sum(validi)/len(validi),3)
                risultato.append((distributore.nome,media))
        return risultato






    def get_sequenza_ottima(self, mese:int):
        """
        Calcola la sequenza ottimale di rifornimenti nei primi 7 giorni
        :return: sequenza di nomi distributore ottimale
        :return: costo ottimale (cioè quello minimizzato dalla sequenza scelta)
        """
        self.__sequenza_ottima = []
        self.__costo_ottimo = -1
        prezzi_settimana = self.__get_prezzi_prima_settimana_mese(mese)

        self.__ricorsione([], 1, None, 0, prezzi_settimana)

        # Traduci gli ID in nomi
        id_to_nome = {distributore.id: distributore.nome for distributore in self._distributori}
        sequenza_nomi = [f"Giorno {giorno}: {id_to_nome[i]}" for giorno, i in enumerate(self.__sequenza_ottima, start=1)]
        return sequenza_nomi, round(self.__costo_ottimo, 2)

    def __ricorsione(self, sequenza_parziale, giorno, ultimo_distributore, costo_corrente, prezzi_settimana):
        """ Implementa la ricorsione """

        #Questa funzione viene chiamata da get_sequenza_ottima
        if giorno>7: #condizione di terminazione della ricorsione,non viene più chiamata la funzione
            #Se giorno>7 abbiamo finito di calcolare la sequenza e possiamo restituire il suo valore
            if self.__costo_ottimo==-1 or self.__costo_ottimo>costo_corrente:
                self.__costo_ottimo=costo_corrente
                self.__sequenza_ottima=list(sequenza_parziale)   #Devo mettere list perchè ricorsione
                                                                #cancellerà sequenza_parziale ho bisogno di copia
            return self.__sequenza_ottima, self.__costo_ottimo

        else:   #Qui viene richiamata la funzione
                #Il costo viene calcolato così,se il distributore è uguale al precedente
                #costo=prezzo_giorno*100 se è diverso costo=prezzo_giorno*100+5
                #La ricorsione calcolerà possibilità su tutti i 7 giorni circa 2 alla 7 e
                # confronterà tra loro le sequenze per scegliere quella con valore minore

            for id_distributore in prezzi_settimana:
                # :return: un dizionario: {id_distributore: [prezzo_giorno1, ..., prezzo_giorno7]}
                costo=prezzi_settimana[id_distributore][giorno-1]*100  #Prezzo al litro per 100
                #Penalità scatta se non è il primo giorno ed è cambiato distributore
                if ultimo_distributore is not None and ultimo_distributore!=id_distributore:
                    #Significa se è primo giorno o è uguale allora no penalità
                    costo=costo+5 #Il costo per cambiare distributore

                #Non posso cambiare valore nel for sennò per a nessun problema,alla
                #seconda del for nella stessa ricorsione ovvero b avrò un giorno in più costo maggiore
                #oltre a list index out of range
                '''costo_corrente+=costo
                giorno+=1
                ultimo_distributore=sequenza_parziale[-1]'''
                sequenza_parziale.append(id_distributore)

                self.__ricorsione(sequenza_parziale,giorno+1,sequenza_parziale[-1], costo_corrente+costo, prezzi_settimana)
                sequenza_parziale.pop()
            return None






    def __get_prezzi_prima_settimana_mese(self, mese: int):
        """
        Restituisce i prezzi dei primi 7 giorni del mese selezionato per ciascun distributore.
        :return: un dizionario: {id_distributore: [prezzo_giorno1, ..., prezzo_giorno7]}
        """
        risultato={}
        for distributore in self._distributori:
            prezzi=distributore.get_prezzi() #Adesso ho tutti i prezzi per ogni distributore
            validi=[None]*7 #Per evitare index error
            for p in prezzi:
                if p.data.month==mese and 1 <= p.data.day <= 7:  #Controllo sia che siamo nel mese giusto,
                                                                 #sia che siamo nella prima settimana
                    giorno=p.data.day
                    validi[giorno-1]=p.prezzo_litro   #Uso giorno-1 per essere sicuro che siano ordinate le varie giornate
                                                      #nella lista
            risultato[distributore.id]=validi
        return risultato