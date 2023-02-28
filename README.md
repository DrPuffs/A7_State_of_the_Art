# A7_State_of_the_Art

I downloaded a bunch of stock market data from Kaggle. https://www.kaggle.com/datasets/paultimothymooney/stock-market-data <br>
However, I only took 10 random stocks from the NASDAQ portion of csv files to use in the project itself. <br>
I utilized 1 producer that starts out listing the names and starting prices of the 10 stocks that you have the option to monitor. <br>
![Picture 1](Part%201.png)
Next, it will ask you which email address you would like to receive your notifications at: <br>
![Picture 2](Part%202.png)
Finally, the producer starts to read the data from the csv file that pertains to the stock that you chose: <br>
![Picture 3](Part%203.png)
Now, my consumer is supposed to collect the data from the producer and calculate if there has been enough of a price increase that you should think about selling or enough of a price decrease that you should consider buying: <br>
![Picture 4](Part%204.png)
Unfortunately, I could not get the email portion to work: <br>
![Error Picture](ERROR.png)
I think that if I could have had more time, I would have figured it out.
