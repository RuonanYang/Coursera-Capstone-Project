#!/usr/bin/env python
# coding: utf-8

# ## Web scraping with BS4

# ### Install the beautifulsoup4

# In[ ]:


get_ipython().system('pip install beautifulsoup4')


# In[12]:


from bs4 import BeautifulSoup


# ### Use the URL to extract the html data

# In[14]:


import requests
r = requests.get("https://en.wikipedia.org/wiki/List_of_postal_codes_of_Canada:_M")
data = r.text
soup = BeautifulSoup(data)
soup.prettify()


# ### Find the desired table

# In[49]:


My_table = soup.find('table',{'class':"wikitable sortable"})


# ### Use the function parse_html_table to parse the table

# In[26]:


def parse_html_table(table):
        n_columns = 0
        n_rows=0
        column_names = []

        # Find number of rows and columns
        # we also find the column titles if we can
        for row in table.find_all('tr'):

            # Determine the number of rows in the table
            td_tags = row.find_all('td')
            if len(td_tags) > 0:
                n_rows+=1
                if n_columns == 0:
                    # Set the number of columns for our table
                    n_columns = len(td_tags)

            # Handle column names if we find them
            th_tags = row.find_all('th') 
            if len(th_tags) > 0 and len(column_names) == 0:
                for th in th_tags:
                    column_names.append(th.get_text())

        # Safeguard on Column Titles
        if len(column_names) > 0 and len(column_names) != n_columns:
            raise Exception("Column titles do not match the number of columns")

        columns = column_names if len(column_names) > 0 else range(0,n_columns)
        df = pd.DataFrame(columns = columns,
                          index= range(0,n_rows))
        row_marker = 0
        for row in table.find_all('tr'):
            column_marker = 0
            columns = row.find_all('td')
            for column in columns:
                df.iat[row_marker,column_marker] = column.get_text()
                column_marker += 1
            if len(columns) > 0:
                row_marker += 1

        # Convert to float if possible
        for col in df:
            try:
                df[col] = df[col].astype(float)
            except ValueError:
                pass

        return df


# In[38]:


import pandas as pd
df = parse_html_table(My_table)


# In[39]:


df.columns = ['Postcode', 'Borough', 'Neighbourhood']


# In[40]:


df['Neighbourhood'] = df['Neighbourhood'].map(lambda x: x.rstrip('\n'))


# In[43]:


df = df[~df['Borough'].isin(['Not assigned'])]


# In[45]:


# Ignore cells with a borough that is not assigned. If a cell has a borough but a not assigned neighbourhood, 
# then the neighbourhood is the same as the borough
df = df[~df['Borough'].isin(['Not assigned'])]
df.loc[df.Neighbourhood=='Not assigned','Neighbourhood']=df.loc[df.Neighbourhood=='Not assigned','Borough']


# In[48]:


print('The number of rows of the table is '+ str(df.shape[0]))


# In[ ]:




