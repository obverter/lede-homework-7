# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %% [markdown]
# # Homework 7, Part Two: A dataset about dogs.
#
# Data from [a FOIL request to New York City](https://www.muckrock.com/foi/new-york-city-17/pet-licensing-data-for-new-york-city-23826/)
# %% [markdown]
# ## Do your importing and your setup

# %%
import pandas as pd

# %% [markdown]
# ## Read in the file `NYC_Dog_Licenses_Current_as_of_4-28-2016.xlsx` and look at the first five rows

# %%
df = pd.read_excel('NYC_Dog_Licenses_Current_as_of_4-28-2016.xlsx', nrows=30000, na_values=['Unknown', 'UNKNOWN'])
df.head(5)

# %% [markdown]
# ## How many rows do you have in the data? What are the column types?
#
# If there are more than 30,000 rows in your dataset, go back and only read in the first 30,000.
#
# * *Tip: there's an option with `.read_csv` to only read in a certain number of rows*

# %%
df.info()

# %% [markdown]
# ## Describe the dataset in words. What is each row? List two column titles along with what each of those columns means.
#
# For example: “Each row is an animal in the zoo. `is_reptile` is whether the animal is a reptile or not”
# %% [markdown]
# Owner Zip Code = ZIP of owner's registered address
# Animal Name = Animal's name
# Animal Gender = Animal's sex
# Primary Breed = Animal's primary breed
# Secondary Breed = Animal's secondary breed
# Animal Dominant Color = Main color that a child would tell you the animal is
# Animal Secondary Color = Animal's secondary color
# Animal Third Color = Animal's tertiary color
# Animal Birth = Animal's Birthday
# Spayed or Neut = Whether the animal has been spayed or neutered
# Guard or Trained = Whether the animal can be classified as guard dog or has received training
# Vaccinated = Whether the animal has been vaccinated
# Application Date = Date and time the application was received
# License Issued Date = Date license was issued
# License Expired Date = Date license expires
# %% [markdown]
# # Your thoughts
#
# Think of four questions you could ask this dataset. **Don't ask them**, just write them down in the cell below. Feel free to use either Markdown or Python comments.
# %% [markdown]
# Which ZIPs have the highest/lowest rate of spay/neut?
# What's the average time between the animal's birth and an application for a license, by ZIP?
# Is there a correlation between primary color and a guard dog classification?
# Which breeds are most likely to be named after Game of Thrones characters?
# %% [markdown]
# # Looking at some dogs
# %% [markdown]
# ## What are the most popular (primary) breeds of dogs? Graph the top 10.

# %%
df['Primary Breed'].value_counts().head(10).plot.bar()

# %% [markdown]
# ## "Unknown" is a terrible breed! Graph the top 10 breeds that are NOT Unknown
#
# * *Tip: Maybe you want to go back to your `.read_csv` and use `na_values=`? Maybe not? Up to you!*

# %%
# The Unknown breeds have been launched into the sun at import.

# %% [markdown]
# ## What are the most popular dog names?

# %%
df['Animal Name'].value_counts().head(10)

# %% [markdown]
# ## Do any dogs have your name? How many dogs are named "Max," and how many are named "Maxwell"?

# %%
df[df['Animal Name'] == 'Ben']['Animal Name'].value_counts()


# %%
df[(df['Animal Name'] == 'Maxwell') | (df['Animal Name']== 'Max')]['Animal Name'].value_counts()

# %% [markdown]
# ## What percentage of dogs are guard dogs?

# %%
df['Guard or Trained'].value_counts(normalize=True) * 100

# %% [markdown]
# ## What are the actual numbers?

# %%
df['Guard or Trained'].value_counts()

# %% [markdown]
# ## Wait... if you add that up, is it the same as your number of rows? Where are the other dogs???? How can we find them??????
#
# Use your `.head()` to think about it, then you'll do some magic with `.value_counts()`. Think about missing data!

# %%
df[df['Guard or Trained'].isna()]

# %% [markdown]
# ## Maybe fill in all of those empty "Guard or Trained" columns with "No"? Or as `NaN`?
#
# Can we make an assumption either way? Then check your result with another `.value_counts()`

# %%
df['Guard or Trained'].fillna('No').value_counts()

# %% [markdown]
# ## What are the top dog breeds for guard dogs?

# %%
df[df['Guard or Trained'] == 'Yes']['Primary Breed'].value_counts()

# %% [markdown]
# ## Create a new column called "year" that is the dog's year of birth
#
# The `Animal Birth` column is a datetime, so you can get the year out of it with the code `df['Animal Birth'].apply(lambda birth: birth.year)`.

# %%
df['year'] = df['Animal Birth'].apply(lambda birth: birth.year)
df.head()

# %% [markdown]
# ## Calculate a new column called “age” that shows approximately how old the dog is. How old are dogs on average?

# %%
df['age'] = pd.datetime.now().year - df.year
df.age.mean()

# %% [markdown]
# # Joining data together

# %%


# %% [markdown]
# ## Which neighborhood does each dog live in?
#
# You also have a (terrible) list of NYC neighborhoods in `zipcodes-neighborhoods.csv`. Join these two datasets together, so we know what neighborhood each dog lives in. **Be sure to not read it in as `df`, or else you'll overwrite your dogs dataframe.**

# %%
neighborhoods_df = pd.read_csv('zipcodes-neighborhoods.csv')
df = df.merge(neighborhoods_df, left_on='Owner Zip Code', right_on='zip')
df.head(5)

# %% [markdown]
# ## What is the most popular dog name in all parts of the Bronx? How about Brooklyn? The Upper East Side?
#
# You'll want to do these separately, and filter for each.

# %%
df[df.borough == 'Bronx']['Animal Name'].value_counts().nlargest(1)


# %%
df[df.borough == 'Brooklyn']['Animal Name'].value_counts().nlargest(1)


# %%
df[df.neighborhood == 'Upper East Side']['Animal Name'].value_counts().nlargest(1)

# %% [markdown]
# ## What is the most common dog breed in each of the neighborhoods of NYC?
#
# * *Tip: There are a few ways to do this, and some are awful (see the "top 5 breeds in each borough" question below).*

# %%
df.groupby('neighborhood')['Primary Breed'].value_counts().groupby(level=0).head(1)

# %% [markdown]
# ## What breed of dogs are the least likely to be spayed? Male or female?
#
# * *Tip: This has a handful of interpretations, and some are easier than others. Feel free to skip it if you can't figure it out to your satisfaction.*

# %%
df.groupby('Primary Breed')['Spayed or Neut'].value_counts(normalize=True).sort_values(ascending=False).tail(3) * 100


# %%
df.groupby('Animal Gender')['Spayed or Neut'].value_counts(normalize=True).sort_values(ascending=False) * 100

# %% [markdown]
# ## Make a new column called `monochrome` that is True for any animal that only has black, white or grey as one of its colors. How many animals are monochrome?

# %%
df['Animal Dominant Color'] = df['Animal Dominant Color'].str.upper()
df['Animal Secondary Color'] = df['Animal Secondary Color'].str.upper()
df['Animal Third Color'] = df['Animal Third Color'].str.upper()

monochromes = ['WHITE', 'BLACK', 'GREY']

for dog in df:
    df['monochrome'] = bool(df['Animal Dominant Color'] or df['Animal Secondary Color'] or df['Animal Third Color'].isin(monochromes))

# %% [markdown]
# ## How many dogs are in each borough? Plot it in a graph.

# %%
df.borough.value_counts().plot(kind='bar')

# %% [markdown]
# ## Which borough has the highest number of dogs per-capita?
#
# You’ll need to merge in `population_boro.csv`

# %%
boro_population = pd.read_csv('boro_population.csv')

# count total dogs / borough
dogs_per_borough = df.borough.value_counts().reset_index()
# col names
dogs_per_borough = dogs_per_borough.rename(
    columns={'index': 'borough', 'borough': 'n_dogs'})
# Merge
dogs_per_borough = dogs_per_borough.merge(
    boro_population, left_on='borough', right_on='borough')
# Calculate dogs/borough
dogs_per_borough['dogs_per_capita'] = dogs_per_borough.n_dogs / \
    dogs_per_borough.population

# Sortify
dogs_per_borough.sort_values('dogs_per_capita', ascending=False)

# %% [markdown]
# ## Make a bar graph of the top 5 breeds in each borough.
#
# How do you groupby and then only take the top X number? You **really** should ask me, because it's kind of crazy.

# %%
df.groupby('borough')['Primary Breed'].value_counts().groupby(level=0).head(5).sort_values(ascending=False).plot.barh().invert_yaxis()
# God I hope this is right


# %%
# My eyes hurt
