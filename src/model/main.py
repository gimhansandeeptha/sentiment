from src.model.models.model import Model
from src.model.models.roberta_model import RobertaModel

class Main:
    def __init__(self) -> None:
        self.model_creator: Model = None

    def create_model(self):
        self.model_creator = RobertaModel()
        self.model_creator.create()

    def load(self, file_path):
        self.model_creator.load(file_path)
    
    def finetune(self, finetune_loader):
        self.model_creator.finetune(finetune_loader)

    def validate(self, validation_loader):
        self.model_creator.validate(validation_loader)
