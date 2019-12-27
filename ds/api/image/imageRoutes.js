let express = require( "express");
let imageController = require("./imageController");

const router = express.Router();
const controller = new imageController();

router.post("/", controller.createImage);
router.get("/", controller.getImages);
router.get("/:id", controller.getImageById);
router.put("/", controller.updateImageById);
router.delete("/", controller.deleteImageById);

module.exports = router;
