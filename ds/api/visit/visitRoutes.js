let express = require( "express");
let visitController = require("./visitController");

const router = express.Router();
const controller = new visitController();

router.post("/", controller.createVisit);
router.get("/", controller.getVisits);
router.get("/:id", controller.getVisitById);
router.put("/", controller.updateVisitById);
router.delete("/", controller.deleteVisitById);

module.exports = router;
