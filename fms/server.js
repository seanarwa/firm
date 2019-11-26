let express = require('express');
let bodyParser = require('body-parser');
let dotenv = require('dotenv');
var multer  = require('multer');
var fs = require('fs');
var data = multer({ dest: 'data/' });

// set environment variables
dotenv.config();

// express app
const app = express();

// configure app
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());

let port = process.env.PORT || 226

// Root path
app.get('/', (req,res) => {
    return res.end('firm-fms is running');
});

app.post('/',
        data.single('image'),
        (req, res, next) => {
            console.log(req.body.name)
            res.send('image received')
        }
);

// catch 404
app.use((req, res, next) => {
    res.status(404).send('ERROR: request path not found');
});

// start the server
var server = app.listen(port,() => {
    var port = server.address().port;
    console.log(`firm-fms started on port ${port}`);
});
  
module.exports = app;