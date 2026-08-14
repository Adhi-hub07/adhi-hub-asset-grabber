<div align="center">

# 🎮 ADHI-HUB — Asset Grabber

**Paste a Roblox asset ID → get everything about it → download it.**

Works with **Hats, Decals, Audio, Meshes, Shirts, Pants, Gear, Animations, Plugins** and more.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)
![Version](https://img.shields.io/badge/Version-1.0-pink)
![Made with ❤](https://img.shields.io/badge/Made%20with-%E2%9D%A4-ff69b4)

</div>

---

## 🚀 Quick Start

[![Download start.bat](https://img.shields.io/badge/⬇_Download_start.bat-8fd3ff?style=for-the-badge)](https://raw.githubusercontent.com/Adhi-hub07/adhi-hub-asset-grabber/main/start.bat)

```bash
pip install rich
python asset_grabber.py
```

Then **paste any asset ID** — for example:

```
102611803        → Verified, Bonafide, Plaidafied (Hat)
2278114          → Roblox logo (Decal)
9128203637       → Mesh
```

You can also paste a full link — `https://www.roblox.com/catalog/102611803/...` — it auto-extracts the ID.

---

## ✨ What it shows you

| Info | Example |
|------|---------|
| 📛 Name | Verified, Bonafide, Plaidafied |
| 🏷 Type | Hat |
| 👤 Creator | Roblox (User) |
| 💰 Price | Free / 50 Robux |
| 📈 Sales | 1,234 |
| 📅 Created | 2013-01-03 |
| 🖼 Preview thumbnail | saved to `_previews/` |

## ⬇ Downloads

| Asset type | What you get |
|------------|--------------|
| Hats / Accessories / Gear | the `.mesh` / `.rbxm` file (importable in Studio) |
| Images / Decals / Shirts | the image file |
| Models / Animations | the `.rbxm` file |
| Audio | the `.mp3` (needs `cookie.txt` — see below) |

All files land in **`Downloads/ADHI-HUB Assets`** — one place for everything.

---

## 🔓 Unlock everything with your login (optional)

Some assets (audio, user uploads) need a Roblox login to download directly.
1. Get your `.ROBLOSECURITY` cookie (browser DevTools → Application → Cookies → `.ROBLOSECURITY`)
2. Create a file named **`cookie.txt`** next to `asset_grabber.py`
3. Paste the cookie inside — that's it. (never share it / never commit it — already gitignored)

---

## 🧑‍💻 Usage

```
1) Lookup / download an asset
2) History        ← last 50 lookups
3) Open folder    ← your downloads
0) Exit
```

---

## 📁 Project Structure

```
adhi-hub-asset-grabber/
├── asset_grabber.py    ← ⭐ the app
├── start.bat           ← Windows launcher
├── run.sh              ← Linux / macOS launcher
├── cookie.txt          ← (optional, yours only — ignored by git)
├── README.md
└── LICENSE             ← MIT
```

---

## ⚖️ License

**MIT** — free to use, share and modify. Built with ❤ by **ADHIHUB**.