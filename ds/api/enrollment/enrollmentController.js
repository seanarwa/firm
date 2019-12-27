let enrollmentModel = require("./enrollmentModel");

class Enrollment {}

Enrollment.prototype.getEnrollments = (req, res) => {
  enrollmentModel.find({}, (err, data) => {
    if (err) {
      res.send(err);
    } else {
      res.send({
        success: true,
        message: "Enrollment fetched successfully",
        data
      });
    }
  });
};

Enrollment.prototype.getEnrollmentById = (req, res) => {
  let id = req.params.id;
  enrollmentModel.findById(id, (err, result) => {
    if (err) {
      res.send(err);
    } else {
      res.send(result);
    }
  });
};

Enrollment.prototype.createEnrollment = (req, res) => {
  let obj = req.body;
  let model = new enrollmentModel(obj);

  model.save((err, data) => {
    if (err) {
      res.send(err);
    } else {
      res.send({
        success: true,
        message: "Enrollment fetched successfully",
        data
      });
    }
  });
};

Enrollment.prototype.updateEnrollmentById = (req, res) => {
  let obj = req.body;
  let id = req.body._id;
  enrollmentModel.findByIdAndUpdate(id, obj, (err, data) => {
    if (err) {
      res.send(err);
    } else {
      res.send(data);
    }
  });
};

Enrollment.prototype.deleteEnrollmentById = (req, res) => {
  let id = req.body._id;
  console.log("delete Enrollment ", req.body);
  enrollmentModel.findByIdAndDelete(id, (err, data) => {
    if (err) {
      res.send(err);
    } else {
      res.send(data);
    }
  });
};

module.exports = Enrollment;
