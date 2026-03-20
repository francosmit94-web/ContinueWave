Static Publish Commands

Artifact
- `PROJECTS/implementation_pages/atlasflow_v1_static.zip`

Integrity
- `SHA256: E613DBC9F85E5A5984115304186A11AFB6E7716297A6BA027CD6A04B03B4FB3D`

Local Smoke Run
```powershell
cd C:\Users\Franco\Desktop\ContinueWave\PROJECTS\implementation_pages
python -m http.server 8080
```

Netlify (CLI)
```powershell
cd C:\Users\Franco\Desktop\ContinueWave\PROJECTS\implementation_pages
netlify deploy --dir . --prod
```

Vercel (CLI)
```powershell
cd C:\Users\Franco\Desktop\ContinueWave\PROJECTS\implementation_pages
vercel --prod
```

GitHub Pages (gh-pages branch)
```powershell
cd C:\Users\Franco\Desktop\ContinueWave
git init
git add PROJECTS/implementation_pages
git commit -m "AtlasFlow v1 static pages"
git branch -M gh-pages
git remote add origin <YOUR_REPO_URL>
git push -u origin gh-pages --force
```

Post-Publish Spot Check
- open `index.html`
- open `homepage.html`
- open `contact.html`
- submit newsletter/contact forms against real endpoints (if wired)
