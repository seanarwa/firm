let express = require( "express");
let enrollmentController = require("./enrollmentController");

const router = express.Router();
const controller = new enrollmentController();

router.post("/", controller.createEnrollment);
router.get("/", controller.getEnrollments);
router.get("/:id", controller.getEnrollmentById);
router.put("/", controller.updateEnrollmentById);
router.delete("/", controller.deleteEnrollmentById);

module.exports = router;
