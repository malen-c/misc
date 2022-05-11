import re
import pandas as pd

df = pd.read_csv('data/NASA astronauts - US ASTRONAUTS.csv')

#converting to string so I don't have to import datetime then using regex to grab year before every newline. bad solution sorry
years = [x for x in re.findall('([0-9]{4})\n', df['Date of birth'].to_string())]
years.append('1965')
names = [x.replace(',', '') for x in df['Astronaut ']]

with open('data/astros.csv', 'r+') as fob:
    fob.write('name,year\n')
    for i in range(df.shape[0]):
        fob.write(names[i] + ',' + years[i] + '\n')
