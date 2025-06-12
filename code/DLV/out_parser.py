
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Put .txt file of KG triples and rules.txt in dlv fact format ",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-o", "--outfile", default='family_small/train_sat.txt', help="Saturated file")
    args = parser.parse_args()
    out_dlv = open('out_dlv').readlines()[2][1:][:-2].split(", ")

    # write again in triple format
    out_facts = []
    with open(args.outfile, 'w') as f:
        for fact in out_dlv:
            str_fact = str(fact).replace('(', ',').replace(')',',').split(',')
            f.writelines(str_fact[1] + '\t' + str_fact[0] + '\t' + str_fact[2] + '\n')
        f.close()
    print(f'Successfully stored file with {len(out_dlv)} facts in {args.outfile}')