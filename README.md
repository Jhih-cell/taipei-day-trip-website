## Taipei-day-trip

 Online website deployed on EC2 → [https://travel.readitlater.live/](https://travel.readitlater.live/)  

### Information for test ↓ (or sign up on your own)<br>
[ member ]<br />
account: test@mail.com<br />
password: test<br />
[ credit card ]<br />(please choose from down below)
|card number        |expiration date|CVV |
|-------------------|---------------|----|
|4242 4242 4242 4242|01/23          |123 |
|3543 9234 8838 2426|01/23          |123 |
|3454 5465 4604 563 |01/23          |1234|
|5451 4178 2523 0575|01/23          |123 |
|6234 5774 3859 4899|01/23          |123 |

### Feature demo<br />
**Frontpage**<br />
1. Infinite scrolling<br />
2. Searching attractions with keyword<br />
<img width="948" alt="index" src="https://user-images.githubusercontent.com/58781081/132538422-f40bb329-694e-42d4-83d5-b451ea6f6605.PNG"><br />

**Membership system page**<br />
Register, login, logout<br />
<img width="948" alt="member" src="https://user-images.githubusercontent.com/58781081/132539185-666d5028-ecdb-4999-a212-7692fb3c012e.PNG"><br />

**Attraction details page**<br />
Attraction information with sites carousel and booking function<br />
<img width="947" alt="attraction" src="https://user-images.githubusercontent.com/58781081/132539435-9551c3ea-f445-407e-95c2-5447ad2393de.PNG"><br />

**Booking and payment page**<br />
Users can fill in contact and credit card information, also can delete itinerary here.<br />
<img width="950" alt="booking_1" src="https://user-images.githubusercontent.com/58781081/132541912-b0b02dc0-7ef2-42d2-96cb-2bc0bf652292.PNG">
<img width="947" alt="booking_2" src="https://user-images.githubusercontent.com/58781081/132539715-c04a296f-65cf-47c2-9114-deb488956859.PNG">





### Techniques used<br />
[ Backend end ]<br />
API for member account functions, sites information fetching, itinerary booking, payment：follow the style of RESTfulAPI<br />
Server：Flask<br />
Deploys the website online：EC2 instance ( Red Hat Enterprise Linux 8 ) <br />
Reverse proxy：NGINX<br />
Add SSL certificate to the website：Cloudflare<br />
Database：MySQL<br />
Third-party payment：Connects TapPay API payment system to pay for the booked itinerary<br />
Confidential information management：set up environmental variables with python-dotenv kit<br />

[ Front end ]<br />
User interface：RWD、Infinite Scroll<br />
Front page, booking page fetching sites information：AJAX<br />
booking page sites carousel：JavaScript<br />

### System architecture<br />
<img width="714" alt="systemStructure" src="https://user-images.githubusercontent.com/58781081/132129096-2c84471c-b06d-4e57-bf8e-094aee92f1ed.png">



