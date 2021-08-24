### Taipei-day-trip

 [Click me to the online website](http://18.217.38.82:3000/)  

**Information for test ↓** (or sign up on your own)<br>
[ member ]<br />
account: test@mail.com<br />
password: test<br />
[ credit card ]<br />
card number：4242 4242 4242 4242<br />
expiration date：01/23<br />
CVV：123<br />

**Techniques used**<br />
[ Backend end ]<br />
API for member account functions, sites information fetching, itinerary booking, payment：follow the style of RESTfulAPI<br />
Server：Flask<br />
Deploys the website online：EC2 instance ( Red Hat Enterprise Linux 8 ) <br />
Database：MySQL<br />
Third-party payment：Connects TapPay API payment system to pay for the booked itinerary<br />
Confidential information management：set up environmental variables with python-dotenv kit<br />

[ Front end ]<br />
User interface：RWD、Infinite Scroll<br />
Front page, booking page fetching sites information：AJAX<br />
booking page sites carousel：JavaScript

［Database Structure］（member、booking、sites information）<br />
![](https://github.com/Jhih-cell/taipei-day-trip-website/blob/main/dbstr.png)
