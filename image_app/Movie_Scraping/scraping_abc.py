from abc import ABC, abstractmethod


class WebScraping(ABC):
    @abstractmethod
    def imdb_web_scraping(self):
        pass

    @abstractmethod
    def metacritic_web_scraping(self):
        pass