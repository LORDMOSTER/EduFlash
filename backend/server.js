const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');

const app = express();
const PORT = process.env.PORT || 5000; // Use 5000 as the default port

app.use(cors()); // Allow Cross-Origin requests
app.use(bodyParser.json()); // Parse JSON bodies

// Test Endpoint
app.get('/', (req, res) => {
  res.send('Welcome to EduFlash API!');
});

// Start the server
app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});
