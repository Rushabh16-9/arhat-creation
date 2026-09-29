import re

with open('app/admin/page.js', 'r', encoding='utf-8') as f:
    js = f.read()

new_remove_bg = '''  async function runGeminiRemoveBg() {
    if (!imagePreview) {
      showToast("Please upload an image first", "error");
      return;
    }
    setGeminiLoading(true);
    setGeminiAction("bg");
    try {
      showToast("Processing... This may take a few seconds", "info");
      
      const base64 = getBase64FromPreview(imagePreview);
      const mime = imageFile?.type || "image/jpeg";
      
      const geminiPromise = fetch("/api/gemini", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ action: "removeBackground", imageBase64: base64 || "", mimeType: mime })
      }).then(r => r.json());

      const removeBgPromise = imglyRemoveBackground(imagePreview, {
        output: { format: 'image/png' }
      });

      const [geminiData, blob] = await Promise.all([geminiPromise, removeBgPromise]);
      
      const newUrl = URL.createObjectURL(blob);
      setImagePreview(newUrl);
      
      const newFile = new File([blob], 'transparent-image.png', { type: 'image/png' });
      setImageFile(newFile);

      if (geminiData.data?.recommendedBg) {
        setBgColor(geminiData.data.recommendedBg);
        showToast("True Background Removed & AI color applied!", "success");
      } else {
        showToast("Background successfully removed!", "success");
      }
    } catch (err) {
      console.error(err);
      showToast("Failed to remove background: " + err.message, "error");
    } finally {
      setGeminiLoading(false);
      setGeminiAction("");
    }
  }'''

# Replace the entire function using regex
js = re.sub(
    r'\s*async function runGeminiRemoveBg\(\) \{[\s\S]*?(?=\s*async function runGeminiEnhance)',
    '\n' + new_remove_bg + '\n\n',
    js
)

# Rename the button
js = js.replace('AI Suggest BG Color', 'AI Remove BG & Color')

with open('app/admin/page.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Function successfully injected!")
