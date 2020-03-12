import pandas as pd

# Create sample CSV-file (100x100)
#df = pd.DataFrame(np.arange(10000).reshape(100,100))
#df.to_csv('test.csv', index=False)
data = pd.read_csv('listings.csv')
for column in data.columns:
    print(column)
