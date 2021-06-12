// Cruz Lopez
// CIS 3368 
// Final Project
// load the things we need
var express = require('express');
var app = express();
const bodyParser  = require('body-parser');

// required module to make calls to a REST API
const axios = require('axios');
const { promiseImpl } = require('ejs');

app.use(bodyParser.urlencoded());

// set the view engine to ejs
app.set('view engine', 'ejs');

// use res.render to load up an ejs view file

// friends page 
app.get('/', function(req, res) {

    // render to friends.ejs
    res.render('pages/friends', {

    });
});

// adding friends page
app.post('/newFriend', function(req, res){
    // receiving user input names and assigning variables
    var newFirstName = req.body.firstName; 
    var newLastName = req.body.lastName;

    console.log(newFirstName + ' ' + newLastName);

    // calling friend local api url to add first and last name
    axios.post('http://127.0.0.1:5000/friend', {
        firstName: newFirstName,
        lastName: newLastName
    })
    .then(function(response){
        console.log(response.data);
    })

    // render to thanks.ejs
    res.render('pages/thanks.ejs', {body: req.body.firstName + " has been added successfully!"})
});

// movies page
app.get('/movies', function(req, res) {
    // calling api 
    axios.get('http://127.0.0.1:5000/friend/allFriends')
    .then((response) => {
        // assigning data to languages variable
        var friends = response.data;
        console.log(friends)
        // render to movies.ejs
        res.render('pages/movies', {friends: friends});
    });
});

// POST - adding movies to selected user 
app.post('/newMovieList', function(req, res){
    // receiving user input for top ten movies under selected user
    var friendID = req.body.friendID;
    var movie1 = req.body.movie1;
    var movie2 = req.body.movie2;
    var movie3 = req.body.movie3;
    var movie4 = req.body.movie4;
    var movie5 = req.body.movie5;
    var movie6 = req.body.movie6;
    var movie7 = req.body.movie7;
    var movie8 = req.body.movie8;
    var movie9 = req.body.movie9;
    var movie10 = req.body.movie10;

    console.log("Favorite movies added");

    // calling movieList api
    axios.post('http://127.0.0.1:5000/movieList', {
        friendID: friendID,
        movie1: movie1,
        movie2: movie2,
        movie3: movie3,
        movie4: movie4,
        movie5: movie5,
        movie6: movie6,
        movie7: movie7,
        movie8: movie8,
        movie9: movie9,
        movie10: movie10
    })
    .then(function(response){
        console.log(response.data);
    })

    // render to thanks.ejs
    res.render('pages/thanks.ejs', {body: "Movies have been added successfully!"})
});

// decisions page 
app.get('/decisions', function(req, res) {
    axios.get('http://127.0.0.1:5000/friend/allFriends')
    .then((response) => {
        // assigning data to languages variable
        var friends = response.data;
        // render to decision.ejs 
        res.render("pages/decisions", {friends: friends});
    });
});

// FinalDecision POST
app.post('/finalDecision', function(req, res){
    // assigning selected friends to 'friends'
    var friends = Object.keys(req.body)
    // randomize array of friends function
    const randomItem=(arr) => arr[Math.floor(Math.random() * arr.length)];
    // chooses a random friend
    var chosenFriend = randomItem(friends)

    // calls api with friendID parameter
    axios.get('http://127.0.0.1:5000/decision?friendID=' + chosenFriend)
    .then((response) => {
        var data = response.data
        // render to thanks.ejs
        res.render('pages/thanks', {body: data + " is the movie for tonight!"})
    })
  
  })


app.listen(8080);
console.log('8080 is the magic port');
