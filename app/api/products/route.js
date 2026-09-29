import { NextResponse } from 'next/server';
import { createClient } from '@supabase/supabase-js';

const MOCK_PRODUCTS = [
  {
    id: '1',
    name: 'Premium Dry Fruits Gift Box',
    description: 'Arhat Creation\'s finest selection — Mora Kaju, Khara Kaju, Badam, Pista, Akhrot, Kismiss, Jaldaru, Anjeer & Kadi Draksh. 100% natural, premium quality, perfect for gifting.',
    price: 899,
    original_price: 1199,
    stock: 25,
    category: 'Dry Fruits',
    image_url: '/dry-fruits.jpg',
    enhanced_image_url: '/dry-fruits.jpg',
    created_at: new Date().toISOString()
  },
  {
    id: '2',
    name: 'Jain Rose Chocolate Barfi',
    description: 'Made strictly following all the rules of Jainism. Creamy white chocolate barfi with dried rose petals. Pure, vegetarian, and crafted with care. 250g per pack.',
    price: 265,
    original_price: null,
    stock: 40,
    category: 'Sweets',
    image_url: '/rose-barfi.jpg',
    enhanced_image_url: '/rose-barfi.jpg',
    created_at: new Date().toISOString()
  },
  {
    id: '3',
    name: 'Mora Kaju (Cashews)',
    description: 'Premium whole cashews, hand-picked and fresh. Rich in healthy fats and protein. 200g resealable pouch.',
    price: 349,
    original_price: 449,
    stock: 60,
    category: 'Dry Fruits',
    image_url: null,
    enhanced_image_url: null,
    created_at: new Date().toISOString()
  },
  {
    id: '4',
    name: 'Badam (Almonds)',
    description: 'Natural whole almonds, rich in Vitamin E and antioxidants. Great for daily nutrition. 200g resealable pouch.',
    price: 299,
    original_price: 399,
    stock: 5,
    category: 'Dry Fruits',
    image_url: null,
    enhanced_image_url: null,
    created_at: new Date().toISOString()
  },
  {
    id: '5',
    name: 'Pista (Pistachios)',
    description: 'Premium Iranian pistachios with a rich, buttery flavour. High in protein and fibre. 150g resealable pouch.',
    price: 499,
    original_price: null,
    stock: 0,
    category: 'Dry Fruits',
    image_url: null,
    enhanced_image_url: null,
    created_at: new Date().toISOString()
  }
];

function getSupabaseAdmin() {
  const url = process.env.NEXT_PUBLIC_SUPABASE_URL;
  const key = process.env.SUPABASE_SERVICE_ROLE_KEY;
  if (!url || !key || url === 'your_supabase_project_url') return null;
  return createClient(url, key, {
    auth: { autoRefreshToken: false, persistSession: false }
  });
}

export async function GET() {
  const supabase = getSupabaseAdmin();
  if (!supabase) {
    return NextResponse.json({ products: MOCK_PRODUCTS, isMock: true });
  }
  try {
    const { data, error } = await supabase
      .from('products')
      .select('*')
      .order('created_at', { ascending: false });
    if (error) throw error;
    return NextResponse.json({ products: data || [] });
  } catch (err) {
    console.error('GET /api/products error:', err);
    return NextResponse.json({ products: MOCK_PRODUCTS, isMock: true, error: err.message });
  }
}

export async function POST(request) {
  const supabase = getSupabaseAdmin();
  if (!supabase) {
    return NextResponse.json({ error: 'Supabase not configured. Please update .env.local' }, { status: 503 });
  }
  try {
    const body = await request.json();
    const { name, description, price, original_price, stock, category, image_url, enhanced_image_url } = body;
    if (!name || !price) {
      return NextResponse.json({ error: 'Name and price are required' }, { status: 400 });
    }
    const { data, error } = await supabase
      .from('products')
      .insert([{ name, description, price: parseFloat(price), original_price: original_price ? parseFloat(original_price) : null, stock: parseInt(stock) || 0, category, image_url, enhanced_image_url }])
      .select()
      .single();
    if (error) throw error;
    return NextResponse.json({ product: data });
  } catch (err) {
    return NextResponse.json({ error: err.message }, { status: 500 });
  }
}

export async function PUT(request) {
  const supabase = getSupabaseAdmin();
  if (!supabase) {
    return NextResponse.json({ error: 'Supabase not configured' }, { status: 503 });
  }
  try {
    const body = await request.json();
    const { id, ...updates } = body;
    if (!id) return NextResponse.json({ error: 'ID required' }, { status: 400 });
    if (updates.price) updates.price = parseFloat(updates.price);
    if (updates.original_price) updates.original_price = parseFloat(updates.original_price);
    if (updates.stock !== undefined) updates.stock = parseInt(updates.stock);
    const { data, error } = await supabase
      .from('products')
      .update(updates)
      .eq('id', id)
      .select()
      .single();
    if (error) throw error;
    return NextResponse.json({ product: data });
  } catch (err) {
    return NextResponse.json({ error: err.message }, { status: 500 });
  }
}

export async function DELETE(request) {
  const supabase = getSupabaseAdmin();
  if (!supabase) {
    return NextResponse.json({ error: 'Supabase not configured' }, { status: 503 });
  }
  try {
    const { searchParams } = new URL(request.url);
    const id = searchParams.get('id');
    if (!id) return NextResponse.json({ error: 'ID required' }, { status: 400 });
    const { error } = await supabase.from('products').delete().eq('id', id);
    if (error) throw error;
    return NextResponse.json({ success: true });
  } catch (err) {
    return NextResponse.json({ error: err.message }, { status: 500 });
  }
}