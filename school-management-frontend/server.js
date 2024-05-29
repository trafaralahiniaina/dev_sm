const express = require('express');
const next = require('next');
const axios = require('axios');

const dev = process.env.NODE_ENV !== 'production';
const app = next({ dev });
const handle = app.getRequestHandler();
const PORT = process.env.PORT || 3000;
const API_BASE_URL = process.env.API_BASE_URL || 'http://localhost:8000/api';

app.prepare().then(() => {
  const server = express();

  // Middleware to set school based on subdomain
  server.use((req, res, next) => {
    const hostname = req.hostname;
    const schoolDomain = hostname.split('.')[0];
    req.schoolDomain = schoolDomain;
    next();
  });

  server.get('/api/schools/data', async (req, res) => {
    const { schoolDomain } = req;

    try {
      const response = await axios.get(`${API_BASE_URL}/schools/`, {
        params: {
          website__contains: schoolDomain,
        },
      });

      const schools = response.data;

      if (schools.length === 0) {
        res.status(404).send('School not found');
      } else {
        const school = schools[0];
        res.json(school);
      }
    } catch (error) {
      console.error('Error fetching school data:', error);
      res.status(500).send('Internal Server Error');
    }
  });

  // Handling all other requests
  server.get('*', (req, res) => {
    return handle(req, res);
  });

  server.listen(PORT, (err) => {
    if (err) throw err;
    console.log(`> Ready on http://localhost:${PORT}`);
  });
});