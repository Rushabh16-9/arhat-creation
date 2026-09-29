-- =========================================================
-- ARHAT SHOP — SUPABASE SETUP
-- Run this in your Supabase SQL Editor
-- =========================================================

-- 1. Create products table
CREATE TABLE IF NOT EXISTS products (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  name TEXT NOT NULL,
  description TEXT,
  price DECIMAL(10,2) NOT NULL,
  original_price DECIMAL(10,2),
  stock INT DEFAULT 0 NOT NULL,
  category TEXT,
  image_url TEXT,
  enhanced_image_url TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 2. Enable Row Level Security
ALTER TABLE products ENABLE ROW LEVEL SECURITY;

-- 3. Allow public reads (users can see products)
CREATE POLICY "Public can read products"
  ON products FOR SELECT USING (true);

-- 4. Allow service role full access (admin)
CREATE POLICY "Service role full access"
  ON products FOR ALL USING (auth.role() = 'service_role');

-- 5. Create storage bucket for product images
INSERT INTO storage.buckets (id, name, public)
VALUES ('product-images', 'product-images', true)
ON CONFLICT (id) DO NOTHING;

-- 6. Storage policy: anyone can read public images
CREATE POLICY "Public image access"
  ON storage.objects FOR SELECT
  USING (bucket_id = 'product-images');

-- 7. Storage policy: service role can upload
CREATE POLICY "Service role upload"
  ON storage.objects FOR INSERT
  WITH CHECK (bucket_id = 'product-images');

-- 8. Auto-update updated_at
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER products_updated_at
  BEFORE UPDATE ON products
  FOR EACH ROW EXECUTE FUNCTION update_updated_at();

-- Done! Your database is ready.
