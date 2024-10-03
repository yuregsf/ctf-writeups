const path = require('path');
const express = require('express');
const pug = require('pug');
const router = express.Router();

router.post('/api/submit_players', (req, res) => {
    const players = ['player1', 'player2', 'player3'];
    const order = {};
    
    players.forEach(player => { order[player] = {} });
    
    const data = req.body;

    Object.keys(data).forEach((player) => {
        Object.keys(data[player]).forEach((name) => {
            order[player][name] = data[player][name]; 
        });
    });

    if (
        (data.player1 && data.player1.includes("vsm")) &&
        (data.player2 && data.player2.includes("gankd")) &&
        (data.player3 && data.player3.includes("zetsu"))
    ) {
        return res.json({
            'response': pug.compile('span Hello #{user}, thank you for letting us know!')({ user: 'guest' })
        });
    } else {
        return res.json({
            'response': 'Please provide us with the full name of an existing player.'
        });
    }
});

module.exports = router;
