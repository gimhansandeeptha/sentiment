import torch
from tqdm import tqdm

class RobertaValidate:
    def __init__(self, model, loss_function) -> None:
        self.model = model
        self.loss_function = loss_function

    def _calculate_accuracy(self,preds, targets):
        n_correct = (preds==targets).sum().item()
        return n_correct
    
    def validate(self, validation_loader, device="cpu"):
        self.model.eval()
        val_loss = 0
        n_correct = 0
        nb_val_steps = 0
        nb_val_examples = 0

        with torch.no_grad():
            for _, data in tqdm(enumerate(validation_loader, 0)):
                ids = data['ids'].to(device, dtype=torch.long)
                mask = data['mask'].to(device, dtype=torch.long)
                token_type_ids = data['token_type_ids'].to(device, dtype=torch.long)
                targets = data['targets'].to(device, dtype=torch.long)

                outputs = self.model(ids, mask, token_type_ids)
                loss = self.loss_function(outputs, targets)
                val_loss += loss.item()
                big_val, big_idx = torch.max(outputs.data, dim=1)
                n_correct += self._calculate_accuracy(big_idx, targets)

                nb_val_steps += 1
                nb_val_examples += targets.size(0)

        val_accuracy = (n_correct * 100) / nb_val_examples
        val_loss /= nb_val_steps
        return val_loss