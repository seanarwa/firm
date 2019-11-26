let express = require( "express");
let personController = require("./personController");

const router = express.Router();
const controller = new personController();

router.post("/", controller.createPerson);
router.get("/", controller.getPersons);
router.get("/:id", controller.getPersonById);
router.put("/", controller.updatePersonById);
router.delete("/", controller.deletePersonById);

module.exports = router;
