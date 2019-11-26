let express = require('express');
let mongoose = require('mongoose');
let bodyParser = require('body-parser');
let dotenv = require('dotenv');

let routes = require('./api/routes');

// set environment variables
dotenv.config();

// express app
const app = express();

// configure mongoose options
mongoose.set('useNewUrlParser', true);
mongoose.set('useFindAndModify', false);
mongoose.set('useCreateIndex', true);
mongoose.set('useUnifiedTopology', true);

// mongoose instance connection url connection
mongoose.Promise = global.Promise;
mongoose.connect('mongodb://localhost/firm');

// configure app
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());

let port = process.env.PORT || 443

// Root path
app.get('/', (req,res) => {
    return res.end('API is running');
});

// Load API routes
app.use('/', routes);

// catch 404
app.use((req, res, next) => {
    res.status(404).send('<h2 align=center>Page Not Found</h2>');
});

// start the server
var server = app.listen(port,() => {
    var port = server.address().port;
    console.log(`firm-db REST API started on port ${port}`);
});
  
module.exports = app;