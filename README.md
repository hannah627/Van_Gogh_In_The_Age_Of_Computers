# Van Gogh In The Age Of Computers

Van Gogh in the Age of Computers is a project that seeks to explore Van Gogh's
works digitally using the Colors of Van Gogh dataset made by Kaggle user
Konstantinos and found at https://www.kaggle.com/pointblanc/colors-of-van-gogh.
Our aim is to explore trends and patterns in his work to both better understand
his works and his career, as well as to help the archival and restoration
process of paintings by creating an interpretable machine learning model.
This will predict the most important identifying information about a painting,
which could make the process more efficient overall.

### To reproduce our results:

To reproduce our results, run the main.py file in the terminal.

Many of our questions involve graphs, which should open automatically, but can
also be found in the graphs file, where q1-1.html is the first graph for
question 1, q1-2.html is the second graph for question 1, etc.

### Packages:

All necessary packages (pandas, bokeh, requests, and sklearn) should already be
installed. If for some reason they're not, please be sure to install them with
your method of choice before running.

### Other things to note

- The third question involves training a machine learning model, which may take a
while to run. As with most models, the prediction accuracy of the model on the
test set also varies.
- The last part of our project involves querying an API that has a capped number
of allowed requests per second, so running that part may take a while.
