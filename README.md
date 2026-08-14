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

### Option A — EXE (easiest, for everyone)

No Python. No installs. Just download & double-click.

[![Download EXE](https://img.shields.io/badge/⬇_Download_ADHI--HUB--Asset--Grabber.exe-pink?style=for-the-badge)](https://github.com/Adhi-hub07/adhi-hub-asset-grabber/releases/download/v1.0.0/ADHI-HUB-Asset-Grabber.exe)

**One-line command (Windows PowerShell):**
```powershell
irm https://github.com/Adhi-hub07/adhi-hub-asset-grabber/releases/download/v1.0.0/ADHI-HUB-Asset-Grabber.exe -OutFile ADHI-HUB-Asset-Grabber.exe; .\ADHI-HUB-Asset-Grabber.exe
```

### Option B — Python source

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

## 🔓 When do you need the login cookie?

| Asset type | Login needed? |
|------------|----------------|
| ✅ **Normal** — hats, decals, images, shirts, faces, gear, animations | **No** — paste ID, download instantly |
| 🔒 **Private / Music** — audio (music IDs), private uploads, limited items | **Yes** — set your cookie in Settings |

**Set the cookie right inside the app:** `4) Settings → Set cookie` → paste your
`.ROBLOSECURITY` value (browser DevTools → Application → Cookies → `.ROBLOSECURITY`),
or press **`6) Help`** in the app for the full 1-minute guide.

Your cookie stays on YOUR device only (`cookie.txt`, gitignored — never shared).

---

## ⚡ What it can do

| Feature | Description |
|---------|-------------|
| 🎮 **Asset lookup** | Name, type, creator, price, sales, created + link |
| 🎵 **Music IDs** | Paste any audio ID → downloads the MP3 (with cookie) |
| 🔓 **Private assets** | Set your cookie in Settings → grab login-only assets |
| 📦 **Batch mode** | `13277990, 102611803, 2278114` → grabs all in a row |
| 📋 **Copy link** | One key → asset URL copied to clipboard |
| 🏷 **Metadata export** | `.txt` (name/creator/desc/price) saved next to every download |
| 🖼 **Previews** | Thumbnails saved to `_previews/` (420px or 720px in Settings) |
| 🕘 **History** | Last 50 lookups |
| 📁 **One folder** | Everything lands in `Downloads/ADHI-HUB Assets` |

## 🧑‍💻 Usage

```
1) Lookup / download   2) Batch mode   3) History
4) ⚙ Settings          5) Open folder  0) Exit
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