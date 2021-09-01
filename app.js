require('dotenv').config();
const { text } = require("body-parser");
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
    lyrics: [String]
};

const Shanty = mongoose.model("Shanty", shantySchema);

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

let port = process.env.PORT;
if (port == null || port == "") {
    port = 3000;
}

app.listen(port, function(){
    console.log("Server started successfully");
});