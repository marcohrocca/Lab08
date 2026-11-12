from database.distributore_DAO import DistributoreDAO
from datetime import datetime #Importo librerai tempo per estrarre i mesi
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
        # TODO

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