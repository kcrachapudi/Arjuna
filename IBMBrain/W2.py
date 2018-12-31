
#For one reason or another, it may be useful to keep that observation even if some features are missing. Now, let's go into how to drop missing values or replace missing values in Python. 
#To remove data that contains missing values Panda's library has a built-in method called dropna. 
#Essentially, with the dropna method, you can choose to drop rows or columns that contain missing values like NaN. 
#So you'll need to specify access equal zero to drop the rows or access equals one to drop the columns that contain the missing values. 
#In this example, there is a missing value in the price column. Since the price of used cars is what we're trying to predict in our upcoming analysis, we have to remove the cars,
#the rows, that don't have a listed price. It can simply be done in one line of code using dataframe.dropna. Setting the argument in place to true, allows the modification to be
#done on the data set directly. In place equals true, just writes the result back into the data frame. This is equivalent to this line of code. 
#Don't forget that this line of code does not change the data frame but is a good way to make sure that you are performing the correct operation. 
#To modify the data frame, you have to set the parameter in place equal to true. You should always check the documentation if you are not familiar with the function or method. 
#The pandas web page has lots of useful resources. To replace missing values like NaNs with actual values, Pandas library has a built-in method called replace
#which can be used to fill in the missing values with the newly calculated values. 
#As an example, assume that we want to replace the missing values of the variable normalized losses by the mean value of the variable.
#Therefore, the missing value should be replaced by the average of the entries within that column. In Python, first we calculate the mean of the column. 
#Then we use the method replace to specify the value we would like to be replaced as the first parameter, in this case NaN. 
#The second parameter is the value we would like to replace it with i.e the mean in this example. This is a fairly simplified way of replacing missing values. 
#There are of course other techniques such as replacing missing values for the average of the group instead of the entire data set. 
#So, we've gone through two ways in Python to deal with missing data. We learnt to drop problematic rows or columns containing missing values 
#and then we learnt how to replace missing values with other values. But don't forget the other ways to deal with missing data. 
#You can always check for a higher quality data set or source or in some cases you may want to leave the missing data as missing data.

