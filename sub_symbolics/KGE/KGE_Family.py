# This is a script to benchmark knowledge graph embeddings on the Family Dataset
# The  models and baselines are specified in conf_kge.json

from pykeen.triples import TriplesFactory
from pykeen.pipeline import pipeline
import torch
import json
import argparse
from pathlib import Path
from pykeen.losses import BCEWithLogitsLoss


class ExperimentConf(object):
    "transforms conf_dict to object"

    def __init__(self, conf_dict):
        for key, value in conf_dict.items():
            setattr(self, key, value)


def preprocess(dataset_name, data_path, create_inverse_triples=False):
    # load data
    Path(Path.cwd() / 'KGE_results' / dataset_name).mkdir(parents=True, exist_ok=True)
    all_triples = TriplesFactory.from_path(data_path / 'all.txt')
    train = TriplesFactory.from_path(data_path / 'train.txt', entity_to_id=all_triples.entity_to_id,
                                     relation_to_id=all_triples.relation_to_id,
                                     create_inverse_triples=create_inverse_triples)
    valid = TriplesFactory.from_path(data_path / 'valid.txt', entity_to_id=all_triples.entity_to_id,
                                     relation_to_id=all_triples.relation_to_id)
    test = TriplesFactory.from_path(data_path / 'test.txt', entity_to_id=all_triples.entity_to_id,
                                    relation_to_id=all_triples.relation_to_id)
    print(f"Data loaded. Train: {train}\n\nValid: {valid}\n\nTest: {test}")
    return train, valid, test


if __name__ == '__main__':
    # if torch.backends.mps.is_available():
    #    device = torch.device("mps")
    # else:
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f'Device: {device}', flush=True)

    # load configurations
    parser = argparse.ArgumentParser(description='Experiments')
    parser.add_argument('config', metavar='file', type=str, help='config file in json format')
    parser.add_argument('dataset_name')
    args = parser.parse_args()
    with open(args.config, 'r') as f:
        json_content = json.loads(f.read())
    dataset_name = args.dataset_name #family_small or family_medium or FB15k-237
    print(f'dataset: {dataset_name}', flush=True)
    # start experiment per conf
    for _conf in json_content['configs']:
        conf = ExperimentConf(_conf)
        print(f'Start Training {conf.model}')
        train, valid, test = preprocess(dataset_name, data_path=Path.cwd().parent / 'datasets' / dataset_name,
                                        create_inverse_triples=conf.create_inverse_triples)
        try:
            result = pipeline(
                training=train,
                validation=valid,
                testing=test,
                model=conf.model,
                # model_kwargs=dict(predict_with_sigmoid=True),
                loss=BCEWithLogitsLoss,
                training_loop='sLCWA',
                training_kwargs=dict(use_tqdm=False),
                # negative_sampler='bernoulli',
                epochs=conf.epochs,
                stopper='early',
                random_seed=conf.seed,
                # device=device,
                device='cpu'
                # result_tracker='wandb',
                # result_tracker_kwargs=dict(project='KGEmbeddings_Family', tags=conf.wandb_tag),
            )
            print(f'Training of {conf.model} on Family done')
            result.save_to_directory(Path(Path.cwd() / 'KGE_results' / dataset_name / conf.model))
            print('Results saved')


            if dataset_name == "family_small" or dataset_name == "family_medium": # Metric is computed only for family_small and family_medium, not on FB
            
                print("---------------")
                # entity_path = "../datasets/" + dataset_name + "/entities.dict"
                # relation_path = "../datasets/" + dataset_name + "/relations.dict"
                test_path = "../datasets/" + dataset_name + "/test.txt"
                sat_path = "../datasets/" + dataset_name + "/train_sat.txt"
                dict_ent = train.entity_to_id
                # with open(entity_path, 'r') as entities_file:
                # for line in train.entity_to_id:
                #     elems = line.strip().split("\t")
                #     dict_ent[int(elems[0])] = int(elems[0])
                dict_rel = train.relation_to_id
                # with open(relation_path, 'r') as relations_file:
                # for line in train.relation_to_id:
                #     elems = line.strip().split("\t")
                #     dict_rel[elems[1]] = int(elems[0])
                # print("relation dictionary  ")
                model = result.model
                tail_batch_list = []
                head_batch_list = []
                with open(test_path, 'r') as test_file:
                    for line in test_file:
                        elems = line.strip().split("\t")
                        first = dict_ent[elems[0]]
                        second = dict_rel[elems[1]]
                        third = dict_ent[elems[2]]
                        tail_batch_list.append([first, second])
                        head_batch_list.append([second, third])
                tail_tensor = torch.tensor(tail_batch_list, dtype=torch.long)
                head_tensor = torch.tensor(head_batch_list, dtype=torch.long)
                print("computing contradicts@1 : ")
                compteur = 0
                head_metric = [0, 0, 0]  # found, not found, contradiction
                tail_metric = [0, 0, 0]
                for i in range(len(tail_tensor) // 16):
                    if 16 * (i + 1) > len(tail_tensor):
                        tail_batch = tail_tensor[16 * i:len(tail_tensor)]
                        head_batch = head_tensor[16 * i:len(head_tensor)]
                    else:
                        tail_batch = tail_tensor[16 * i:16 * (i + 1)]
                        head_batch = head_tensor[16 * i:16 * (i + 1)]
                    tail_score = model.score_t(tail_batch)
                    head_score = model.score_h(head_batch)
                    best_tail_ids = torch.argmax(tail_score, dim=1).tolist()
                    best_head_ids = torch.argmax(head_score, dim=1).tolist()

                    result = "Satisfiability Metric Result\n"

                    c = 0
                    for prediction in best_tail_ids:
                        found_true = False
                        found = False
                        head = tail_batch[c][0]
                        rel = tail_batch[c][1]
                        tail = prediction
                        with open(sat_path, 'r') as sat_file:  # TODO: replace here with the real train_sat
                            for line in sat_file:
                                elems = line.strip().split("\t")
                                if head == dict_ent[elems[0]] and tail == dict_ent[elems[2]]:
                                    found = True
                                    if rel == dict_rel[elems[1]]:
                                        found_true = True
                        if found_true:
                            head_metric[0] += 1
                        elif found:
                            head_metric[2] += 1
                        else:
                            head_metric[1] += 1
                        c += 1
                    result += f"Tail prediction: {head_metric}\n"

                    c = 0
                    for prediction in best_head_ids:
                        found_true = False
                        found = False
                        head = prediction
                        rel = head_batch[c][0]
                        tail = head_batch[c][1]
                        with open(sat_path, 'r') as sat_file:  # TODO: replace here with the real train_sat
                            for line in sat_file:
                                elems = line.strip().split("\t")
                                if head == dict_ent[elems[0]] and tail == dict_ent[elems[2]]:
                                    found = True
                                    if rel == dict_rel[elems[1]]:
                                        found_true = True
                        if found_true:
                            tail_metric[0] += 1
                        elif found:
                            tail_metric[2] += 1
                        else:
                            tail_metric[1] += 1
                        c += 1
                    result += f"Head prediction: {tail_metric}\n"
                both = [h + t for h, t in zip(head_metric, tail_metric)]
                result += f"Both prediction: {both}"
                print(both)
                print("---------------")

                res_path = Path(Path.cwd() / 'KGE_results' / dataset_name / conf.model / "satisfiability_metric.txt")
                with open(res_path, "w") as text_file:
                    text_file.write(result)

        except Exception as error:
            print(f'Model {conf.model} skipped because the following error occured: {error}')
            continue

