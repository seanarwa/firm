let mongoose = require("mongoose");

const Schema = mongoose.Schema;

let enrollmentSchema = new Schema(
  {
    // id: ID! is auto created by the database called "_id"
    image: {
      data: Buffer,
      contentType: String
    },
    imageEncoding: [Number],
    imageNormalizedEncoding: [Number],
    imageConfidence: {
      type: Number,
      min: 0,
      max: 100
    }
  },
  {
    timestamps: true // auto create createdAt and updatedAt
  }
);

const enrollment = mongoose.model("Enrollment", enrollmentSchema);
module.exports = enrollment;

// extra codes
// after line 3: const AutoIncrement = require('mongoose-sequence')(mongoose);
// after line 17: enrollmentSchema.plugin(AutoIncrement, {inc_field: 'enrollmentId'});
