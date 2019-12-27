let mongoose = require("mongoose");

const Schema = mongoose.Schema;

let personSchema = new Schema(
  {
    // id: ID! is auto created by the database called "_id"
    enrollments: [
      {
        type: mongoose.Schema.Types.ObjectId,
        ref: 'Enrollment'
      }
    ],
    visits: [
      {
        type: mongoose.Schema.Types.ObjectId,
        ref: 'Visit'
      }
    ]
  },
  {
    timestamps: true // auto create createdAt and updatedAt
  }
);

const person = mongoose.model("Person", personSchema);
module.exports = person;

// extra codes
// after line 3: const AutoIncrement = require('mongoose-sequence')(mongoose);
// after line 17: personSchema.plugin(AutoIncrement, {inc_field: 'personId'});
