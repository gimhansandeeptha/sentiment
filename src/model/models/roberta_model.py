import torch
from transformers import RobertaTokenizer
from src.model.models.model import Model
from src.model.models.finetune.roberta_finetune import RobertaFinetune
from src.model.models.validate.roberta_validate import RobertaValidate
from model.models.roberta import RobertaClass
from src.model.models.inference.roberta_inference import RobertaInference

"""Concreate factory for Roberta models"""
class RobertaModel(Model):
    def __init__(self) -> None:
        self.model: torch.nn.Module = None
        self.tokenizer = None
        self.loss_function = None
        self.optimizer = None
        self.max_len = 256
        self.device = "cpu"
    
    def create(self):
        model = RobertaClass() # This model can be changed to different model architecture. in roberta_models folder.
        self.model = model

        tokenizer = RobertaTokenizer.from_pretrained('roberta-base', truncation=True, do_lower_case=True)
        self.tokenizer = tokenizer

        loss_function = torch.nn.CrossEntropyLoss()
        self.loss_function = loss_function

        LEARNING_RATE = 1e-05
        optimizer = torch.optim.Adam(params=model.parameters(), lr=LEARNING_RATE)
        self.optimizer = optimizer
    
    def load(self, file_path):
        checkpoint: dict=torch.load(file_path)
        model_state_dict = checkpoint.get("model_state_dict")
        optimizer_state_dict = checkpoint.get("optimizer_state_dict")
        self.model.load_state_dict(model_state_dict)
        self.optimizer.load_state_dict(optimizer_state_dict)

    def train(self, train_loader):
        pass
    
    def finetune(self, finetune_loader):
        finetune = RobertaFinetune(self.model, self.optimizer, self.loss_function)
        finetune(self.model, finetune_loader)

    def validate(self, validation_loader) -> float:
        validate = RobertaValidate(self.model, self.loss_function)
        validation_loss = validate.validate(validation_loader)
        return validation_loss
    
    def infer(self, text):
        infer = RobertaInference(self.model, self.tokenizer, self.max_len, self.device)
        return infer.inference(text)

    def save(self, file_path):
        checkpoint = {
            'model_state_dict': self.model.state_dict(),
            'optimizer_state_dict': self.optimizer.state_dict(),
        }
        torch.save(checkpoint, file_path)
