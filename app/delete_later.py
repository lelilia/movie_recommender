import pickle
import os.path
from sklearn.decomposition import NMF
import pandas as pd

file_name = 'teste_ob_das_geht.pkl'

data = [
    [5, 4, 1, 1, 3],
    [3, 2, 1, 3, 1],
    [3, 3, 3, 3, 5],
    [1, 1, 5, 4, 4],
]
columns = ['Titanic', 'Tiffany', 'Terminator', 'Star Trek', 'Star Wars'] #movies
index = ['Ada', 'Bob', 'Steve', 'Margaret'] #users

#need a dataframe for this
R = pd.DataFrame(data, index=index, columns=columns).values

#create a model and set the hyperparameters
# model assumes R ~ PQ'
model = NMF(n_components=2, init='random', random_state=10)

model.fit(R)


if os.path.exists(file_name):
    print('I get the file')
else:
    print('no file found')
    with open(file_name, 'wb') as file:
        pickle.dump(model, file)