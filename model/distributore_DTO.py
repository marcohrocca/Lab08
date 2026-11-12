from dataclasses import dataclass
from database.prezzo_DAO import PrezzoDAO   #Importo database con i prezzi

'''
    DTO (Data Transfer Object) dell'entità Distributore
'''

@dataclass()
class Distributore:
    id: int
    nome: str
    indirizzo: str

    # RELAZIONI
    lista_prezzi: list = None #Lista dei prezzi di un oggetto distributore inizializzata come none in partenza

    #Tipo di ORM
    def get_prezzi(self):
        """ Aggiorna e Restituisce la lista di prezzi (self.lista_prezzi) associati al distributore"""
        self.lista_prezzi=PrezzoDAO().get_prezzi(self.id) #La lista prezzi adesso vale ciò che mi da DAO tramite metodo get_prezzi
                                                          #che ha già come parametro l'id distributore
        return self.lista_prezzi #Restituisco la lista dei prezzi aggiornata

    def __eq__(self, other):
        return isinstance(other, Distributore) and self.id == other.id

    def __str__(self):
        return f"{self.id} | {self.nome} | Indirizzo: {self.indirizzo}"

    def __repr__(self):
        return f"{self.id} | {self.nome} | Indirizzo: {self.indirizzo}"

'''
if __name__ == '__main__':
    print(PrezzoDAO().get_prezzi(1))
chiedere come fare per questo debug
'''
