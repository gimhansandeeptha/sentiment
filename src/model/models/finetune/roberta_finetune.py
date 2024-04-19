import torch
from tqdm import tqdm

class RobertaFinetune():
    def __init__(self, model: torch.nn.Module, optimizer, loss_function, early_stopping_patience=3) -> None:
        self.model: torch.nn.Module = model
        self.loss_function = loss_function
        self.optimizer = optimizer
        self.early_stopping_patience = early_stopping_patience
        self.min_val_loss = float('inf')
        self.no_improvement_count = 0

    def calculate_accuracy(self,preds, targets):
        n_correct = (preds==targets).sum().item()
        return n_correct

    # Finetuning loop
    def finetune(self, training_loader, device='cpu', epochs=3):
        self.model.train()     
        for epoch in range(epochs):
            tr_loss = 0
            n_correct = 0
            nb_tr_steps = 0
            nb_tr_examples = 0

            for _, data in tqdm(enumerate(training_loader, 0)):
                ids = data['ids'].to(device, dtype=torch.long)
                mask = data['mask'].to(device, dtype=torch.long)
                token_type_ids = data['token_type_ids'].to(device, dtype=torch.long)
                targets = data['targets'].to(device, dtype=torch.long)

                outputs = self.model(ids, mask, token_type_ids)
                loss = self.loss_function(outputs, targets)
                tr_loss += loss.item()
                big_val, big_idx = torch.max(outputs.data, dim=1)
                n_correct += self.calculate_accuracy(big_idx, targets)

                nb_tr_steps += 1
                nb_tr_examples += targets.size(0)

                self.optimizer.zero_grad()
                loss.backward()
                self.optimizer.step()

        return self.model