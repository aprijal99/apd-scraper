import re, pandas as pd

def main():
  amp = pd.read_csv('apd_amp.csv', dtype={'APD ID': str})

  with open('apd_amp_2.fasta', 'w') as f:
    for idx in amp.index:
      seqName = re.split('\(', amp.loc[idx, 'Name'])[0]
      source = re.split(',', amp.loc[idx, 'Source'])[1].strip() if ',' in amp.loc[idx, 'Source'] else amp.loc[idx, 'Source']

      f.write(f'>{seqName}_{source}\n')
      f.write(amp.loc[idx, 'Sequence'] + '\n')

if __name__ == '__main__':
  main()