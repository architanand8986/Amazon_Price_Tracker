# Amazon_Price_Tracker
This is a **flask project** that helps user to keep the history of prices of the products availaible on amazon site in a **sqlite3 database**.It also helps the user to get a **visual clue** about the data with the help of **data visualisation** done with the help of **numpy and matplotlib library in python**<br /><br />

**WORKING IDEA** ::<br/> This app extracts date from the amazon url given from the user and extracts price and other relevant information about the product using web scrapping by **beautiful soup** in python.Then it stores the data in database and show the history of prices to the user in a tabular form. After 3 trackings user can access the advanced analysis for visualising the data from the price trackers<br /><br /><br />

**RUN THE APPLICATION**::<br /> This application and it's database is deployed using docker. So you need to do the follow the following procedures to run the application :->
1. Install and run docker on your system.
2. While the docker is running, go in the projects folder and run the command **docker compose up -d** to run the docker containers of the project in detatched mode.
3. After the process is complete,then goto **localhost:3000** to access the site.
4. If you want to change the ports on which the services are running, then you can change the port mapping in the **docker-compose** file.
5. For checking the services running status write **docker compose ps** and for stopping the application server write **docker compose down** in the command line.
<br/><br /> 
**PROCEDURE TO USE**::<br /> The landing page of the site contains all the relevant procedure to use the app effectively and in correct manner<br /><br /><br />

**Important Points**::<br />
- The app will allow the user to track the price of that product only ones a day.<br /><br />
- This app will show only 7 slots of price history per product.If the all the 7 slots are full and you add a new 
  tracker then it would rewrite on the oldest tracker present in the history.<br /><br />
- If the app shows the error that no data is fetched from the url,then delete that product and add a new product with correct url.The system wouldnot automatically remove the trash trackers.<br /><br />
- To see the advanced analysis(data visualisation), you have to track the product atleast 3 times.The data will then be plotted against mean and median of data set in order to give more clarity to the user.<br /><br />
- Loading of advanced analysis can sometime take time, so please be patient and donot cancel the process in between.<br /><br />

**Hazards**::<br />
- Sometimes Amazon security configurations can stop the scrapping process,if this happens then the user can wait for some time, or use a **VPN** while tracking or change the **headers in scrapper.py** with the **request header attributes** that can be accessed by the **networks tab** in your browser.<br /><br />
- If the user stops the process of loading of advanced analysis, then the main thread would come out of the main loop and the user would have to restart the server

