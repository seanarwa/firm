let mongoose = require("mongoose");

const Schema = mongoose.Schema;

let imageSchema = new Schema(
  {
    // id: ID! is auto created by the database called "_id"
    image: {
      data: Buffer,
      contentType: String
    }
  },
  {
    timestamps: true // auto create createdAt and updatedAt
  }
);

const image = mongoose.model("image", imageSchema);
module.exports = image;

// extra codes
// after line 3: const AutoIncrement = require('mongoose-sequence')(mongoose);
// after line 17: imageSchema.plugin(AutoIncrement, {inc_field: 'imageId'});
