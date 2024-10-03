const express = require('express');
const path = require('path');
const fs = require('fs');
const app = express();
const port = 3000;

app.use(express.json());
app.use(express.static('public'));

// Object to store API tokens for each username
const userTokens = {};

// Middleware to check API token and username
const checkApiToken = (req, res, next) => {
  const token = req.headers['x-api-token'];
  const username = req.headers['x-username'];
  console.log(token, username)
  console.log(userTokens[username])
  console.log("typeof token from header: ", typeof token)
  console.log("typeof userTokens[username]: ", typeof userTokens[username])
  if (!username || !token || userTokens[username] != token) {
    delete userTokens[username];
    return res.status(401).json({ error: 'Unauthorized' });
  }
  next();
};

// Serve index.html
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// Serve admin.html
app.get('/admin', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'admin.html'));
});

// Admin API endpoint with token authorization
app.get('/api/admin', checkApiToken, (req, res) => {
  res.json({ message: 'Welcome to the admin endpoint!' });
});

// New endpoint to return flag.txt content
app.get('/api/flag', checkApiToken, (req, res) => {
  fs.readFile('/app/flag.txt', 'utf8', (err, data) => {
    if (err) {
      console.error(err);
      return res.status(500).json({ error: 'Error reading flag file' });
    }
    res.json({ flag: data.trim() });
  });
});

// Endpoint to generate 5 random numbers (accessible by all users)
app.get('/api/random', (req, res) => {
  const randomNumbers = Array.from({ length: 20 }, () => Math.floor(Math.random() * 9000000000000000));
  res.json({ numbers: randomNumbers });
});

// Endpoint to generate/update the API token for a username
app.post('/api/update-token', (req, res) => {
  const { username } = req.body;
  if (!username) {
    return res.status(400).json({ error: 'Username is required' });
  }
  const newToken = Math.floor(Math.random() * 9000000000000000);
  userTokens[username] = newToken;
  res.json({ message: 'API token updated successfully for ' + username });
});

app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
});
