# Next Song is 春日影 - Writeup

## Description

<p align="center">
  <img src="No Hack No CTF 2025/Next song is 春日影/image1.png" width="700" alt="challenge banner / screenshot 1">
</p>

“NextJS Vulnerability at /admin”

`Author: Frank`

[https://nhnc\_next-song.frankk.uk](https://nhnc_next-song.frankk.uk/)

<p align="center">
  <img src="E:\CTF\writeup git\No Hack No CTF 2025\Catch The Goose - Writeup\image2.jpg" width="800" alt="Hacker animation">
</p>

A little curious, I clicked the link with the hope that its not “never gonna give u up”.

<p align="center">
  <img src="E:\CTF\writeup git\No Hack No CTF 2025\Catch The Goose - Writeup\image3.jpg" width="800" alt="Hacker animation">
</p>

okayy, so whats now.

Hmm. It's redirecting me to a YouTube video. Probably a **decoy** — redirection is often used to mislead or prevent unauthorized access. Plus, I got the description from the start “NextJS Vulnerability at /admin”. So I searched it, it matches, what is happening in the challenge.

[https://www.picussecurity.com/resource/blog/cve-2025-29927-nextjs-middleware-bypass-vulnerability](https://www.picussecurity.com/resource/blog/cve-2025-29927-nextjs-middleware-bypass-vulnerability)

<p align="center">
  <img src="E:\CTF\writeup git\No Hack No CTF 2025\Catch The Goose - Writeup\image4.jpg" width="800" alt="Hacker animation">
</p>

<p align="center">
  <img src="E:\CTF\writeup git\No Hack No CTF 2025\Catch The Goose - Writeup\image5.jpg" width="800" alt="Hacker animation">
</p>

just copy and paste the `X-Middleware-Subrequest: src/middleware:nowaf:src/middleware:src/middleware:src/middleware:src/middleware:middleware:middleware:nowaf:middleware:middleware:middleware:pages/_middleware`

then I got the flag.

<p align="center">
  <img src="E:\CTF\writeup git\No Hack No CTF 2025\Catch The Goose - Writeup\image6.jpg" width="800" alt="Hacker animation">
</p>
