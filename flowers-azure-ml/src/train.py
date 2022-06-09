import numpy as np
import torch
from torch.utils.data import DataLoader
from torch.optim.lr_scheduler import ReduceLROnPlateau
from pathlib import Path

from config import opt
from models import FlowersConvModel
from utils import train_model, get_images_paths, get_train_test_split, init_seeds
from datasets import FlowersDataset
from datasets.preprocessing import train_transformations, val_transformations

### Add References
import argparse
from azureml.core import Run, Model
from azureml.core.resource_configuration import ResourceConfiguration


parser = argparse.ArgumentParser()
parser.add_argument('--data-folder', type=str, dest='data_folder', help='data folder mounting point')
args = parser.parse_args()
opt.path_to_data = Path(args.data_folder) / 'flower_photos_selected'


if __name__ == '__main__':
    run = Run.get_context()

    init_seeds(opt.seed)
    num_classes = len(set(opt.idx_to_class.keys()))

    data_df = get_images_paths(opt=opt)
    train_df, val_df = get_train_test_split(df=data_df, opt=opt)

    train_dataset = FlowersDataset(
        img_paths=train_df['path'].values.copy(),
        labels=train_df['label'].values.copy(),
        num_classes=num_classes,
        transform=train_transformations,
        use_descriptors_as_features=opt.use_descriptors_as_features,
        features_type=opt.features_type,
    )

    train_dataloader = DataLoader(
        train_dataset,
        batch_size=opt.batch_size,
        shuffle=True,
        num_workers=opt.num_workers,
        pin_memory=opt.pin_memory,
    )

    val_dataset = FlowersDataset(
        img_paths=val_df['path'].values.copy(),
        labels=val_df['label'].values.copy(),
        num_classes=num_classes,
        transform=val_transformations,
        use_descriptors_as_features=opt.use_descriptors_as_features,
        features_type=opt.features_type,
    )

    val_dataloader = DataLoader(
        train_dataset,
        batch_size=opt.batch_size,
        shuffle=False,
        num_workers=opt.num_workers,
        pin_memory=opt.pin_memory,
    )

    model = FlowersConvModel(
        encoder_name=opt.encoder_name, pretrained=opt.pretrained, num_classes=num_classes
    ).to(opt.device)
    # model.freeze_middle_layers()

    criterion = torch.nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(filter(lambda p: p.requires_grad, model.parameters()), lr=opt.lr)
    scheduler = ReduceLROnPlateau(optimizer, mode='min', patience=2, factor=0.1, verbose=True)

    train_model(run, model, optimizer, scheduler, criterion, train_dataloader, val_dataloader, opt, target_metric='f1_avg', best_target_metric=-np.inf)

    # Register the model
    print('Registering model...')
    Model.register(
        workspace=run.experiment.workspace,
        model_path='outputs/models/FlowersConvModel_model_best.pth',
        model_name='Flowers-clf-PyTorch',
        description="Flowers PyTorch Classifier",
        tags={'Training context': 'Pipeline'},
        resource_configuration=ResourceConfiguration(cpu=1, memory_in_gb=2)
    )

    print('Finish!')
    run.complete()
