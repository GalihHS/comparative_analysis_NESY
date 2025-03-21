import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Put .txt file of KG triples and rules.txt in dlv fact format ",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-f", "--trainfile", default='family_small/train.txt', help="train file to be transformed")
    parser.add_argument("-r", "--rulefile", default='family_small/rule.txt', help="rule file to use")
    args = parser.parse_args()
    print(args)

    # read and transform the fact
    in_triples = open(args.trainfile).readlines()
    print(f'File {args.trainfile} contains {len(in_triples)} triples.')
    fact_list = []

    for line in in_triples:
        head, relation, tail = line.split('\t')
        if tail.endswith('\n'):
            tail = tail[:-1]
        fact_list.append(str(relation) + '(' + str(head) + ',' + str(tail) + ').\n')

    # add facts and rules to the program
    with open('in_dlv', 'w') as f:
        f.writelines(fact_list)
        f.writelines(open(args.rulefile).readlines())
        f.close()

    print(f'Transformed {args.trainfile} triples to input format expected from DLV')


