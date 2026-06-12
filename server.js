const express = require("express");
const cors = require("cors");

const app = express();

app.use(cors());
app.use(express.json());

app.get("/users", (req, res) => {
    res.json(["love", "hate"]);
});

app.post("/signup", (req, res) => {

    console.log("Received:");
    console.log(req.body);

    res.json({
        success: true,
        message: "User received",
        data: req.body
    });

});

app.listen(8000, "0.0.0.0", () => {
    console.log("Server running on port 8000");
});