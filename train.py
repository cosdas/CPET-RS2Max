import logging

import yaml
from aim import Repo
from omegaconf import OmegaConf
from rich.logging import RichHandler

from utils.exp import VO2Experiment

logging.basicConfig(
    level=logging.INFO,
    format='%(message)s',
    datefmt='[%X]',
    handlers=[RichHandler(show_path=False)],
)
repo = Repo('.')

default_filters = [['majdysrh', '=', 0], ['myocisch', '=', 0]]
# Default filters for neither major dysrhythmia nor myocardial ischemia
model_mapping = {}


def run_exp(group, time_list, filters, fold, args, full_load, drop_ci=False):
    drop_columns = args.drop_columns.copy()
    if drop_ci and 'ci' not in drop_columns:
        drop_columns.append('ci')
    experiment = VO2Experiment(
        group=group,
        time_list=time_list,
        filters=filters,
        fold=fold,
        version=args.version,
        drop_columns=drop_columns,
        repo=repo,
        full_load=full_load,
    )
    experiment.fit_and_evaluate()
    experiment.close()
    model_mapping[f'{group}_{time_list}{"_(-ci)" if drop_ci else ""}'] = experiment.id


def main():
    """
    Arguments:
    - filters: List of filters to apply to the data. (ex. ['majdysrh', '=', 0])
    - version: Version of the experiment to run
    - drop_columns: List of columns to drop from the dataset. (ex. ['ci'])
    - gender_group: 'all', 'each' - whether to run the experiment for all or each gender separately.
    - full_load: Whether to load the entire dataset or hold out data for cross-validation.
    - time_list List of features to include (0: Demographic, 1: Rest, 2: Submaximal) (ex. [[0], [0, 1], [0, 1, 2]])
    """

    args = OmegaConf.create(
        dict(
            filters=[],
            version='default',
            drop_columns=[],
            gender_group='all',
            full_load=False,
            time_list=[[0], [0, 1], [0, 1, 2]],
        )
    )
    args.merge_with_cli()
    assert args.gender_group in ['all', 'each']
    full_load = args.full_load
    print(args)
    groups = ['NG', 'OG', 'NG+OG']
    filter = default_filters + args.filters

    if args.gender_group == 'all':
        for group in groups:
            for time in args.time_list:  # 0: Demographic, 1: Rest, 2: Submaximal
                if full_load:
                    run_exp(group, time, filter, 0, args, full_load=full_load)
                    if time == [0, 1, 2]:  # If all time features are included, also run without CI
                        run_exp(group, time, filter, 0, args, full_load=full_load, drop_ci=True)
                else:
                    for fold in range(5):  # 5-fold cross validation
                        run_exp(group, time, filter, fold, args, full_load=full_load)
    else:
        for gender_filter in [['gender', '=', 0], ['gender', '=', 1]]:
            nf = filter + [gender_filter]
            for group in groups:
                for time in args.time_list:
                    if full_load:
                        run_exp(group, time, nf, 0, args, full_load=full_load)
                    else:
                        for fold in range(5):
                            run_exp(group, time, nf, fold, args, full_load=full_load)


if __name__ == '__main__':
    main()

    with open('data/model_mapping.yml', 'w') as f:
        yaml.dump(model_mapping, f, default_flow_style=False)
