const express = require("express")
const app = express()

app.use(express.json())

const users = ["love", "hate"]

app.get("/users", (request, response) => {
  response.json(users)
})

app.listen(8000)

