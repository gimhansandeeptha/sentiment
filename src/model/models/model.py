from abc import ABC, abstractmethod

"""Creator"""
class Model(ABC):
    @abstractmethod
    def create(self):
        pass

    @abstractmethod
    def load(self, model_state_dict, optimizer_state_dict):
        pass

    @abstractmethod
    def train(self, train_loader):
        pass

    @abstractmethod
    def finetune(self, finetune_loader):
        pass

    @abstractmethod
    def validate(self, validation_loader)-> float:
        pass

    @abstractmethod
    def save(self, file_path):
        pass

    
