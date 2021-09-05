### Taipei-day-trip

 Online website deployed on EC2 → [http://18.217.38.82/](http://18.217.38.82/)  

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
Reverse proxy：NGINX<br />
Database：MySQL<br />
Third-party payment：Connects TapPay API payment system to pay for the booked itinerary<br />
Confidential information management：set up environmental variables with python-dotenv kit<br />

[ Front end ]<br />
User interface：RWD、Infinite Scroll<br />
Front page, booking page fetching sites information：AJAX<br />
booking page sites carousel：JavaScript


