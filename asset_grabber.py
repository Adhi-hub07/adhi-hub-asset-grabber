import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.request

if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stdin.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

APP_DIR = os.path.dirname(os.path.abspath(__file__))
HISTORY = os.path.join(APP_DIR, "history.json")
SETTINGS = os.path.join(APP_DIR, "settings.json")
COOKIE_FILE = os.path.join(APP_DIR, "cookie.txt")
DOWNLOADS = os.path.join(os.path.expanduser("~"), "Downloads", "ADHI-HUB Assets")
PREVIEWS = os.path.join(DOWNLOADS, "_previews")

UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"}

BANNER = r"""[bold magenta]
     █████╗ ██████╗ ██╗  ██╗██╗
    ██╔══██╗██╔══██╗██║  ██║██║
    ███████║██║  ██║███████║██║
    ██╔══██║██║  ██║██╔══██║██║
    ██║  ██║██████╔╝██║  ██║██║
    ╚═╝  ╚═╝╚═════╝ ╚═╝  ╚═╝╚═╝
[/bold magenta]"""
TAGLINE = "[bold]ASSET GRABBER[/bold]  —  paste an asset ID, get everything about it"
VERSION = "1.2.0"


def check_update():
    try:
        data = fetch_json("https://api.github.com/repos/Adhi-hub07/adhi-hub-asset-grabber/releases/latest")
        tag = (data.get("tag_name") or "").lstrip("v")
        if tag:
            theirs = tuple(int(x) for x in re.split(r"[.-]", tag) if x.isdigit())
            mine = tuple(int(x) for x in re.split(r"[.-]", VERSION) if x.isdigit())
            if theirs > mine:
                console.print(f"[bold yellow]⬆ New version {tag} available![/bold yellow]")
                console.print(f"[dim]   Get it: https://github.com/Adhi-hub07/adhi-hub-asset-grabber/releases/latest[/dim]\n")
    except Exception:
        pass

ASSET_TYPES = {
    1: ("Image", ".png"),
    2: ("T-Shirt", ".png"),
    3: ("Audio", ".mp3"),
    4: ("Mesh", ".mesh"),
    5: ("Lua", ".lua"),
    8: ("Hat", ".mesh"),
    11: ("Shirt", ".png"),
    12: ("Pants", ".png"),
    13: ("T-Shirt Accessory", ".mesh"),
    17: ("Head", ".mesh"),
    18: ("Face", ".png"),
    19: ("Gear", ".rbxm"),
    24: ("Animation", ".rbxm"),
    27: ("Decal", ".png"),
    28: ("Video", ".mp4"),
    37: ("Plugin", ".rbxm"),
    40: ("MeshPart", ".mesh"),
    41: ("Hair Accessory", ".mesh"),
    42: ("Face Accessory", ".mesh"),
    43: ("Neck Accessory", ".mesh"),
    44: ("Shoulder Accessory", ".mesh"),
    45: ("Front Accessory", ".mesh"),
    46: ("Back Accessory", ".mesh"),
    47: ("Waist Accessory", ".mesh"),
    48: ("Climb Animation", ".rbxm"),
    49: ("Death Animation", ".rbxm"),
    50: ("Fall Animation", ".rbxm"),
    51: ("Idle Animation", ".rbxm"),
    52: ("Jump Animation", ".rbxm"),
    53: ("Run Animation", ".rbxm"),
    54: ("Swim Animation", ".rbxm"),
    55: ("Walk Animation", ".rbxm"),
    61: ("Emote Animation", ".rbxm"),
    62: ("Video", ".mp4"),
    64: ("T-Shirt Accessory", ".mesh"),
    75: ("Mesh (Hidden Surface Removal)", ".mesh"),
}


def load_settings():
    try:
        return json.load(open(SETTINGS, encoding="utf-8"))
    except Exception:
        return {}


def save_settings(s):
    json.dump(s, open(SETTINGS, "w", encoding="utf-8"), indent=2)


def thumb_size():
    return int(load_settings().get("thumb_size", 420))


def load_cookie():
    if os.path.exists(COOKIE_FILE):
        c = open(COOKIE_FILE, encoding="utf-8-sig").read().strip()
        if "|_" in c:
            c = c.split("|_", 1)[-1]
        return c or None
    return None


def fetch_json(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.loads(r.read().decode("utf-8", "replace"))


def fetch_bytes(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()


def download_bytes(asset_id, cookie=None):
    urls = [
        f"https://assetdelivery.roblox.com/v1/asset?id={asset_id}",
        f"https://assetdelivery.roblox.com/v1/asset/?id={asset_id}",
        f"https://www.roblox.com/asset/?id={asset_id}",
    ]
    last_err = None
    for u in urls:
        try:
            headers = dict(UA)
            if cookie:
                headers["Cookie"] = f".ROBLOSECURITY={cookie}"
            req = urllib.request.Request(u, headers=headers)
            with urllib.request.urlopen(req, timeout=60) as r:
                return r.read(), None
        except Exception as e:
            last_err = e
            continue
    return None, last_err


def human_size(n):
    for unit in ("B", "KB", "MB", "GB"):
        if n < 1024:
            return f"{n:.1f} {unit}"
        n /= 1024
    return f"{n:.1f} TB"


def extract_ids(text):
    ids = []
    m = re.search(r"roblox\.com/(?:catalog|library)/(\d+)", text)
    if m:
        ids.append(int(m.group(1)))
    for t in re.split(r"[,;\s]+", text):
        t = t.strip()
        if t.isdigit():
            ids.append(int(t))
    return list(dict.fromkeys(ids))


def lookup(asset_id):
    info = None
    try:
        info = fetch_json(f"https://economy.roblox.com/v2/assets/{asset_id}/details")
        if "errors" in info:
            info = None
    except Exception:
        info = None
    if not info:
        try:
            info = fetch_json(f"https://catalog.roblox.com/v1/assets/{asset_id}")
            if "errors" in info or "id" not in info:
                info = None
        except Exception:
            info = None
    return info


def get_thumbnail(asset_id):
    try:
        size = thumb_size()
        data = fetch_json(f"https://thumbnails.roblox.com/v1/assets?assetIds={asset_id}&size={size}x{size}&format=Png&isCircular=false")
        url = (data.get("data") or [{}])[0].get("imageUrl")
        if url:
            return fetch_bytes(url)
    except Exception:
        pass
    return None


def safe_name(name):
    return re.sub(r'[\\/*?:"<>|]', "_", name or "asset")[:80]


def copy_clipboard(text):
    try:
        if os.name == "nt":
            subprocess.run(["clip"], input=text.encode("utf-16-le"), check=True)
        else:
            for cmd in (["xclip", "-selection", "clipboard"], ["xsel", "-b"]):
                try:
                    subprocess.run(cmd, input=text.encode("utf-8"), check=True)
                    return True
                except Exception:
                    continue
        return True
    except Exception:
        return False


def show_info(asset_id, info, interactive=True):
    if not info:
        console.print(Panel(f"[yellow]Could not fetch details for asset [bold]#{asset_id}[/bold][/yellow]\n"
                            f"[dim]It may be deleted, private, or not in the catalog.[/dim]\n"
                            f"[dim]You can still try downloading the raw file.[/dim]",
                            title=f"⚠ No details", border_style="yellow"))
        return None, None, None

    aid = info.get("id") or info.get("assetId") or asset_id
    name = info.get("Name") or info.get("name") or f"Asset {aid}"
    desc = info.get("Description") or info.get("description") or ""
    atype = info.get("AssetTypeId") or info.get("assetType") or None
    if isinstance(atype, dict):
        type_name = atype.get("name", "Unknown")
        ext = ".mesh"
    else:
        type_name, ext = ASSET_TYPES.get(atype, ("Asset", ".bin"))

    creator = info.get("Creator") or info.get("creator") or {}
    creator_name = creator.get("Name") or creator.get("name") or "Unknown"
    creator_type = creator.get("CreatorType") or creator.get("type") or "User"

    price = info.get("PriceInRobux") or info.get("price") or 0
    sales = info.get("Sales") or info.get("sales") or 0
    created = (info.get("Created") or info.get("created") or "?").split("T")[0]
    link = f"https://www.roblox.com/library/{aid}"

    t = Table(show_header=False, box=None, padding=(0, 2))
    t.add_column(style="bold cyan", width=14)
    t.add_column(style="white")
    t.add_row("Name", f"[bold]{name}[/bold]")
    t.add_row("Type", type_name)
    t.add_row("Creator", f"{creator_name} ({creator_type})")
    t.add_row("Price", f"🪙 {price} Robux" if price else "Free")
    t.add_row("Sales", str(sales))
    t.add_row("Created", created)
    t.add_row("Roblox", link)
    if desc:
        t.add_row("Description", desc[:220])
    console.print(Panel(t, title=f"🎮 Asset #{aid}", border_style="magenta"))

    if interactive and input("\n📋 Copy the asset link? [y/N] ").strip().lower() in ("y", "yes"):
        copy_clipboard(link)
        console.print("[green]✅ Link copied to clipboard[/green]")

    return type_name, ext, info


def save_history(asset_id, name, type_name):
    hist = []
    if os.path.exists(HISTORY):
        try:
            hist = json.load(open(HISTORY, encoding="utf-8"))
        except Exception:
            hist = []
    hist.insert(0, {"id": asset_id, "name": name, "type": type_name})
    json.dump(hist[:50], open(HISTORY, "w", encoding="utf-8"), indent=2)


def save_metadata(asset_id, info, path):
    if not info:
        return
    name = info.get("Name") or info.get("name") or ""
    desc = info.get("Description") or info.get("description") or ""
    atype = info.get("AssetTypeId") or "?"
    creator = info.get("Creator") or {}
    price = info.get("PriceInRobux") or info.get("price") or 0
    sales = info.get("Sales") or info.get("sales") or 0
    created = (info.get("Created") or info.get("created") or "?")
    lines = [
        f"Asset ID      : {asset_id}",
        f"Name          : {name}",
        f"Type          : {atype}",
        f"Creator       : {creator.get('Name', '?')}",
        f"Price         : {price} Robux",
        f"Sales         : {sales}",
        f"Created       : {created}",
        f"Link          : https://www.roblox.com/library/{asset_id}",
        f"Description   : {desc}" if desc else "",
    ]
    try:
        meta_path = os.path.splitext(path)[0] + ".txt"
        open(meta_path, "w", encoding="utf-8").write("\n".join(lines))
    except Exception:
        pass


def download_asset(asset_id, ext, name, thumb, type_name=None, info=None):
    os.makedirs(DOWNLOADS, exist_ok=True)
    os.makedirs(PREVIEWS, exist_ok=True)
    if thumb:
        try:
            tp = os.path.join(PREVIEWS, f"{asset_id}_preview.png")
            open(tp, "wb").write(thumb)
        except Exception:
            pass
    cookie = load_cookie()
    with console.status(f"[cyan]Downloading asset #{asset_id}..."):
        data, err = download_bytes(asset_id, cookie)

    if data and len(data) >= 4:
        path = os.path.join(DOWNLOADS, f"{safe_name(name)}__{asset_id}{ext}")
        open(path, "wb").write(data)
        save_metadata(asset_id, info, path)
        console.print(f"[green]✅ Saved [bold]{os.path.basename(path)}[/bold] ({human_size(len(data))})[/green]")
        console.print(f"[dim]   📁 {DOWNLOADS}[/dim]")
        return True

    if thumb and ext == ".png":
        path = os.path.join(DOWNLOADS, f"{safe_name(name)}__{asset_id}.png")
        open(path, "wb").write(thumb)
        save_metadata(asset_id, info, path)
        console.print(f"[green]✅ Saved image via preview [bold]{os.path.basename(path)}[/bold][/green]")
        console.print(f"[dim]   📁 {DOWNLOADS}[/dim]")
        return True

    hint = ""
    err_text = str(err or "")
    if "403" in err_text or "not authorized" in err_text:
        hint = ("\n[yellow]💡 This asset is RESTRICTED — the owner (or Roblox) blocked direct\n"
                "   download for this account. That's the asset's choice, not yours.\n"
                "   Other IDs usually work — try another![/yellow]")
    elif "409" in err_text:
        hint = "\n[yellow]💡 This asset is DELISTED (409) — removed from delivery but still in\n   the catalog. Nothing can download it.[/yellow]"
    elif not cookie and type_name in ("Audio",):
        hint = ("\n[yellow]💡 MUSIC assets need your login.\n"
                "   Normal assets (hats, decals, images) work WITHOUT login.\n"
                "   For music/private: Settings → Set cookie → paste .ROBLOSECURITY → done.[/yellow]")
    elif not cookie:
        hint = ("\n[yellow]💡 This asset is login-only (private / restricted).\n"
                "   Normal assets need NO login. For private ones: Settings → Set cookie.\n"
                "   Type 9 (Help) to see the 1-minute guide.[/yellow]")
    console.print(f"[red]❌ Download failed: {err}{hint}[/red]")
    return False


def grab_one(aid, auto_dl=False):
    with console.status(f"[cyan]Fetching asset #{aid}..."):
        info = lookup(aid)
        thumb = get_thumbnail(aid)
    type_name, ext, info = show_info(aid, info, interactive=not auto_dl)
    name = (info or {}).get("Name") or (info or {}).get("name") or f"asset_{aid}"
    save_history(aid, name, type_name or "?")
    if auto_dl or input("\n⬇ Download the file? [y/N] ").strip().lower() in ("y", "yes"):
        return download_asset(aid, ext or ".bin", name, thumb, type_name, info)
    console.print()
    return True


def pick_items_table(title, items):
    t = Table(title=title, header_style="bold magenta")
    t.add_column("#", width=4)
    t.add_column("ID", style="cyan")
    t.add_column("Name", style="white", overflow="fold")
    t.add_column("Type", style="yellow")
    for i, it in enumerate(items[:15], 1):
        tn = it.get("assetType", {}).get("name", "?") if isinstance(it.get("assetType"), dict) else "?"
        t.add_row(str(i), str(it.get("id")), str(it.get("name", "?")), tn)
    console.print(t)
    pick = input("\n➜ Pick number(s) or 'all': ").strip().lower()
    if pick == "all":
        return [it["id"] for it in items[:15]]
    ids = []
    for p in re.split(r"[,;\s]+", pick):
        if p.isdigit() and 1 <= int(p) <= min(len(items), 15):
            ids.append(items[int(p) - 1]["id"])
    return ids


def search_assets():
    console.print("[dim]Search the Roblox catalog — type a keyword:[/dim]")
    kw = input("➜  ").strip()
    if not kw:
        return
    try:
        import urllib.parse
        data = fetch_json("https://catalog.roblox.com/v1/search/items/details?category=All&limit=10&keyword=" + urllib.parse.quote(kw))
    except Exception as e:
        console.print(f"[red]❌ Search failed: {e}[/red]")
        return
    items = [it for it in (data.get("data") or []) if it.get("id")]
    if not items:
        console.print("[yellow]No results for that keyword.[/yellow]")
        return
    ids = pick_items_table(f"🔎 Results for '{kw}'", items)
    if not ids:
        console.print("[red]❌ No valid picks.[/red]")
        return
    console.print(f"[cyan]Grabbing {len(ids)} asset(s)...[/cyan]\n")
    ok = 0
    for aid in ids:
        console.rule(f"Asset #{aid}")
        if grab_one(aid, auto_dl=True):
            ok += 1
    console.rule()
    console.print(f"[green]✅ Done: {ok}/{len(ids)} downloaded.[/green]")


def import_file():
    console.print("[dim]Drag the .txt file here or type its full path (Enter = ids.txt in this folder):[/dim]")
    raw = input("➜  ").strip().strip('"')
    path = raw or os.path.join(APP_DIR, "ids.txt")
    if not os.path.exists(path):
        console.print(f"[red]❌ File not found: {path}[/red]")
        return
    try:
        lines = open(path, encoding="utf-8").read().splitlines()
    except Exception as e:
        console.print(f"[red]❌ Can't read file: {e}[/red]")
        return
    ids, bad = [], 0
    for ln in lines:
        found = extract_ids(ln)
        if found:
            ids.extend(found)
        elif ln.strip() and not ln.strip().startswith("#"):
            bad += 1
    ids = list(dict.fromkeys(ids))
    if not ids:
        console.print("[red]❌ No valid IDs found in that file.[/red]")
        return
    console.print(f"[cyan]📄 {os.path.basename(path)} — {len(ids)} ID(s) found, {bad} line(s) skipped (empty/bad).[/cyan]\n")
    ok = 0
    for i, aid in enumerate(ids, 1):
        console.rule(f"[{i}/{len(ids)}] Asset #{aid}")
        if grab_one(aid, auto_dl=True):
            ok += 1
    console.rule()
    fail = len(ids) - ok
    if fail:
        console.print(f"[green]✅ Done: {ok} downloaded, [red]{fail} failed[/red] ({len(ids)} total).[/green]")
    else:
        console.print(f"[green]✅ Done: ALL {ok} downloaded successfully! 🎉[/green]")


def creator_mode():
    console.print("[dim]Paste a creator's username (e.g. Roblox) or their user ID:[/dim]")
    raw = input("➜  ").strip()
    uid = None
    if raw.isdigit():
        uid = int(raw)
    else:
        try:
            body = json.dumps({"usernames": [raw]}).encode()
            req = urllib.request.Request("https://users.roblox.com/v1/usernames/users", data=body,
                                         headers={**UA, "Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=20) as r:
                res = json.loads(r.read().decode("utf-8", "replace"))
            uid = (res.get("data") or [{}])[0].get("id")
        except Exception as e:
            console.print(f"[red]❌ Username lookup failed: {e}[/red]")
            return
    if not uid:
        console.print("[red]❌ User not found.[/red]")
        return
    try:
        data = fetch_json(f"https://catalog.roblox.com/v1/search/items/details?category=All&creatorType=User&creatorTargetId={uid}&limit=10")
    except Exception as e:
        console.print(f"[red]❌ Couldn't load creations: {e}[/red]")
        return
    items = [it for it in (data.get("data") or []) if it.get("id")]
    if not items:
        console.print("[yellow]No public creations found for this creator.[/yellow]")
        return
    ids = pick_items_table(f"👤 Creations of '{raw}' (user {uid})", items)
    if not ids:
        console.print("[red]❌ No valid picks.[/red]")
        return
    console.print(f"[cyan]Grabbing {len(ids)} asset(s)...[/cyan]\n")
    ok = 0
    for aid in ids:
        console.rule(f"Asset #{aid}")
        if grab_one(aid, auto_dl=True):
            ok += 1
    console.rule()
    console.print(f"[green]✅ Done: {ok}/{len(ids)} downloaded.[/green]")


def show_help():
    console.print(Panel(
        "[bold green]✅ NORMAL assets — NO login needed[/bold green]\n"
        "   Hats, decals, images, shirts, faces, gear, animations...\n"
        "   → Just paste the ID and download. Works instantly.\n\n"
        "[bold yellow]🔒 PRIVATE / MUSIC assets — needs your cookie[/bold yellow]\n"
        "   Audio (music IDs), user uploads (meshes/models), private uploads...\n"
        "   → Roblox requires a login to grab these.\n\n"
        "[bold cyan]🔑 HOW TO GET YOUR COOKIE (1 minute)[/bold cyan]\n"
        "   1. Open roblox.com in Chrome (logged in)\n"
        "   2. Press F12 → click the \"Application\" tab\n"
        "   3. Cookies → https://www.roblox.com\n"
        "   4. Find \".ROBLOSECURITY\" → copy its value\n"
        "   5. In this app: Settings → Set cookie → paste it\n"
        "   → Done! Private & music assets now download.\n\n"
        "[bold]WHAT YOU CAN GRAB:[/bold]\n"
        "   • Without login: all normal public assets (instant)\n"
        "   • With login: EVERYTHING visible on roblox.com —\n"
        "     all music IDs, all user uploads, all catalog items\n"
        "   • Nobody can grab: truly private (owner-only) or\n"
        "     deleted assets — not even with a cookie\n\n"
        "[dim]🛡 Your cookie stays on YOUR device only (cookie.txt, never shared).[/dim]",
        title="ℹ HOW IT WORKS", border_style="green"))
    console.print()


def settings_menu():
    while True:
        cookie = load_cookie()
        status = "[green]✅ SET[/green]" if cookie else "[yellow]⚠️ NOT SET[/yellow]"
        console.print(Panel(f"Cookie (.ROBLOSECURITY): {status}\n"
                            f"Thumbnail size: [cyan]{thumb_size()}px[/cyan]\n\n"
                            f"  [bold cyan]1)[/bold cyan] Set cookie      "
                            f"[bold cyan]2)[/bold cyan] Clear cookie\n"
                            f"  [bold cyan]3)[/bold cyan] Thumbnail size  "
                            f"[bold cyan]4)[/bold cyan] Open downloads folder\n"
                            f"  [bold cyan]0)[/bold cyan] Back",
                            title="⚙ Settings", border_style="cyan"))
        c = input("\n➜  ").strip()
        if c == "0":
            return
        if c == "1":
            console.print("[dim]Paste your .ROBLOSECURITY cookie (from browser DevTools → Cookies):[/dim]")
            val = input("➜  ").strip()
            if val:
                open(COOKIE_FILE, "w", encoding="utf-8").write(val)
                console.print("[green]✅ Cookie saved! Private & audio assets are now unlocked.[/green]")
        elif c == "2":
            try:
                os.remove(COOKIE_FILE)
                console.print("[yellow]Cookie cleared.[/yellow]")
            except OSError:
                console.print("[yellow]No cookie set.[/yellow]")
        elif c == "3":
            s = load_settings()
            cur = thumb_size()
            other = 720 if cur == 420 else 420
            s["thumb_size"] = other
            save_settings(s)
            console.print(f"[green]✅ Thumbnails now {other}px.[/green]")
        elif c == "4":
            os.makedirs(DOWNLOADS, exist_ok=True)
            os.startfile(DOWNLOADS) if os.name == "nt" else console.print(f"📁 {DOWNLOADS}")
        console.print()


def batch_mode():
    console.print("[dim]Paste many asset IDs or links, separated by commas/spaces (one line):[/dim]")
    raw = input("➜  ").strip()
    ids = extract_ids(raw)
    if not ids:
        console.print("[red]❌ No valid IDs found.[/red]")
        return
    console.print(f"[cyan]Found {len(ids)} asset(s).[/cyan]\n")
    for aid in ids:
        console.rule(f"Asset #{aid}")
        grab_one(aid, auto_dl=True)
    console.rule()
    console.print(f"[green]✅ Batch done — {len(ids)} asset(s) processed.[/green]")


def show_history():
    if not os.path.exists(HISTORY):
        console.print("[yellow]No history yet.[/yellow]")
        return
    hist = json.load(open(HISTORY, encoding="utf-8"))
    if not hist:
        console.print("[yellow]No history yet.[/yellow]")
        return
    t = Table(title="🕘 Recent lookups", header_style="bold magenta")
    t.add_column("#", width=4)
    t.add_column("ID", style="cyan")
    t.add_column("Name", style="white", overflow="fold")
    t.add_column("Type", style="yellow")
    for i, h in enumerate(hist[:20], 1):
        t.add_row(str(i), str(h["id"]), h.get("name", "?"), h.get("type", "?"))
    console.print(t)


def main_loop():
    while True:
        cookie = load_cookie()
        ck = "[green]🔓 unlocked[/green]" if cookie else "[yellow]🔒 locked[/yellow]"
        console.print(Panel(BANNER + "\n" + TAGLINE + f"\n[dim]Login: {ck}[/dim]", border_style="magenta"))
        console.print("  [bold cyan]1)[/bold cyan] Lookup / download   "
                      "[bold cyan]2)[/bold cyan] Batch mode   "
                      "[bold cyan]3)[/bold cyan] 📄 Import .txt file   "
                      "[bold cyan]4)[/bold cyan] 👤 Creator mode\n"
                      "  [bold cyan]5)[/bold cyan] 🔎 Search keyword   "
                      "[bold cyan]6)[/bold cyan] History   "
                      "[bold cyan]7)[/bold cyan] ⚙ Settings   "
                      "[bold cyan]8)[/bold cyan] Open folder   "
                      "[bold cyan]9)[/bold cyan] ℹ Help   "
                      "[bold cyan]0)[/bold cyan] Exit")
        choice = input("\n➜  ").strip()
        if choice == "0":
            console.print("[dim]Bye! — ADHI-HUB[/dim]")
            break
        if choice == "9":
            show_help()
            continue
        if choice == "8":
            os.makedirs(DOWNLOADS, exist_ok=True)
            os.startfile(DOWNLOADS) if os.name == "nt" else console.print(f"📁 {DOWNLOADS}")
            continue
        if choice == "7":
            settings_menu()
            continue
        if choice == "6":
            show_history()
            continue
        if choice == "5":
            search_assets()
            continue
        if choice == "4":
            creator_mode()
            continue
        if choice == "3":
            import_file()
            continue
        if choice == "2":
            batch_mode()
            continue

        console.print("[dim]Paste an asset ID (or roblox.com/catalog/... link):[/dim]")
        raw = input("➜  ").strip()
        ids = extract_ids(raw)
        if not ids:
            console.print("[red]❌ That doesn't look like an asset ID.[/red]")
            continue
        grab_one(ids[0])


def main():
    try:
        check_update()
        main_loop()
    except KeyboardInterrupt:
        console.print("\n[dim]Bye! — ADHI-HUB[/dim]")


if __name__ == "__main__":
    main()