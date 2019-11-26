let express = require('express');

let models = [
	"image",
	"person"
];

const app = express();

models.forEach((model) => {
    let routes = require(`./${model}/${model}Routes`);
    app.use(`/${model}`, routes)
});

module.exports = app;