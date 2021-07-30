import argparse
import data_loader.data_loader as module_data
import model.loss as module_loss
import model.metric as module_metric
import model.model as module_arch
import utils.visualizer as module_vis
from parse_config import ConfigParser
from trainer import Trainer
from sacred import Experiment
import transformers

ex = Experiment('train')
@ex.main
def run():
    logger = config.get_logger('train')

    if config['visualizer']['type'] != "":
        visualizer = config.initialize(
            name='visualizer',
            module=module_vis,
            exp_name=config['name'],
            web_dir=config._web_log_dir
        )
    else:
        visualizer = None

    # build tokenizer
    tokenizer = transformers.AutoTokenizer.from_pretrained(config['arch']['args']['text_params']['model'], TOKENIZERS_PARALLELISM=False)

    # setup data_loader instances
    data_loader = config.initialize('data_loader', module_data)
    config['data_loader']['args']['split'] = 'val'
    valid_data_loader = config.initialize('data_loader', module_data)
    print('Train dataset: ', len(data_loader.sampler), ' samples')
    print('Val dataset: ', len(valid_data_loader.sampler), ' samples')
    # build model architecture, then print to console
    config['arch']['args']['experts_used'] = data_loader.dataset.experts_used

    model = config.initialize('arch', module_arch)
    logger.info(model)

    # get function handles of loss and metrics
    loss = config.initialize(name="loss", module=module_loss)
    metrics = [getattr(module_metric, met) for met in config['metrics']]
    # build optimizer, learning rate scheduler. delete every lines containing lr_scheduler for disabling scheduler
    trainable_params = filter(lambda p: p.requires_grad, model.parameters())
    optimizer = config.initialize('optimizer', transformers, trainable_params)
    lr_scheduler = None
    if 'lr_scheduler' in config._config:
        if hasattr(transformers, config._config['lr_scheduler']['type']):
            lr_scheduler = config.initialize('lr_scheduler', transformers, optimizer)
        else:
            print('lr scheduler not found')
    if config['trainer']['neptune']:
        writer = ex
    else:
        writer = None
    trainer = Trainer(model, loss, metrics, optimizer,
                      config=config,
                      data_loader=data_loader,
                      valid_data_loader=valid_data_loader,
                      lr_scheduler=lr_scheduler,
                      visualizer=visualizer,
                      writer=writer,
                      tokenizer=tokenizer,
                      max_samples_per_epoch=config['trainer']['max_samples_per_epoch'],
                      init_val=config['trainer']['init_val'])

    trainer.train()


if __name__ == '__main__':
    args = argparse.ArgumentParser(description='PyTorch Template')
    args.add_argument('-c', '--config', default=None, type=str,
                      help='config file path (default: None)')
    args.add_argument('-r', '--resume', default=None, type=str,
                      help='path to latest checkpoint (default: None)')
    args.add_argument('-d', '--device', default=None, type=str,
                      help='indices of GPUs to enable (default: all)')
    args.add_argument('-o', '--observe', action='store_true',
                      help='Whether to observe (neptune)')

    config = ConfigParser(args)
    ex.add_config(config._config)

    if config['trainer']['neptune']:
        from neptunecontrib.monitoring.sacred import NeptuneObserver
        raise ValueError("Neptune credentials not yet added")
        ex.observers.append(NeptuneObserver(
            api_token='',
            project_name=''))
        ex.run()
    else:
        run()
