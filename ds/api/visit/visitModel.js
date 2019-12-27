let mongoose = require("mongoose");

const Schema = mongoose.Schema;

let visitSchema = new Schema(
  {
    // id: ID! is auto created by the database called "_id"
    name: String,
    time : {
      type : Date,
      default: Date.now
    },
    location: String,
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

const visit = mongoose.model("Visit", visitSchema);
module.exports = visit;

// extra codes
// after line 3: const AutoIncrement = require('mongoose-sequence')(mongoose);
// after line 17: visitSchema.plugin(AutoIncrement, {inc_field: 'visitId'});
