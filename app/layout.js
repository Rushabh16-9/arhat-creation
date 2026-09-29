import './globals.css';

export const metadata = {
  title: 'Arhat Shop — Premium Products',
  description: 'Discover premium products with exceptional quality. Shop the latest collections with fast delivery.',
  keywords: 'shop, premium, products, ecommerce, delivery, dry fruits, sweets, arhat creation',
  openGraph: {
    title: 'Arhat Shop',
    description: 'Premium product shopping experience',
    type: 'website',
  },
};

export const viewport = {
  width: 'device-width',
  initialScale: 1,
};

export default function RootLayout({ children }) {
  return (
    <html lang="en" suppressHydrationWarning>
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <link
          href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800;900&family=Playfair+Display:ital,wght@0,600;1,600&display=swap"
          rel="stylesheet"
        />
      </head>
      <body suppressHydrationWarning>{children}</body>
    </html>
  );
}