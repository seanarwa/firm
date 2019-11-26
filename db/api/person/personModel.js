let mongoose = require("mongoose");

const Schema = mongoose.Schema;

let personSchema = new Schema(
  {
    // id: ID! is auto created by the database called "_id"
    person: {
      data: Buffer,
      contentType: String
    }
  },
  {
    timestamps: true // auto create createdAt and updatedAt
  }
);

const person = mongoose.model("person", personSchema);
module.exports = person;

// extra codes
// after line 3: const AutoIncrement = require('mongoose-sequence')(mongoose);
// after line 17: personSchema.plugin(AutoIncrement, {inc_field: 'personId'});
