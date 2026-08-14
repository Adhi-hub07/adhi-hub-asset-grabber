const btn = document.getElementById("copy");
const status = document.getElementById("status");

async function grab() {
  try {
    const cookie = await chrome.cookies.get({
      name: ".ROBLOSECURITY",
      url: "https://www.roblox.com",
    });
    if (cookie && cookie.value) {
      await navigator.clipboard.writeText(cookie.value);
      status.textContent = "✅ Copied! Paste it in the app: Settings → Set cookie";
      status.style.color = "#9adf9a";
    } else {
      status.textContent = "❌ No cookie found — log in to roblox.com first";
      status.style.color = "#ff9e9e";
    }
  } catch (e) {
    status.textContent = "❌ Error: " + e.message;
    status.style.color = "#ff9e9e";
  }
}

btn.addEventListener("click", grab);
grab();