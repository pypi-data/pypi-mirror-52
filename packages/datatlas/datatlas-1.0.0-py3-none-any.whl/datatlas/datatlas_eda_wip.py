
"""
[TITLE]
Author: Mei Yong
Updated Date: Sat Sep 21 15:28:52 2019

"""



import pandas as pd
df = pd.read_csv(r"C:\Users\shaom\Desktop\Machine_Learning\projects\data\titanic.csv")


def get_dtype_profile(df):
    
    import re
    
    dtype_regex_dict = {}
    
    for column in df:
        
        col = df[column]
        
        # Data prep for regex
        col.dropna(inplace=True) # Drop nulls
        col = col.astype(str).str.lower() # Lowercase
        col = col.str.replace(' ','') # Remove whitespace
        col = col.apply(lambda x: re.sub(r'[^\w\s]', '', x)) # Remove punctuation
        
        numeric_count, string_count, mixed_count = 0, 0, 0
        
        for item in col:
            
            item_len = len(item)
            
            # Find the number of alphabets in the string
            alphabet_find = re.findall(r"[a-zA-Z]+", item)
            try:
                alphabet_len = len(alphabet_find[0])
            except:
                alphabet_len = 0
            
            # Find the number of numbers in the string
            number_find = re.findall(r"[0-9]+", item)
            try:
                number_len = len(number_find[0])
            except:
                number_len = 0
            
            # Note the number of strings that are fully alphabets, fully numbers, or mixed
            if item_len == number_len:
                numeric_count += 1
            elif item_len == alphabet_len:
                string_count += 1
            else:
                mixed_count += 1
        
        
        dtype_regex_result = {'numeric': round(numeric_count/len(col) *100, 2)
                            ,'non-numeric': round(string_count/len(col) *100, 2)
                            ,'mixed': round(mixed_count/len(col) *100, 2)   
                            }
            
        dtype_regex_dict[column] = dtype_regex_result

    return dtype_regex_dict


dtype_profile = get_dtype_profile(df)




import re
    
    dtype_regex_dict = {}
    
for column in df:
    
    col = df[column]
    
    # Data prep for regex
    col = col.astype(str).str.lower() # Lowercase
    col = col.str.replace(' ','') # Remove whitespace
    col = col.apply(lambda x: re.sub(r'[^\w\s]', '', x)) # Remove punctuation
    
    
    item = 'gooblygoop'
    
    test = re.search(r"^[y](es)?", item)
    test.group(0)





### If column is a date column, convert it to datetime format
for column in sfPermitsClean:
    if 'date' in column:
        sfPermitsClean[column] = pd.to_datetime(sfPermitsClean[column], errors='coerce')
        
        ### Formatting datetime
import datetime
ex_date_1 = "01-03-2019"
ex_date_2 = datetime.datetime.strptime(ex_date_1, "%d-%m-%Y")





        
        ### Count up the labels and group
        
        ### If more than 1 group, output 'Warning: Mixed types {'string':10%, 'numeric':90%}
        
        ### Note the most commonly occuring label
        
        ### If most values look like numerics BUT the auto-detected type is string, then warning should be numeric
        
        ### If most values look like strings BUT the auto-detected type is numeric, then warning should be string (this will likely never be triggered)
        
        
        
        
        
        
                
        ### ID check
        ### Check for sequential score
        ### Check for repeated value score - mask then group then average where zero is means more repeated values and one means less repeated values and closer to zero is more likely to be an ID
        ### Check for Benford's law - basically if the values start with the same number or set of numbers
            
        ### y/n check
        ### Convert to string (keep the NaNs)
        ### Check for common y/n values
            
        ### Date check
        ### Remove NaNs
        ### Convert to string
        ### Check regex and label
        ### Count up the labels
        ### If >60% date then date warning


        