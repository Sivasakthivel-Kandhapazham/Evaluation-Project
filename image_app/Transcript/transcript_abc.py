from abc import ABC, abstractmethod


class TranscriptGeneral(ABC):
    @abstractmethod
    def speech_to_text_openai(self):
        pass