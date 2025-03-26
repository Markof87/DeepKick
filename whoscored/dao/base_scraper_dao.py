from abc import ABC, abstractmethod

# DAO Base: interfaccia per lo scraping che restituisce oggetti Match
class BaseScraperDAO(ABC):
    @abstractmethod
    def fetch_data(self):
        """
        Recupera i dati dalla fonte e restituisce una lista di oggetti Match.
        """
        pass