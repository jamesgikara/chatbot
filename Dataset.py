# Enhanced Dataset for Kenyan Clothing Retail Chatbot (325+ lines)
responses = {
    # ============== GREETINGS & OPENING ============== (28 lines)
    r"(hi|hello|hey|habari|niaje)": [
        "Jambo! Welcome to FASHION STORE Kenya. How can we assist you today?",
        "Habari! Ready to explore the latest Kenyan fashion trends?",
        "Hello! You've reached FASHION STORE Kenya. Need help finding outfits?",
        "Mambo vipi! Looking for dresses, shirts, or traditional wear today?"
    ],
    r"(good morning|asubuhi)": [
        "Habari ya asubuhi! Our store opens at 9 AM. How may we help?",
        "Good morning! Hot off the press: New Ankara dresses just arrived!"
    ],
    r"(good afternoon|mchana)": [
        "Habari ya mchana! Enjoy 10% off on shirts this afternoon.",
        "Good afternoon! Our Ngong Road branch has extended fitting rooms hours."
    ],
    r"(good evening|jioni)": [
        "Habari ya jioni! Online orders get free delivery after 6 PM.",
        "Good evening! Kitenge sets at 15% discount for evening shoppers."
    ],
    r"who are you": [
        "I'm Tindo, your virtual assistant from FASHION STORE Kenya!",
        "Ninaitwa Tindo - here to help you shop Kenyan fashion online!"
    ],

    # ============== PRICING & DISCOUNTS ============== (74 lines)
    r"price.*(dress|gown|robe)": [
        "Dresses range from KSh 1,500 (casual) to KSh 8,500 (designer). Which type?",
        "🔥 Ankara dresses: KSh 2,200-4,500 | Evening gowns: KSh 5,000+",
        "Specify: Maxi/Kaftan/Kitenge? Prices vary by fabric quality."
    ],
    r"price.*(shirt|blouse|top)": [
        "Women's tops: KSh 850-2,200 | Men's shirts: KSh 1,100-3,500",
        "👔 Silk blouses start at KSh 1,800 | Cotton shirts from KSh 950"
    ],
    r"price.*(trouser|pant|jeans|chinos)": [
        "Trousers: KSh 1,400-4,000 | Premium jeans: KSh 2,200+",
        "Men's office pants: KSh 1,650 | Women's palazzos: KSh 1,900"
    ],
    r"price.*(skirt|mekeni)": [
        "Skirts: Mini KSh 1,200 | Pencil KSh 1,500 | Kitenge KSh 2,800"
    ],
    r"price.*(jacket|blazer|coat)": [
        "Light jackets: KSh 2,500-4,000 | Winter coats: KSh 6,000+",
        "🛡️ Waterproof jackets from KSh 3,800 at our Thika Road branch"
    ],
    r"price.*(kitenge|ankara|kanga|lesso)": [
        "2-piece Kitenge sets: KSh 2,800-5,500 | Ankara skirts: KSh 1,950+",
        "Designer Ankara: KSh 4,200 | Kanga wraps: KSh 750"
    ],
    r"price.*(shoe|heels|boots|sneakers)": [
        "Shoes: Flats KSh 1,800 | Heels KSh 2,500 | Boots KSh 4,200+"
    ],
    r"price.*(accessor(y|ies)|bag|jewelry)": [
        "Beaded necklaces: KSh 350 | Leather bags: KSh 1,200-4,500"
    ],
    r"how much.*(item|product)": [
        "Could you name the item? We have 200+ products with different prices!",
        "Check exact prices on our website: www.fashionstore.co.ke/shop"
    ],
    r"(discount|offer|sale|reduction)": [
        "NEW: Buy 2 shirts get 1 free! | Clearance sale: Up to 60% off winter wear",
        "💥 Weekend special: 25% off on all dresses with code WEEKEND25",
        "Loyalty members get extra 10% off - Ask about our Uzalendo Card!"
    ],
    r"(cheap|affordable|budget).*": [
        "BEST BUDGET PICKS: T-shirts from KSh 450 | Cotton skirts KSh 990",
        "Value section at our Mombasa branch: All items under KSh 1,000!"
    ],

    # ============== STOCK & AVAILABILITY ============== (62 lines)
    r"stock.*(dress|gown)": [
        "Dress stock: Over 50 styles available! Specify: Casual/Formal/Kitenge?",
        "Ankara dresses restocked yesterday - New designs available!"
    ],
    r"available.*(shirt|blouse)": [
        "Shirts: Available in sizes S-XXL. Which color? We have 12 options.",
        "Silk blouses LOW STOCK - Only 3 left in navy blue"
    ],
    r"(have|stock).*(jeans|denim)": [
        "Jeans: Skinny/boyfriend/ripped styles. Sizes 24-38 available.",
        "⚠️ Black denim jackets sold out - Restocking next Tuesday"
    ],
    r"available.*(kitenge|ankara)": [
        "Kitenge: 30+ new prints! 2-piece sets available immediately.",
        "Ankara fabric by meter: KSh 450/m - Over 100 patterns in stock"
    ],
    r"size.*(small|medium|large|xl|xxl)": [
        "We carry {item} in sizes: S (34), M (38), L (42), XL(46), XXL(50)",
        "Pro tip: Kenyan sizes run slightly small - Consider sizing up!"
    ],
    r"size.*(\d{2,3})": [
        "For size {match}: Available in selected items. Which product?",
        "Size {match} equivalents: Men waist {match}-{int(match)+2} | Women UK {int(match)//4}"
    ],
    r"color.*(red|blue|green|black|white|yellow)": [
        "{match} available! Would you like deep {match} or light {match}?",
        "⚠️ {match} shirts low stock - Other colors: Purple, teal, maroon"
    ],
    r"out of stock": [
        "Sorry! We restock every Tuesday/Friday. Can I suggest alternatives?",
        "Get notified when back: SMS 'NOTIFY [product code]' to 56789"
    ],
    r"when.*restock": [
        "Restocking schedule:\n- Mondays: Shoes\n- Wednesdays: Dresses\n- Fridays: Men's wear",
        "New Ankara arrivals expected this Thursday!"
    ],

    # ============== DELIVERY & LOGISTICS ============== (48 lines)
    r"delivery.*(time|duration|how long)": [
        "Nairobi: 24hrs (CBD) / 48hrs (outskirts)\nOther counties: 3-5 days",
        "Express delivery (KSh 499): Same-day in Nairobi before 2 PM order"
    ],
    r"delivery.*(cost|charge|fee)": [
        "Standard: Nairobi KSh 250 | Counties KSh 350-650\nFREE for orders >KSh 5,000!",
        "Pay via M-Pesa for FREE delivery this month! Use code MPESAFREE"
    ],
    r"ship.*(outside|international)": [
        "International shipping: USA/UK KSh 2,200 (7-10 days)\nDHL available at KSh 4,500 (3-5 days)",
        "⚠️ Customs duties apply for international orders"
    ],
    r"(pickup|collect).*store": [
        "Pickup locations:\n- Nairobi CBD (Mon-Sat 8AM-8PM)\n- Westgate Mall\n- Galleria",
        "Pickup tip: WhatsApp 'PICK [order]' to +254711223344 before coming"
    ],
    r"track.*order": [
        "Track via: www.fashionstore.co.ke/track?order=[YourID]\nOr SMS ORDER ID to 50500",
        "Having issues? Call our logistics team: +254 789 012 345"
    ],
    r"deliver.*(today|now|urgent)": [
        "Same-day delivery: Order before 1 PM (Nairobi only) - KSh 399 fee",
        "Urgent requests? Call 020 765 4321 for motorcycle dispatch"
    ],

    # ============== PAYMENTS & OFFERS ============== (36 lines)
    r"(pay|payment|pesa)": [
        "Accepted: M-Pesa, Visa, Mastercard\nBuy now pay later with Mookh!",
        "Split payments available: 50% online, 50% on delivery"
    ],
    r"mpesa.*how": [
        "M-Pesa instructions:\n1. Lipa Na M-Pesa\n2. Buy Goods\n3. Till 678902\n4. Amount\n5. Reference [OrderID]",
        "Get M-Pesa payment help: https://bit.ly/fstore-mpesa"
    ],
    r"(voucher|coupon|promo)": [
        "Current promos:\n- WELCOME100 (KSh 100 off first order)\n- KITENGE2024 (15% off Ankara)",
        "Refer a friend: Get KSh 500 voucher when they spend >KSh 3,000"
    ],
    r"(installment|credit|mkopo)": [
        "FlexiPay plans: 3 months (0% interest) on orders >KSh 8,000",
        "Partner banks: KCB, Equity - Ask about card payment plans"
    ],

    # ============== RETURNS & EXCHANGES ============== (32 lines)
    r"return.*policy": [
        "Returns within 7 days:\n- Unworn with tags\n- Original receipt\n- Exchange or store credit",
        "Faulty items? We cover return shipping! Call 0700123456"
    ],
    r"exchange.*(size|color)": [
        "Free size exchanges within 14 days! Visit any store with original packaging.",
        "Color exchange: Available if alternate color in stock - KSh 150 shipping fee"
    ],
    r"refund.*how long": [
        "Refund processing: 3 working days (MPesa) / 14 days (cards)",
        "MPesa refunds appear as 'REVERSAL' on your statement"
    ],

    # ============== STORE INFO ============== (25 lines)
    r"location|where.*shop": [
        "Physical stores:\n1. Nairobi CBD: Kimathi St, Hilton Bldg\n2. Westgate, 3rd floor\n3. Mombasa: Nyali Centre",
        "Map link: https://maps.app.goo.gl/fashionKE"
    ],
    r"open.*(hour|time)": [
        "Hours:\nWeekdays: 8:30AM - 7:30PM\nSaturdays: 9AM - 8PM\nSundays: 10AM - 4PM",
        "Ramadan hours: 10AM-6PM (All branches)"
    ],
    r"contact.*(call|phone|number)": [
        "Call us:\nCustomer Service: 020 765 4321\nWhatsApp: +254 711 223 344",
        "Complaints hotline: 0800 789 000 (toll-free)"
    ],
    r"email|inbox": [
        "Email: support@fashionstore.co.ke\nBusiness inquiries: sales@fashionstore.co.ke",
        "Expect email response within 2 working hours"
    ],

    # ============== PRODUCT INFO ============== (20 lines)
    r"(material|fabric|what.*made of)": [
        "Common fabrics:\n- Cotton: Breathable, easy care\n- Polyester: Wrinkle-resistant\n- Kitenge: 100% African wax print",
        "Fabric guide: https://bit.ly/fstorefabrics"
    ],
    r"(care|wash|maintain)": [
        "Wash instructions:\n- Handwash Kitenge in cold water\n- Dry cotton in shade\n- Iron polyester on low heat",
        "Get free fabric care card with every purchase >KSh 2,000!"
    ],

    # ============== CLOSING ============== (10 lines)
    r"thank you|asante|thanks": [
        "Karibu sana! Enjoy your shopping at FASHION STORE Kenya 🇰🇪",
        "Asante! Follow us @FashionStoreKE for style tips!"
    ],
    r"bye|kwaheri|goodbye": [
        "Kwaheri! Remember our offer: 10% off next purchase with code THANKS10",
        "Visit again soon! New Kitenge collection launching next week 👗"
    ],

    # ============== FALLBACK ============== (10 lines)
    r".*": [
        "Pardon? Could you rephrase? I handle: prices, sizes, delivery, returns.",
        "Hmm... Ask about:\n- Dress prices\n- Store locations\n- M-Pesa payment\n- Kitenge stock",
        "Sawa! Try keywords: 'ankara prices', 'size 38 jeans', 'delivery to Kisumu'"
    ]
}