let personModel = require("./personModel");

class Person {}

Person.prototype.getPersons = (req, res) => {
  personModel.find({}, (err, data) => {
    if (err) {
      res.send(err);
    } else {
      res.send({
        success: true,
        message: "Person fetched successfully",
        data
      });
    }
  });
};

Person.prototype.getPersonById = (req, res) => {
  let id = req.params.id;
  personModel.findById(id, (err, result) => {
    if (err) {
      res.send(err);
    } else {
      res.send(result);
    }
  });
};

Person.prototype.createPerson = (req, res) => {
  let obj = req.body;
  let model = new personModel(obj);

  model.save((err, data) => {
    if (err) {
      res.send(err);
    } else {
      res.send({
        success: true,
        message: "Person fetched successfully",
        data
      });
    }
  });
};

Person.prototype.updatePersonById = (req, res) => {
  let obj = req.body;
  let id = req.body._id;
  personModel.findByIdAndUpdate(id, obj, (err, data) => {
    if (err) {
      res.send(err);
    } else {
      res.send(data);
    }
  });
};

Person.prototype.deletePersonById = (req, res) => {
  let id = req.body._id;
  console.log("delete Person ", req.body);
  personModel.findByIdAndDelete(id, (err, data) => {
    if (err) {
      res.send(err);
    } else {
      res.send(data);
    }
  });
};

module.exports = Person;
