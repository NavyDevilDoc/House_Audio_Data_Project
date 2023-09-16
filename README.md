# House_Audio_Data_Project
After collecting two weeks of data using what's in my "House Environmental Data" repository, I wanted to push things further. This time, I'm using an Arduino Nano 33 BLE to characterize the background noise in my house. 

The first iteration, now that it's up and running, takes background noise at 16 KHz and downsamples the incoming data to 1 KHz to be a little more manageable for my poor computer. I save five minutes of data to a CSV file. To account for negative sensor values, I find the root mean square voltage and use it to convert the Analog-to-Digital data at the sensor to decibels. As of this writing, I am in the process of collecting 48 hours of data. I collected just over two hours of data earlier and am working on putting the data together into a data frame for processing. 

Just as I did in the house environmental data repository, I will add logging and a scheduler for data analysis. My wife joked that I keep getting more and more froggy, so who knows what I'll come up with next!
