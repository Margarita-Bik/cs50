-- Keep a log of any SQL queries you execute as you solve the mystery.

--Checking what happened in the crime scene that day and time
SELECT description FROM crime_scene_reports WHERE month = 7 AND day = 28 AND street = "Chamberlin Street";

--Checking what did witnesses said at the interviews
SELECT transcript FROM interviews WHERE month = 7 AND day = 28 AND year = 2020;

--Checking in 1st witness's story, the car where the thief got in
SELECT activity, license_plate, minute FROM courthouse_security_logs WHERE year = 2020 AND month = 7 AND day = 28 AND hour = 10 AND minute > 15 AND minute <25;

--Finding the names of people who own the cars that left within 10 minutes from theft
SELECT name FROM people WHERE license_plate = "5P2BI95" OR license_plate = "94KL13X" OR license_plate = "6P58WS2" OR license_plate = "4328GD8" OR license_plate = "G412CB7" OR license_plate =  "L93JTIZ" OR license_plate = "322W7JE" OR license_plate = "0NTHK55";

--Checking in 2nd witness's story, the names of people who whithdrawed money that day in that atm
SELECT name FROM people JOIN bank_accounts ON people.id = bank_accounts.person_id WHERE account_number IN (SELECT account_number FROM atm_transactions WHERE year = 2020 AND month = 7 AND day = 28 AND atm_location = "Fifer Street" AND transaction_type = "withdraw");

--Right now, we are down to 5 suspects: Elizabeth,Danielle, Russell and Ernest

--Checking in 3rd witness's story, the people who talked for less than a minute on the phone, that day and time
SELECT name FROM people WHERE phone_number IN (SELECT caller FROM phone_calls WHERE year = 2020 AND month = 7 AND day = 28 AND duration < 60);
SELECT name FROM people WHERE phone_number IN (SELECT receiver FROM phone_calls WHERE year = 2020 AND month = 7 AND day = 28 AND duration < 60);

--At this time, we have narrowed it down to Russell and Ernest and the suspected accomplices Melissa and Berthold respectively

--Checking which is the first flight away, and where does it go
SELECT city FROM airports JOIN flights ON airports.id = flights.destination_airport_id WHERE origin_airport_id IN (SELECT id FROM airports WHERE city = "Fiftyville") AND year = 2020 AND month = 7 AND day = 29 ORDER BY hour, minute LIMIT 1;

--We now know he/she went to London

--Finding flight id
SELECT id FROM flights WHERE origin_airport_id IN (SELECT id FROM airports WHERE city = "Fiftyville") AND destination_airport_id IN (SELECT id FROM airports WHERE city = "London") AND year = 2020 AND month = 7 AND day = 29 ORDER BY hour, minute LIMIT 1;

--Checking which one of the suspects went to London on this flight
SELECT name FROM people WHERE passport_number IN (SELECT passport_number FROM passengers WHERE flight_id = 36);

--So, the thief is Ernest and the accomplice is Berthold









