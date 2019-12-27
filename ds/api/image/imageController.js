let imageModel = require("./imageModel");

class Image {}

Image.prototype.getImages = (req, res) => {
  imageModel.find({}, (err, data) => {
    if (err) {
      res.send(err);
    } else {
      res.send({
        success: true,
        message: "Image fetched successfully",
        data
      });
    }
  });
};

Image.prototype.getImageById = (req, res) => {
  let id = req.params.id;
  imageModel.findById(id, (err, result) => {
    if (err) {
      res.send(err);
    } else {
      res.send(result);
    }
  });
};

Image.prototype.createImage = (req, res) => {
  let obj = req.body;
  let model = new imageModel(obj);

  model.save((err, data) => {
    if (err) {
      res.send(err);
    } else {
      res.send({
        success: true,
        message: "Image fetched successfully",
        data
      });
    }
  });
};

Image.prototype.updateImageById = (req, res) => {
  let obj = req.body;
  let id = req.body._id;
  imageModel.findByIdAndUpdate(id, obj, (err, data) => {
    if (err) {
      res.send(err);
    } else {
      res.send(data);
    }
  });
};

Image.prototype.deleteImageById = (req, res) => {
  let id = req.body._id;
  console.log("delete Image ", req.body);
  imageModel.findByIdAndDelete(id, (err, data) => {
    if (err) {
      res.send(err);
    } else {
      res.send(data);
    }
  });
};

module.exports = Image;
