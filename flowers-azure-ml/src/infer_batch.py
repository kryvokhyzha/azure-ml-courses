import os
import torch
import cv2
from azureml.core import Model
from models import FlowersConvModel
from datasets.preprocessing import val_transformations
from config import opt


def prepare_data_for_model(path_to_image, transform=None):
    image = cv2.imread(path_to_image)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    if transform is not None:
        image = transform(image=image)['image']
        
    return image.unsqueeze(0)


def init():
    # Runs when the pipeline step is initialized
    global model

    # load the model
    num_classes = len(set(opt.idx_to_class.keys()))
    model_path = Model.get_model_path('Flowers-clf-PyTorch')
    model = FlowersConvModel(
        encoder_name=opt.encoder_name, pretrained=opt.pretrained, num_classes=num_classes
    ).to(opt.device)
    model.load_state_dict(torch.load(model_path)['state_dict'])
    model.eval()


def run(mini_batch):
    # This runs for each batch
    resultList = []

    # process each file in the batch
    with torch.no_grad():
        for image_path in mini_batch:
            image = prepare_data_for_model(image_path, transform=val_transformations)
        
            image = image.to(opt.device)
            output = model(image)
            predicted_class = torch.argmax(output, dim=1).detach().cpu().numpy().reshape(1, -1)
            # Append prediction to results
            resultList.append("{}: {}".format(os.path.basename(image_path), predicted_class[0]))
    return resultList
