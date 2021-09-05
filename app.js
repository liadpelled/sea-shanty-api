require('dotenv').config();
const { text } = require("body-parser");
const { json } = require('express');
const express = require("express");
const mongoose = require("mongoose");

const app = express();
app.use(express.static('public'));
app.use(express.urlencoded({extended: true}));

const dbURL = "mongodb+srv://" + process.env.MONGOUSER + ":" + process.env.MONGOPW + "@cluster0.gwlov.mongodb.net/shanties2DB?retryWrites=true&w=majority"

try {
    mongoose.connect(dbURL, {useNewUrlParser: true, useUnifiedTopology: true}, ()=>console.log("Mongoose is connected"));
} catch (e) {
    console.log("No connection");
}

const shantySchema = {
    title: String,
    lyrics: [[String]]
};

const Shanty = mongoose.model("Shanty", shantySchema, 'shanties_bs');

app.get("/", function(req, res){
    res.sendFile("public/index.html")
});

app.get("/random", (req,res) => {

    Shanty.find({}, (err, foundShanties) => {
        if (!err){
            var randomShanty = foundShanties[Math.floor(Math.random()*foundShanties.length)];
            var randomVerse = randomShanty.lyrics[Math.floor(Math.random()*randomShanty.lyrics.length)];

            var result = {
                shanty: randomShanty.title,
                lyrics: randomVerse
            }

            res.send(result);
        }

        else {
            res.send(err);
        }
    });
});

app.get("/shanties/all", (req,res) => {

    Shanty.find({}, (err, foundShanties) => {
        if (!err){
            var result = []

            foundShanties.forEach((shanty) => {
                result.push(shanty.title)
            })

            res.send(result)
        }

        else {
            res.send(err);
        }
    });

});

app.get("/shanties", (req,res) => {

    const queryTitleLower = req.query.title.toLowerCase();
    const queryTitle = queryTitleLower.replace(/(^|\s)[A-Za-zÀ-ÖØ-öø-ÿ]/g, c => c.toUpperCase());
    
    Shanty.findOne({title: queryTitle}, (err, foundShanty) => {
        if (!err){
            if (!foundShanty) {
                var result = {
                    error: "No shanty found."
                }
                res.send(result);
            }
            else {
                var result = {
                    shanty: foundShanty.title,
                    lyrics: foundShanty.lyrics
                }

                res.send(result);
            }
        }

        else {
            res.send(err);
        }
    });

});

let port = process.env.PORT;
if (port == null || port == "") {
    port = 3000;
}

app.listen(port, function(){
    console.log("Server started successfully");
});