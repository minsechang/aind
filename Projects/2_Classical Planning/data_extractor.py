import re

def main():
    input_txt = '/Users/minse_chang/Downloads/result_second_2.txt'
    with open(input_txt, 'r') as ff:
        for line in ff:
            if 'Solving ' in line:
                prob, heur = re.search('Solving\s(.*)\susing\s(.*)...', line).groups()
                # print(line)
                continue
            try:
                actions, expansions, goalTests, newnodes = re.search("\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+", line).groups()
                # print(line)
                continue
            except:
                pass
            try:
                length, time = re.search("Plan\slength\:\s?(\d+)\s+Time\selapsed\sin\sseconds\:\s?([0-9]*\.[0-9]+)?", line).groups()
                print(','.join([prob, heur, actions, expansions, goalTests, newnodes, length, time]))
                continue
            except:
                pass


if __name__ == '__main__':
    main()
