import re

with open('app/admin/page.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Add the imgly import at the top
import_statement = "import imglyRemoveBackground from '@imgly/background-removal';\n"
if "imglyRemoveBackground" not in js:
    js = js.replace('"use client";', '"use client";\n' + import_statement)

# Update runGeminiRemoveBg to actually do background removal!
old_remove_bg = '''  async function runGeminiRemoveBg() {
    const base64 = getBase64FromPreview(imagePreview);
    if (!base64 && !imageUrl) {
      showToast("Please upload an image first", "error");
      return;
    }
    setGeminiLoading(true);
    setGeminiAction("bg");
    try {
      let b64 = base64;
      let mime = imageFile?.type || "image/jpeg";
      if (!b64 && imageUrl) {
        // Fetch from URL
        const resp = await fetch(/api/gemini, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ action: "removeBackground", imageBase64: "placeholder", mimeType: mime })
        });
        const d = await resp.json();
        if (d.error && d.error.includes("not configured")) {
          showToast("Add GEMINI_API_KEY to .env.local to use AI features", "info");
          return;
        }
      }
      const res = await fetch("/api/gemini", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ action: "removeBackground", imageBase64: b64 || "", mimeType: mime })
      });
      const data = await res.json();
      if (data.error) {
        showToast(data.error, "error");
        return;
      }
      if (data.data?.recommendedBg) {
        setBgColor(data.data.recommendedBg);
        showToast("o" Gemini AI suggested background color applied!", "success");
      } else {
        showToast("Gemini processed the image, but no background color was suggested", "info");
      }
    } catch (err) {
      showToast(err.message, "error");
    } finally {
      setGeminiLoading(false);
      setGeminiAction("");
    }
  }'''

new_remove_bg = '''  async function runGeminiRemoveBg() {
    if (!imagePreview) {
      showToast("Please upload an image first", "error");
      return;
    }
    setGeminiLoading(true);
    setGeminiAction("bg");
    try {
      showToast("Processing... This may take a few seconds", "info");
      
      // 1. Ask Gemini for optimal background color
      const base64 = getBase64FromPreview(imagePreview);
      const mime = imageFile?.type || "image/jpeg";
      
      const geminiPromise = fetch("/api/gemini", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ action: "removeBackground", imageBase64: base64 || "", mimeType: mime })
      }).then(r => r.json());

      // 2. Actually remove background locally using WebAssembly!
      const removeBgPromise = imglyRemoveBackground(imagePreview, {
        output: { format: 'image/png' }
      });

      const [geminiData, blob] = await Promise.all([geminiPromise, removeBgPromise]);
      
      // Apply the transparent PNG
      const newUrl = URL.createObjectURL(blob);
      setImagePreview(newUrl);
      
      // Create a file object from blob so it can be uploaded to supabase
      const newFile = new File([blob], 'transparent-image.png', { type: 'image/png' });
      setImageFile(newFile);

      if (geminiData.data?.recommendedBg) {
        setBgColor(geminiData.data.recommendedBg);
        showToast("? True Background Removed & AI color applied!", "success");
      } else {
        showToast("? Background successfully removed!", "success");
      }
    } catch (err) {
      console.error(err);
      showToast("Failed to remove background: " + err.message, "error");
    } finally {
      setGeminiLoading(false);
      setGeminiAction("");
    }
  }'''

js = js.replace(old_remove_bg, new_remove_bg)

# Ensure the button says "AI Background Color" again or "AI Remove BG & Color"
js = js.replace('AI Suggest BG Color', 'AI Remove BG & Color')

with open('app/admin/page.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Actual BG removal implemented!")
