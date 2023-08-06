
# Neat Panda

[![pypi](https://img.shields.io/pypi/v/neat_panda.svg)](https://pypi.python.org/pypi/neat_panda)

[![Build Status](https://dev.azure.com/henricsundberg/neat_panda/_apis/build/status/htp84.neat_panda?branchName=master)](https://dev.azure.com/henricsundberg/neat_panda/_build/latest?definitionId=1&branchName=master)
[![](https://img.shields.io/azure-devops/build/henricsundberg/neat_panda/1/master.svg)]()

[![](https://img.shields.io/azure-devops/coverage/henricsundberg/neat_panda/1/master.svg)]()
[![](https://img.shields.io/azure-devops/tests/henricsundberg/neat_panda/1/master.svg?passed_label=good&failed_label=bad&skipped_label=n%2Fa</code>)]()

[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/htp84/neat_panda.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/htp84/neat_panda/context:python)
[![Total alerts](https://img.shields.io/lgtm/alerts/g/htp84/neat_panda.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/htp84/neat_panda/alerts/)


Neat Panda contains three main methods/functions, spread, gather and clean_columnames. The ideas for these methods are from the spread and gather functions in the R package [*tidyr*](https://tidyr.tidyverse.org/) and the make_clean_columns function in the R package [*janitor*](https://github.com/sfirke/janitor). 

The spread function is syntactic sugar for the [*pandas*](https://pandas.pydata.org/pandas-docs/stable/) library method [*pivot*](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.pivot.html) and the gather method is syntactic sugar for the pandas method [*melt*](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.melt.html).


## Features
### clean_column_names
```python
from neat_panda import clean_column_names

print(df.columns.tolist())
["Country    ", "Sub$region", "Actual"]

df = df.clean_column_names()
# or
df.columns = clean_column_names(df.columns)
# or
df = clean_column_names(df)
# or
df = df.pipe(clean_columnnames)

print(df.columns.tolist())
["country", "sub_region", "actual"]

```

### spread
#### R
```R
library(tidyr)
library(dplyr)
library(gapminder)

gapminder2 <- gapminder %>% select(country, continent, year, pop)
gapminder3 <- gapminder2 %>% spread(key = year, value = pop)
head(gapminder3, n = 5)
```
#### Python
```python
from neat_panda import spread
from gapminder import gapminder

gapminder2 = gapminder[["country", "continent", "year", "pop"]]
gapminder3 = gapminder2.spread(key="year", value="pop")
# or
gapminder3 = spread(df=gapminder2, key="year", value="pop")
# or
gapminder3 = gapminder2.pipe(spread, key="year", value="pop")

gapminder3.head()
```
##### Output R
```
# A tibble: 5 x 14
  country     continent   `1952`   `1957`   `1962`   `1967`   `1972`   `1977`   `1982`   `1987`   `1992`   `1997`   `2002`   `2007`
  <fct>       <fct>        <int>    <int>    <int>    <int>    <int>    <int>    <int>    <int>    <int>    <int>    <int>    <int>
1 Afghanistan Asia       8425333  9240934 10267083 11537966 13079460 14880372 12881816 13867957 16317921 22227415 25268405 31889923
2 Albania     Europe     1282697  1476505  1728137  1984060  2263554  2509048  2780097  3075321  3326498  3428038  3508512  3600523
3 Algeria     Africa     9279525 10270856 11000948 12760499 14760787 17152804 20033753 23254956 26298373 29072015 31287142 33333216
4 Angola      Africa     4232095  4561361  4826015  5247469  5894858  6162675  7016384  7874230  8735988  9875024 10866106 12420476
5 Argentina   Americas  17876956 19610538 21283783 22934225 24779799 26983828 29341374 31620918 33958947 36203463 38331121 40301927
```
##### Output Python
```
       country continent      1952      1957      1962      1967      1972      1977      1982      1987      1992      1997      2002      2007
0  Afghanistan      Asia   8425333   9240934  10267083  11537966  13079460  14880372  12881816  13867957  16317921  22227415  25268405  31889923
1      Albania    Europe   1282697   1476505   1728137   1984060   2263554   2509048   2780097   3075321   3326498   3428038   3508512   3600523
2      Algeria    Africa   9279525  10270856  11000948  12760499  14760787  17152804  20033753  23254956  26298373  29072015  31287142  33333216
3       Angola    Africa   4232095   4561361   4826015   5247469   5894858   6162675   7016384   7874230   8735988   9875024  10866106  12420476
4    Argentina  Americas  17876956  19610538  21283783  22934225  24779799  26983828  29341374  31620918  33958947  36203463  38331121  40301927
```


### gather
#### R
```R
library(tidyr)
# gapminder3 is obtained as above
gapminder4 <- gather(gapminder3, key="year", "value"="pop", 3:14)
# or
years <- c("1952", "1957", "1962", "1967", "1972", "1977", "1982", "1987", "1992", "1997", "2002", "2007")
gapminder4 <- gather(gapminder3, key="year", "value"="pop", years)

head(gapminder4, n = 5)
```
#### Python
```python
from neat_panda import gather
# gapminder3 is obtained as above
gapminder4 = gather(gapminder3, key="year", value="pop", columns=range(2, 13))
# or
gapminder4 = gather(gapminder3, key="year", value="pop", columns=range(0, 2), invert_columns=True)
# or
years = ["1952", "1957", "1962", "1967", "1972", "1977", "1982", "1987", "1992", "1997", "2002", "2007"]
gapminder4 = gather(gapminder3, key="year", value="pop", columns=years)
# or
gapminder4 = gather(gapminder3, key="year", value="pop", columns=["country", "continent"], invert_columns=True)

gapminder4.head()
```
##### Output R
```
# A tibble: 5 x 4
  country     continent year       pop
  <fct>       <fct>     <chr>    <int>
1 Afghanistan Asia      1952   8425333
2 Albania     Europe    1952   1282697
3 Algeria     Africa    1952   9279525
4 Angola      Africa    1952   4232095
5 Argentina   Americas  1952  17876956
```
##### Output Python
```
       country continent  year       pop
0  Afghanistan      Asia  1952   8425333
1      Albania    Europe  1952   1282697
2      Algeria    Africa  1952   9279525
3       Angola    Africa  1952   4232095
4    Argentina  Americas  1952  17876956

```





