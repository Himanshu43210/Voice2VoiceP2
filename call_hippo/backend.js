// Express.js example


const express = require('express');
const axios = require('axios');
const cors = require('cors');
const app = express();

// Use middlewares
app.use(cors());
app.use(express.json());

// const express = require('express');
// const axios = require('axios');
// const app = express();

app.post('/initiateCall', async (req, res) => {
    const apiToken = '651f50e419eb2b1e8979e724'; // Store securely!
    const phoneNumber = req.body.phoneNumber;
    const loggedInUserEmail = req.body.loggedInUserEmail;

    try {
        const response = await axios.post('https://web.callhippo.com/v1/user/add', {
            token: apiToken,
            email: loggedInUserEmail,
            number: phoneNumber,
            // add other necessary parameters as required
        });

        res.status(200).json({ success: true, message: 'Call initiated' });
    } catch (error) {
        res.status(500).json({ success: false, message: 'Error initiating call' });
    }
});

app.listen(3000, () => {
    console.log('Server started on http://localhost:3000');
});
