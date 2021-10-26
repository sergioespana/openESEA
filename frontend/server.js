const express = require('express')
const serveStatic = require('serve-static')
const path = require('path')

const app = express()

// const port = 3000

app.use('/', serveStatic(path.join(__dirname, '/dist')))

const port = process.env.PORT || 8080

// app.get('/', (req, res) => {
//   res.send('Hello World!')
// })

app.listen(port, () => {
  console.log(`Example app listening at http://localhost:${port}`)
})