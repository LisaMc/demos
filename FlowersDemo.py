
# coding: utf-8

# In[1]:


import numpy as np
import bokeh
from bokeh.plotting import figure, show, output_file, output_notebook
from bokeh.charts import Histogram
from bokeh.sampledata.iris import flowers

output_notebook()


# The flowers dataset is a dataframe with observational values for a number of samples. 
# In Python, operations can be called directly on an object by the dot notation.
# View just the top 5 rows by calling the "head" function on the flowers dataframe.

# In[2]:


flowers.head(5)


# In[3]:


display(flowers.tail(3))


# Notice that the indexing starts at 0, so the values will range from 0-149.  You can view any range of rows within the dataframe by specifying the start, length, and increment parameters.  The following starts at the 3rd position, will display up to, but not including the 10th row, skipping every second record.

# In[4]:


flowers[3:10:2]


# In[5]:


flowers.sort_values(by='sepal_length').head()


# In[6]:


flowers[flowers.sepal_length < 5]


# In[7]:


flowers.describe()


# In[8]:


display(flowers["species"].unique())
display(flowers.species.value_counts())


# In[9]:


hist = Histogram(flowers,values='petal_length')
show(hist)


# In[10]:


hist2 = Histogram(flowers,values='petal_length', label="species", color="species")
show(hist2)


# In[11]:


colormap = {'setosa': 'red', 'versicolor': 'green', 'virginica': 'blue'}
colors = [colormap[x] for x in flowers['species']]
p = figure(title = "Iris Morphology")
p.xaxis.axis_label = 'Petal Length'
p.yaxis.axis_label = 'Petal Width'

p.circle(flowers["petal_length"], flowers["petal_width"],
         color=colors, fill_alpha=0.2, size=10)

show(p)


# Unfortunately, adding a legend is not straightforward using this method (that I know of), since the colors are not directly attached to the data.  It's best to not alter the original data, so we will create a temporary copy of the data frame and add a column called "colors" as defined by the color map.  The "for" loop will then iterate over each of the species varieties, pull the rows that match that variety, then define the circle location based on the petal length (x-axis) and width (y-axis), with the according color and legend label.

# In[12]:


colormap = {'setosa': 'red', 'versicolor': 'green', 'virginica': 'blue'}
temp = flowers
temp['colors'] = [colormap[x] for x in temp['species']]
temp = temp.set_index("species")
display(temp.index)
p = figure(title = "Iris Morphology")
p.xaxis.axis_label = 'Petal Length'
p.yaxis.axis_label = 'Petal Width'

for variety in temp.index.unique():
    p.circle(temp.loc[variety,'petal_length'], temp.loc[variety,"petal_width"],
         color=temp.loc[variety,"colors"], fill_alpha=0.2, size=10, legend=variety)

p.legend.location = "top_left"
show(p)


# Here is just another example of how to add a legend using a column data source method with different data.

# In[13]:


from bokeh.models import ColumnDataSource, CategoricalColorMapper
from bokeh.palettes import RdBu3

source = ColumnDataSource(dict(
    x=[1, 2, 3, 4, 5, 6],
    y=[2, 1, 2, 1, 2, 1],
    label=['hi', 'lo', 'hi', 'lo', 'hi', 'lo']
))
color_mapper = CategoricalColorMapper(factors=['hi', 'lo'], palette=[RdBu3[2], RdBu3[0]])

p = figure(x_range=(0, 7), y_range=(0, 3), height=300, tools='save')
p.circle(
    x='x', y='y', radius=0.5, source=source,
    color={'field': 'label', 'transform': color_mapper},
    legend='label'
)
show(p)


# And another way to iteratively add lines to a plot and define different legend attributes

# In[14]:


x = np.linspace(0.1, 5, 100)

p = figure(title="log axis example", y_axis_type="log",
           y_range=(0.001, 10**22))

p.line(x, np.sqrt(x), legend="y=sqrt(x)",
       line_color="tomato", line_dash="dotdash")

p.line(x, x, legend="y=x")
p.circle(x, x, legend="y=x")

p.line(x, x**2, legend="y=x**2")
p.circle(x, x**2, legend="y=x**2",
         fill_color=None, line_color="olivedrab")

p.line(x, 10**x, legend="y=10^x",
       line_color="gold", line_width=2)

p.line(x, x**x, legend="y=x^x",
       line_dash="dotted", line_color="indigo", line_width=2)

p.line(x, 10**(x**2), legend="y=10^(x^2)",
       line_color="coral", line_dash="dashed", line_width=2)

p.legend.location = "top_left"

output_file("logplot.html", title="log plot example")

show(p)  # open a browser


# In[ ]:




