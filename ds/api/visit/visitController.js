let visitModel = require("./visitModel");

class Visit {}

Visit.prototype.getVisits = (req, res) => {
  visitModel.find({}, (err, data) => {
    if (err) {
      res.send(err);
    } else {
      res.send({
        success: true,
        message: "Visit fetched successfully",
        data
      });
    }
  });
};

Visit.prototype.getVisitById = (req, res) => {
  let id = req.params.id;
  visitModel.findById(id, (err, result) => {
    if (err) {
      res.send(err);
    } else {
      res.send(result);
    }
  });
};

Visit.prototype.createVisit = (req, res) => {
  let obj = req.body;
  let model = new visitModel(obj);

  model.save((err, data) => {
    if (err) {
      res.send(err);
    } else {
      res.send({
        success: true,
        message: "Visit fetched successfully",
        data
      });
    }
  });
};

Visit.prototype.updateVisitById = (req, res) => {
  let obj = req.body;
  let id = req.body._id;
  visitModel.findByIdAndUpdate(id, obj, (err, data) => {
    if (err) {
      res.send(err);
    } else {
      res.send(data);
    }
  });
};

Visit.prototype.deleteVisitById = (req, res) => {
  let id = req.body._id;
  console.log("delete Visit ", req.body);
  visitModel.findByIdAndDelete(id, (err, data) => {
    if (err) {
      res.send(err);
    } else {
      res.send(data);
    }
  });
};

module.exports = Visit;
