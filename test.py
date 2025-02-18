import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 
import seaborn as sns
from sklearn.model_selection import train_test_split
import warnings
warnings.filterwarnings('ignore')

from sklearn.preprocessing import StandardScaler, OneHotEncoder, PowerTransformer
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor

# Load data
data = pd.read_csv("notebook/house_prices.csv")

# Strip column names to ensure no trailing or leading spaces
data.columns = data.columns.str.strip()

# Basic information and initial data cleaning
print(data.info())

# Dropping unnecessary columns
data.drop(columns=['Title', 'Sub_title', 'Description', 'Seller_name', 'Seller_type',
                   'published_date', 'Lat', 'Lon', 'Post_URL', 'Address', 'Location'], axis=1, inplace=True)

# Cleaning functions
def clean_price(data):
    data["Price"] = data['Price'].apply(lambda x: x.split(" ")[-1])
    data['Price'] = data['Price'].str.replace(',', '', regex=True)
    data['Price'] = pd.to_numeric(data['Price'])
    return data

def clean_bath(data):
    data["Baths"] = data['Baths'].apply(lambda x: x.replace('10+', '10'))
    data.dropna(subset=['Baths'], inplace=True)
    data['Baths'] = pd.to_numeric(data['Baths'])
    return data

def clean_bed(data):
    data["Beds"] = data['Beds'].apply(lambda x: x.replace('10+', '10'))
    data.dropna(subset=['Beds'], inplace=True)
    data['Beds'] = pd.to_numeric(data['Beds'])
    return data

def clean_land_size(data):
    def check_land_size(x):
        try:
            return float(x)
        except:
            return None
    data["Land size"] = data['Land size'].str.replace('perches', '', regex=True)
    data['Land size'] = data['Land size'].apply(check_land_size)
    data.dropna(subset=['Land size'], inplace=True)
    data['Land size'] = pd.to_numeric(data['Land size'])
    return data

def clean_house_size(data):
    data['House size'] = data['House size'].apply(lambda x: x.split(" ")[0])
    data["House size"] = data['House size'].str.replace(',', '', regex=True)
    data.dropna(subset=['House size'], inplace=True)
    data['House size'] = pd.to_numeric(data['House size'])
    return data  

def Geo_Address(data):
    location_status = data['Geo_Address'].value_counts()
    location_status_less_5 = location_status[location_status < 5]
    data['Geo_Address'] = data['Geo_Address'].apply(lambda x: 'Other' if x in location_status_less_5 else x)
    data.dropna(subset=['Geo_Address'], inplace=True)
    return data

# Remove outliers using IQR
def remove_outliers_iqr(data, columns, multiplier=1.5):
    if isinstance(columns, str):
        columns = [columns]
    for col in columns:
        Q1 = np.percentile(data[col], 25, method='midpoint')    
        Q3 = np.percentile(data[col], 75, method='midpoint')   
        IQR = Q3 - Q1
        lower_bound = Q1 - (multiplier * IQR) 
        upper_bound = Q3 + (multiplier * IQR)
        data = data[(data[col] > lower_bound) & (data[col] < upper_bound)] 
    return data

# Clean data
print('Before cleaning: ', data.shape)
data = clean_bath(data)
data = clean_bed(data)
data = clean_land_size(data)
data = clean_house_size(data)
data = clean_price(data)
data = Geo_Address(data)  
outlier_columns = ['Price', 'Beds', 'Baths', 'Land size', 'House size']  
data = remove_outliers_iqr(data=data, columns=outlier_columns)
print("After cleaning: ", data.shape)

# Ensure 'Price' column is present
print("Columns after cleaning: ", data.columns)
print(data.info())

# Ensure 'Price' is available
if 'Price' not in data.columns:
    raise ValueError("Column 'Price' not found after cleaning.")

# Specify columns
power = ['Land size', 'Beds', 'House size']
num_columns = ['Price', 'Beds', 'Baths', 'Land size', 'House size']
cat_columns = ['Geo_Address']

# ColumnTransformer for preprocessing
preprocess = ColumnTransformer([
    ('power_pipeline', PowerTransformer(method='yeo-johnson'), power),
    ('num_pipeline', StandardScaler(), num_columns),
    ('cat_pipeline', OneHotEncoder(), cat_columns) 
])

# Check data
print(data.head())
# Convert 'Price' and other numeric columns to numeric types
data['Price'] = pd.to_numeric(data['Price'], errors='coerce')
data['Land size'] = pd.to_numeric(data['Land size'], errors='coerce')
data['House size'] = pd.to_numeric(data['House size'], errors='coerce')
data['Beds'] = pd.to_numeric(data['Beds'], errors='coerce')
data['Baths'] = pd.to_numeric(data['Baths'], errors='coerce')
data = data.dropna()

X = data.drop(columns=['Price'], axis=1)
y = data['Price']
# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

X_train = preprocess.fit_transform(X_train)
X_test = preprocess.transform(X_test)

# Combine input features with target labels
train_arr = np.c_[X_train, np.array(y_train)]
test_arr = np.c_[X_test, np.array(y_test)]
print(train_arr.shape)
print(test_arr.shape)

rf = RandomForestRegressor()
rf.fit(X_train, y_train)
print(rf.score(X_train, y_train))

#train_data, test_data = train_test_split(data, test_size=0.2, random_state=42)
#print(train_data.columns)
#print(test_data.columns)

# Splitting features and target for train and test
#input_feature_train_data = train_data.drop(columns=['Price'], axis=1)
#target_feature_train_data = train_data['Price']

#input_feature_test_data = test_data.drop(columns=['Price'], axis=1)
#target_feature_test_data = test_data['Price']


# Preprocess input features
#input_train_arr = preprocess.fit_transform(input_feature_train_data)
#input_test_arr = preprocess.transform(input_feature_test_data)

# Combine input features with target labels
#train_arr = np.c_[input_train_arr, np.array(target_feature_train_data)]
#test_arr = np.c_[input_test_arr, np.array(target_feature_test_data)]

# Save processed data to files
#np.save('train.npy', train_arr)
#np.save('test.npy', test_arr)

# Load data back
#train = np.load('train.npy')
#test = np.load('test.npy')

# Split back into inputs and targets
#input_train = train[:, :-1]
#target_train = train[:, -1]

# Train RandomForest model
#rf = RandomForestRegressor()
#rf.fit(input_train, target_train)

# Evaluate model
#print(f'Model R^2 score: {rf.score(input_train, target_train)}')

# Optional: Predict on the test set
#input_test = test[:, :-1]
#target_test = test[:, -1]
#predictions = rf.predict(input_test)
