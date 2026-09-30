import { NextResponse } from 'next/server';
import { GoogleGenerativeAI } from '@google/generative-ai';

export async function POST(request) {
  const apiKey = process.env.GEMINI_API_KEY;
  if (!apiKey || apiKey === 'your_gemini_api_key') {
    return NextResponse.json({ error: 'Gemini API key not configured. Add GEMINI_API_KEY to .env.local' }, { status: 503 });
  }

  try {
    const body = await request.json();
    const { action, imageBase64, mimeType = 'image/jpeg', productName, productDescription } = body;

    const genAI = new GoogleGenerativeAI(apiKey);
    const model = genAI.getGenerativeModel({ model: 'gemini-3.8-flash' });

    if (action === 'enhance') {
      // Use Gemini to analyze and provide enhancement instructions, 
      // then re-generate an enhanced description of the product
      const imagePart = {
        inlineData: { data: imageBase64, mimeType }
      };

      const result = await model.generateContent([
        imagePart,
        `You are a professional product photographer and e-commerce expert. 
        Analyze this product image and provide:
        1. A compelling product name (if not already: "${productName}")
        2. A detailed product description (3-4 sentences, highlight key benefits)
        3. Suggested category
        4. Key selling points (3 bullet points)\n        5. A suggested CSS filter string to visually enhance the image (brightness, contrast, saturate)
        
        Respond in JSON format:
        {
          "suggestedName": "...",
          "description": "...",
          "category": "...",
          "sellingPoints": ["...", "...", "..."],
          "suggestedCssFilter": "e.g., contrast(1.1) saturate(1.2)"
        }`
      ]);

      const text = result.response.text();
      let parsed;
      try {
        const jsonMatch = text.match(/\{[\s\S]*\}/);
        parsed = jsonMatch ? JSON.parse(jsonMatch[0]) : { description: text };
      } catch {
        parsed = { description: text };
      }

      return NextResponse.json({ success: true, data: parsed, action: 'enhance' });
    }

    if (action === 'removeBackground') {
      // Use Gemini Vision to analyze and describe how to remove bg
      // Since Gemini doesn't do actual image manipulation via API in standard mode,
      // we'll use it to confirm the subject and return enhanced metadata
      const imagePart = {
        inlineData: { data: imageBase64, mimeType }
      };

      const result = await model.generateContent([
        imagePart,
        `Analyze this product image. 
        Describe the main product/subject in detail.
        Provide the optimal background color for this product on an e-commerce site.
        
        Respond in JSON:
        {
          "subject": "detailed description of the main product",
          "recommendedBg": "#hexcolor",
          "bgDescription": "why this background works",
          "productType": "category of product"
        }`
      ]);

      const text = result.response.text();
      let parsed;
      try {
        const jsonMatch = text.match(/\{[\s\S]*\}/);
        parsed = jsonMatch ? JSON.parse(jsonMatch[0]) : {};
      } catch {
        parsed = {};
      }

      return NextResponse.json({ 
        success: true, 
        data: parsed, 
        action: 'removeBackground',
        note: 'Background analysis complete. The image will be displayed with the recommended background color.'
      });
    }

    if (action === 'generate360Description') {
      const imagePart = {
        inlineData: { data: imageBase64, mimeType }
      };

      const result = await model.generateContent([
        imagePart,
        `You are a luxury product presenter. 
        Create an engaging 360-degree product presentation script for this product.
        Include: front view description, side profile, back/details, top view, and unique features.
        Keep it concise and compelling.
        
        Respond in JSON:
        {
          "frontView": "...",
          "sideProfile": "...",
          "backDetails": "...",  
          "topView": "...",
          "uniqueFeature": "...",
          "overallImpression": "..."
        }`
      ]);

      const text = result.response.text();
      let parsed;
      try {
        const jsonMatch = text.match(/\{[\s\S]*\}/);
        parsed = jsonMatch ? JSON.parse(jsonMatch[0]) : {};
      } catch {
        parsed = {};
      }

      return NextResponse.json({ success: true, data: parsed, action: 'generate360Description' });
    }

    if (action === 'analyzeInventory') {
      const { products, bills } = body;
      
      const prompt = `You are an expert retail inventory analyst and pricing strategist.

Here is the current product inventory:
${JSON.stringify(products, null, 2)}

Here is the order history (past bills):
${JSON.stringify(bills, null, 2)}

Analyze this data carefully and provide actionable business recommendations.
Consider:
- Which products sell fast (high demand) and need restocking
- Which products are slow-moving and overstocked
- Optimal pricing based on demand (increase price for high-demand, reduce for slow-movers)
- Products that are out of stock but were previously ordered (missed revenue)

Respond ONLY with valid JSON in this exact format:
{
  "summary": "2-3 sentence executive summary of inventory health",
  "restock": [
    {
      "productId": "...",
      "productName": "...",
      "currentStock": 0,
      "recommendedStock": 20,
      "currentPrice": 500,
      "recommendedPrice": 550,
      "reason": "Sold X units in past Y days, high demand",
      "urgency": "high"
    }
  ],
  "reduce": [
    {
      "productId": "...",
      "productName": "...",
      "currentStock": 50,
      "recommendedStock": 15,
      "currentPrice": 800,
      "recommendedPrice": 699,
      "reason": "Only sold X units, slow moving",
      "urgency": "low"
    }
  ],
  "outOfStockAlert": [
    {
      "productId": "...",
      "productName": "...",
      "orderedCount": 5,
      "reason": "Was ordered but currently out of stock"
    }
  ]
}`;

      const result = await model.generateContent([prompt]);
      const text = result.response.text();
      let parsed;
      try {
        const jsonMatch = text.match(/\{[\s\S]*\}/);
        parsed = jsonMatch ? JSON.parse(jsonMatch[0]) : { summary: text, restock: [], reduce: [], outOfStockAlert: [] };
      } catch {
        parsed = { summary: 'Could not parse analysis. Please try again.', restock: [], reduce: [], outOfStockAlert: [] };
      }

      return NextResponse.json({ success: true, data: parsed, action: 'analyzeInventory' });
    }

    return NextResponse.json({ error: 'Unknown action.' }, { status: 400 });

  } catch (err) {
    console.error('Gemini API error:', err);
    return NextResponse.json({ error: err.message || 'Gemini API error' }, { status: 500 });
  }
}
