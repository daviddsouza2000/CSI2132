import pandas as pd

# Create sample CSV-file (100x100)
#df = pd.DataFrame(np.arange(10000).reshape(100,100))
#df.to_csv('test.csv', index=False)
data = pd.read_csv('listings.csv')
#for column in data.columns:
#    print(column)

l = [x for x in range(100,len(data.index))]
print(l[100])
print(data.shape)
data = data.drop(l)
print(data.shape)
print(data.head())
print(data.tail())
    
data.to_csv('toronto_listings.csv')
