from django.core.management.base import BaseCommand
from store.models import Product


class Command(BaseCommand):
    help = 'Populate the database with sample products'

    def handle(self, *args, **options):
        # Sample products data
        products_data = [
            {
                'name': 'Logitech MX Master 3S',
                'brand': 'Logitech',
                'category': 'mouse',
                'price': '8999',
                'stock': 15,
                'description': 'Advanced wireless mouse with precision scrolling, ergonomic design, and multi-device support. Perfect for professionals who demand the best.',
            },
            {
                'name': 'Samsung 970 EVO Plus SSD',
                'brand': 'Samsung',
                'category': 'ssd',
                'price': '12999',
                'stock': 20,
                'description': 'High-performance NVMe SSD with 1050MB/s read speeds. Ideal for gaming, content creation, and system upgrades.',
            },
            {
                'name': 'Dell UltraSharp 27" Monitor',
                'brand': 'Dell',
                'category': 'monitor',
                'price': '34999',
                'stock': 8,
                'description': 'Stunning 4K IPS display with 100% sRGB color accuracy. Perfect for designers, photographers, and content creators.',
            },
            {
                'name': 'TP-Link AX6000 WiFi 6 Router',
                'brand': 'TP-Link',
                'category': 'router',
                'price': '15999',
                'stock': 12,
                'description': 'Next-generation WiFi 6 router with dual-band coverage and MU-MIMO technology. Experience lightning-fast connectivity.',
            },
            {
                'name': 'HyperX Cloud II Gaming Headset',
                'brand': 'HyperX',
                'category': 'headphone',
                'price': '6999',
                'stock': 25,
                'description': 'Professional-grade gaming headset with 7.1 surround sound, detachable mic, and comfortable memory foam.',
            },
            {
                'name': 'Logitech C920 HD Webcam',
                'brand': 'Logitech',
                'category': 'webcam',
                'price': '4999',
                'stock': 18,
                'description': 'Crystal-clear 1080p HD video for video calls and streaming. Auto-focus and built-in microphone for convenience.',
            },
            {
                'name': 'Corsair K95 Platinum XT Keyboard',
                'brand': 'Corsair',
                'category': 'keyboard',
                'price': '19999',
                'stock': 10,
                'description': 'Premium mechanical keyboard with Cherry MX switches, RGB lighting, and programmable macro keys.',
            },
            {
                'name': 'Razer DeathAdder V3 Mouse',
                'brand': 'Razer',
                'category': 'mouse',
                'price': '6999',
                'stock': 22,
                'description': 'Ultra-lightweight gaming mouse with 30000 DPI sensor and ultra-fast click response. Built for esports.',
            },
            {
                'name': 'WD Blue SN570 SSD 1TB',
                'brand': 'Western Digital',
                'category': 'ssd',
                'price': '8999',
                'stock': 30,
                'description': 'Reliable NVMe SSD with 3400MB/s read speeds. Great for everyday computing and gaming.',
            },
            {
                'name': 'ASUS VP28UQG 4K Gaming Monitor',
                'brand': 'ASUS',
                'category': 'monitor',
                'price': '34999',
                'stock': 6,
                'description': '4K UHD gaming monitor with 1ms response time and AMD FreeSync. Perfect for demanding games.',
            },
            {
                'name': 'TP-Link Archer AX1500 WiFi 6',
                'brand': 'TP-Link',
                'category': 'router',
                'price': '9999',
                'stock': 14,
                'description': 'Affordable WiFi 6 router with excellent coverage and performance for home use.',
            },
            {
                'name': 'SteelSeries Arctis Pro Headset',
                'brand': 'SteelSeries',
                'category': 'headphone',
                'price': '32999',
                'stock': 9,
                'description': 'Premium professional gaming headset with lossless audio and ultra-premium build quality.',
            },
            {
                'name': 'Razer Kiyo Webcam',
                'brand': 'Razer',
                'category': 'webcam',
                'price': '9999',
                'stock': 11,
                'description': '1080p webcam with built-in ring light for streaming. Perfect for content creators and streamers.',
            },
            {
                'name': 'Keychron K8 Wireless Keyboard',
                'brand': 'Keychron',
                'category': 'keyboard',
                'price': '8999',
                'stock': 17,
                'description': 'Compact mechanical keyboard with wireless connectivity and multi-device support.',
            },
            {
                'name': 'Logitech MX Anywhere 3S',
                'brand': 'Logitech',
                'category': 'mouse',
                'price': '7999',
                'stock': 19,
                'description': 'Compact wireless mouse with cross-computer workflow support and fast scrolling.',
            },
        ]

        created_count = 0
        for product_data in products_data:
            product, created = Product.objects.get_or_create(
                name=product_data['name'],
                defaults={
                    'brand': product_data['brand'],
                    'category': product_data['category'],
                    'price': product_data['price'],
                    'stock': product_data['stock'],
                    'description': product_data['description'],
                    'is_active': True,
                }
            )
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'Created: {product.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Already exists: {product.name}'))

        self.stdout.write(
            self.style.SUCCESS(f'✓ Successfully created {created_count} products!')
        )
