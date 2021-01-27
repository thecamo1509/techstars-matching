# Welcome to my TechStars Challenge!

Hi! I'm Camilo Andrés Morales, FullStack Developer with entrepreneur spirit. In this challenge I was able to demonstrate my critical thinking, algorithim creation and problem solving skills, in addition I was also able to show some of skills at Frontend development by creating a simple, minimalist and clear dashboard to use the app. 

# Process
The technical challenge solving process is divided in different phases:

 - Identifying and having a deep understanding of the problem
 - Whiteboarding
 - Checking for actual solutions, what is currently out there?
 - Technical analysis of these current solutions and how they work.
 - Whiteboarding
 - Doing paper/pencil testing of the current problem
 - Following the current workflow and finding improvement points
 - Reading the dataset
 - Organizing and filtering the dataset
 - Finding a pattern on the manual process using a piece of code of the dataset
 - Whiteboarding the database models
 - Selecting programming language, frameworks, etc
 - Finding opensource plugins, libraries that could help.
 - Coding the backend
 - Coding the frontend(dashboard and views)
 - Integrating the backend with the frontend
 - Testing
 
 As you can notice the actual coding steps are few compared to what I spent on thinking on possible solutions and checking alternatives to what I currently needing.

## Checking for actual solutions, what is currently out there?
One of the current solution I found was for obvious reasons Google calendar, google calendar offers the possiblity to create events based on the current availability of both parts. However according to techstars current needs Google calendar stills being so manual.


![Gooogle Calendar](https://www.amocrm.com/static/images/pages/integrations/logo/google-calendar.png)

Another solution I found was https://www.scheduleit.com/ One classroom assignment software, I took a look at this project as a reference to identify how could we assign a specific object based on time availability.
![Scheduleit](https://www.scheduleit.com/images/scheduleit19-1200b.png)


## Reading the dataset
Finding a solution isn't that easy if you have a mess with your data. It is like trying to find your keys in your room when is such a mess. It is necessary to have a clean space to work with, cleaning your dataset and structuring as simple and clear as possible. 

This is the original data:

![enter image description here](https://i.imgur.com/Djss41r.png)

It is difficult to read and find a pattern that way right?
Now let's take a look at how I organized it and filtered it:

![enter image description here](https://i.imgur.com/tqaPDa4.png)

You might not see any difference at first but look closer... Yeah I created some simple filters on the google spreedsheet to be able to manipulate and see the data just the way I need. Now I realized that the best way to filter the data was by Mentor's availability days and time blocks. 

## Finding a pattern on the manual process using a piece of code of the dataset

Now that I feel comfortable with the data I'm seeing I am able to look for patterns in it. This part is not as easy as I am telling you, it took me hours and hours trying to identify a pattern that could help me realizing how to create a meeting between the mentor and the startup with no overlays.

So what finally worked for me was creating a little chart where I have a list of specific mentors and their corresponding startups, I also had the timeblocks above to be able to assign appointments.

This is what I did:

![enter image description here](https://i.imgur.com/7W12doS.png)

I started Assigning the startups to the mentors based on their availability and I realized that the condition was simple, actually I needed to conditions to be able to assign an appointment:
	- The Mentor should not have any appointment scheduled at that time
	- The Startup should not have any appointment scheduled at that time
	- The Startup should not have more than one appointment with its mentor on the same timeblock
It sounds obvious right? But let's take a deep look at how I solved it.

![enter image description here](https://i.imgur.com/Prub1vF.png)
So in this example I am assigning appointments to Jackson Carson's startups so I started in order, with Avengers Inc, so as you can see what I did was kind of drawing a Cartesian plane where the Y is the time block I am trying to assign the startup to, and the X is the mentor I am trying to assign to this appointment. As you can see Avengers Inc can NOT be placed on this slot because it is already on the Y (this means it has an appointment with another mentor at that specific time), so what I do is to move to the next startup assigned to this mentor and try that same slot, if that one fits the conditions I mentioned above, I place it. 

![enter image description here](https://i.imgur.com/5wNUdOL.png)

I did this exact exercise and I got it to work! this means I just needed to move that same logic to my code.

## Whiteboarding the database models

Now I am ready to code, the first thing I did was to whiteboard the database models I needed based on the dataset, this is the relation whiteboard:

![enter image description here](https://i.imgur.com/KXbbiVN.png)

Every Mentor can have 1 or more startups assigned and so the startups. This is a many to many relation. Now the appointment relates directly to both objects so thats why they are there as foreign keys.

## Selecting programming language, frameworks, etc

The stack of technologies I selected based on my knowledge, skills and deadlines is:

- BACKEND: Python and Django( Framework)
- DATABASE: sqlite3 (based on sql, faster to integrate)
- Frontend: HTML, CSS, Bootstrap, JS

As you can see I selected base web technologies and focused on the best technology to develop the algorithim to be efficient and effective.

## Finding opensource plugins, libraries that could help.

I used:

- [Full Calendar by Creative Tim](https://www.creative-tim.com/product/full-calendar)
- [Pandas (Data structuring)](https://pandas.pydata.org/)

## Screenshots

### Login and Signup

![enter image description here](https://i.imgur.com/lkZ6dlC.png)

### Home / Calendar

![enter image description here](https://i.imgur.com/kuT6if8.png)

### AutoBooking

![enter image description here](https://i.imgur.com/skDiRRy.png)

### User Profile

![enter image description here](https://i.imgur.com/KypDTNQ.png)

### Startup and Mentor's List

![enter image description here](https://i.imgur.com/8RugL7J.png)

![enter image description here](https://i.imgur.com/PQp2ulq.png)

### Light / Dark Mode

![enter image description here](https://i.imgur.com/kD5ymOX.png)

