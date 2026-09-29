-- =========================================================
-- ARHAT SHOP — SUPABASE PERMISSIONS FIX
-- Run this in your Supabase SQL Editor to fix permissions
-- =========================================================

-- 1. Drop existing policies if they exist
DROP POLICY IF EXISTS "Public can read products" ON products;
DROP POLICY IF EXISTS "Service role full access" ON products;

-- 2. Disable RLS temporarily to allow service role access
ALTER TABLE products DISABLE ROW LEVEL SECURITY;

-- 3. Grant full access to both authenticated and anon roles
GRANT ALL ON products TO anon;
GRANT ALL ON products TO authenticated;
GRANT ALL ON products TO service_role;

-- 4. Re-enable RLS with correct policies
ALTER TABLE products ENABLE ROW LEVEL SECURITY;

-- 5. Allow anyone to read (public store)
CREATE POLICY "Allow public read"
  ON products FOR SELECT
  TO anon, authenticated
  USING (true);

-- 6. Allow service_role full access (admin operations)
CREATE POLICY "Allow service_role all"
  ON products FOR ALL
  TO service_role
  USING (true)
  WITH CHECK (true);

-- 7. Fix storage permissions too
DROP POLICY IF EXISTS "Public image access" ON storage.objects;
DROP POLICY IF EXISTS "Service role upload" ON storage.objects;

CREATE POLICY "Public image read"
  ON storage.objects FOR SELECT
  TO public
  USING (bucket_id = 'product-images');

CREATE POLICY "Service role image upload"
  ON storage.objects FOR INSERT
  TO service_role
  WITH CHECK (bucket_id = 'product-images');

CREATE POLICY "Service role image delete"
  ON storage.objects FOR DELETE
  TO service_role
  USING (bucket_id = 'product-images');

-- Done! Permissions are now set correctly.
SELECT 'Permissions fixed successfully!' as status;
