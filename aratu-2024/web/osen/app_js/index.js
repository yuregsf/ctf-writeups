const express       = require('express');
const app           = express();
const routes        = require('./routes');
const path          = require('path');

app.use(express.json());
app.use(routes);

app.all('*', (req, res) => {
    return res.status(404).send('404 page not found');
});

app.listen(3000, () => console.log('Listening on port 3000'));