const express = require('express');
const app = express();
const path = require('path');
app.use('/admin', (req, res, next) => {
	  const bypass = req.headers['x-middleware-subrequest'];
	  if (bypass && bypass.includes('middleware:middleware')) {
		      return next();
		    }
	  return res.redirect('https://youtu.be/W8DCWI_Gc9c?si=L-fDdWK4YnGJtEfB');
});

app.get('/admin', (req, res) => {
	  res.send('NHNC{ANon_iS_cUtE_RIGhT?}');
});
app.use(express.static('public'));
app.get('/', (req, res) => {
	  res.sendFile(path.join(__dirname, 'public', 'a2.jpg'));
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`CTF server running at http://localhost:${PORT}`);
});

