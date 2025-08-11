import re
import random
import json
import datetime
from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple
import nltk
from textblob import TextBlob

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('punkt')
    nltk.download('stopwords')

@dataclass
class Message:
    """Data class for chat messages"""
    content: str
    sender: str  # 'user' or 'bot'
    timestamp: datetime.datetime
    language: str = 'en'

class KenyanFashionChatbot:
    """AI-powered chatbot for Kenyan clothing retail business"""
    
    def __init__(self):
        self.conversation_history: List[Message] = []
        self.user_context = {
            'name': None,
            'preferred_style': None,
            'size_preference': None,
            'location': None,
            'last_product_category': None
        }
        self.load_responses()
        self.load_product_data()
        self.size_guide = self.create_size_guide()
        
    def create_size_guide(self) -> Dict[str, Dict]:
        """Comprehensive size guide with measurements"""
        return {
            'women': {
                'dresses': {
                    'sizes': ['XS', 'S', 'M', 'L', 'XL', 'XXL'],
                    'measurements': {
                        'XS': {'bust': '30-32"', 'waist': '24-26"', 'hips': '34-36"'},
                        'S': {'bust': '32-34"', 'waist': '26-28"', 'hips': '36-38"'},
                        'M': {'bust': '34-36"', 'waist': '28-30"', 'hips': '38-40"'},
                        'L': {'bust': '36-38"', 'waist': '30-32"', 'hips': '40-42"'},
                        'XL': {'bust': '38-40"', 'waist': '32-34"', 'hips': '42-44"'},
                        'XXL': {'bust': '40-42"', 'waist': '34-36"', 'hips': '44-46"'}
                    },
                    'kenyan_sizes': {'XS': 8, 'S': 10, 'M': 12, 'L': 14, 'XL': 16, 'XXL': 18}
                },
                'tops': {
                    'sizes': ['XS', 'S', 'M', 'L', 'XL', 'XXL'],
                    'measurements': {
                        'XS': {'bust': '30-32"', 'waist': '24-26"'},
                        'S': {'bust': '32-34"', 'waist': '26-28"'},
                        'M': {'bust': '34-36"', 'waist': '28-30"'},
                        'L': {'bust': '36-38"', 'waist': '30-32"'},
                        'XL': {'bust': '38-40"', 'waist': '32-34"'},
                        'XXL': {'bust': '40-42"', 'waist': '34-36"'}
                    }
                }
            },
            'men': {
                'shirts': {
                    'sizes': ['XS', 'S', 'M', 'L', 'XL', 'XXL'],
                    'measurements': {
                        'XS': {'chest': '34-36"', 'waist': '28-30"', 'sleeve': '32"'},
                        'S': {'chest': '36-38"', 'waist': '30-32"', 'sleeve': '33"'},
                        'M': {'chest': '38-40"', 'waist': '32-34"', 'sleeve': '34"'},
                        'L': {'chest': '40-42"', 'waist': '34-36"', 'sleeve': '35"'},
                        'XL': {'chest': '42-44"', 'waist': '36-38"', 'sleeve': '36"'},
                        'XXL': {'chest': '44-46"', 'waist': '38-40"', 'sleeve': '37"'}
                    },
                    'kenyan_sizes': {'XS': 36, 'S': 38, 'M': 40, 'L': 42, 'XL': 44, 'XXL': 46}
                },
                'trousers': {
                    'sizes': [28, 30, 32, 34, 36, 38, 40],
                    'measurements': {
                        28: {'waist': '28"', 'inseam': '32"'},
                        30: {'waist': '30"', 'inseam': '32"'},
                        32: {'waist': '32"', 'inseam': '32"'},
                        34: {'waist': '34"', 'inseam': '32"'},
                        36: {'waist': '36"', 'inseam': '32"'},
                        38: {'waist': '38"', 'inseam': '32"'},
                        40: {'waist': '40"', 'inseam': '32"'}
                    }
                }
            },
            'general_tips': [
                "📏 How to measure: Use a soft tape measure over light clothing",
                "👕 For tops: Measure around the fullest part of your bust/chest",
                "👖 For bottoms: Measure natural waistline (above belly button)",
                "👗 Dresses: Measure bust, waist, and hips",
                "🔄 If between sizes: Size up for comfort, down for fitted look",
                "✂️ Free alterations available for all Nairobi store purchases"
            ]
        }
    
    def load_responses(self):
        """Load response patterns and templates"""
        self.responses = {
            'greetings': {
                'patterns': [
                    r'\b(hi|hello|hey|jambo|mambo|hallo|good morning|good afternoon|good evening)\b',
                    r'\b(habari|salamu|hujambo)\b'
                ],
                'responses': [
                    "Jambo! Karibu to FashionHub Kenya! 🇰🇪 How can I help you find the perfect outfit today?",
                    "Hello! Welcome to our fashion family. Ungependa nini leo? (What would you like today?)",
                    "Habari! Welcome to FashionHub Kenya. How may I assist you with your fashion needs?",
                    "Mambo vipi? Ready to explore our latest Kenyan fashion? What can I help you find?"
                ]
            },
        
            
            'payment': {
                'patterns': [
                    r'\b(mpesa|m-pesa|payment|pay|money|cost|price|lipa|malipo)\b',
                    r'\b(till|paybill|send money|how to pay)\b'
                ],
                'responses': [
                    "We accept multiple payment methods:\n\n💳 M-Pesa (Till: 789123)\n💰 Cash on Delivery (Nairobi only)\n🏦 Bank Transfer\n\nTo pay via M-Pesa:\n1. Go to Lipa na M-Pesa\n2. Buy Goods and Services\n3. Till: 789123\n4. Enter amount & PIN\n\nNeed help? Call 0700-123-456",
                    "Payment options:\n\n• M-Pesa: Instant confirmation (Till: 789123)\n• Cash on Delivery: +KSh 100 service fee\n• Bank: Co-op Bank 1234567890\n\nFree delivery for orders >KSh 5,000! Want me to explain any option?"
                ]
            },
            
            'traditional_wear': {
                'patterns': [
                    r'\b(kitenge|ankara|traditional|african|dashiki|kanga|cultural|nguo za kitamaduni)\b',
                    r'\b(wedding|harusi|office wear|kazini|sherehe)\b'
                ],
                'responses': [
                    "Our traditional collection is stunning! 🌍\n\n👗 Kitenge dresses: KSh 2,500 - 4,500\n👔 Ankara suits: KSh 4,000 - 7,000\n👘 Kanga sets: KSh 1,800 - 3,000\n\nWhat occasion are you shopping for? We have sizes 8-22 available.",
                    "Beautiful African prints available! ✨\n\n• Latest Kitenge designs\n• Custom Ankara outfits\n• Kanga accessories\n\nPerfect for weddings, cultural events, or office wear. Would you like size recommendations?"
                ]
            },
            
            'sizing': {
                'patterns': [
                    r'\b(size|fit|measurement|small|medium|large|xl|saizi|kipimo|ukubwa)\b',
                    r'\b(chest|bust|waist|hips|size guide|how to measure)\b'
                ],
                'responses': [
                    "Let me help with sizing! 📏 What type of clothing are you interested in? (dresses, shirts, trousers etc.)",
                    "I have a detailed size guide! Please tell me:\n1. Clothing type\n2. Your measurements\n3. Preferred fit\n\nOr ask 'How to measure' for instructions!"
                ]
            },
            
            'delivery': {
                'patterns': [
                    r'\b(delivery|shipping|transport|send|courier|peleka|utoaji)\b',
                    r'\b(nairobi|mombasa|kisumu|nakuru|upcountry|how long|delivery time)\b'
                ],
                'responses': [
                    "Delivery options: 🚚\n\n• Nairobi CBD: KSh 300 (2-4 hrs)\n• Nairobi Residential: KSh 400 (same day)\n• Major Towns: KSh 500 (2-3 days)\n• Upcountry: KSh 800 (3-5 days)\n\nFREE delivery for orders >KSh 5,000!",
                    "Our delivery network covers all Kenya:\n\n⚡ Express: Same day (Nairobi)\n🚐 Standard: 1-2 days (Major towns)\n🚛 Economy: 3-5 days (Countrywide)\n\nWhere should we deliver? I can give exact estimates!"
                ]
            },
            
            'products': {
                'patterns': [
                    r'\b(dress|shirt|trouser|suit|casual|formal|show me|what do you have|nguo)\b',
                    r'\b(blouse|skirt|jacket|jeans|tops|collection|styles|outfits)\b'
                ],
                'responses': [
                    "Our collections: 🛍️\n\n👗 Dresses: KSh 1,500 - 4,000\n👔 Suits: KSh 3,000 - 8,000\n👕 Casual wear: KSh 800 - 2,500\n🌍 Traditional: KSh 2,000 - 5,500\n👚 Office wear: KSh 1,200 - 3,500\n\nWhat style interests you?",
                    "Latest arrivals: ✨\n\n• New corporate collection\n• Wedding & event dresses\n• African print specials\n• Weekend casual range\n\nAll sizes 8-22 available. What would you like to see?"
                ]
            },
            
            'store_info': {
                'patterns': [
                    r'\b(location|address|where|contact|phone|hours|duka|mahali)\b',
                    r'\b(directions|map|find you|visit)\b'
                ],
                'responses': [
                    "Visit FashionHub Kenya: 📍\n\n🏢 Tom Mboya Street, Nairobi CBD\n📍 Near Kencom House (Blue Building)\n📞 0700-123-456\n💬 WhatsApp: 0700-123-456\n🕒 Mon-Sat: 8AM-7PM\n❌ Sunday: Closed",
                    "Find us easily! 🗺️\n\n📍 Tom Mboya Street, CBD\n🚌 Near Kencom Bus Stage\n🅿️ Free parking\n🚶 2 min from Kencom\n\nLook for the blue building with orange signage! Need directions?"
                ]
            },
            
            'thanks': {
                'patterns': [
                    r'\b(thanks|thank you|asante|shukrani|appreciate)\b',
                    r'\b(helpful|nice|good job|great)\b'
                ],
                'responses': [
                    "Asante sana! 😊 Happy to help! Anything else I can assist with?",
                    "Karibu! Always here for your fashion needs. What else can I do for you today?"
                ]
            }
        }
        
    def load_product_data(self):
        """Load product catalog data"""
        self.products = {
            'dresses': [
                {'name': 'Kitenge Office Dress', 'price': 2500, 'sizes': ['S', 'M', 'L'], 'colors': ['Blue', 'Green', 'Red'], 'category': 'traditional'},
                {'name': 'Ankara Evening Dress', 'price': 3500, 'sizes': ['M', 'L', 'XL'], 'colors': ['Multi', 'Gold', 'Purple'], 'category': 'traditional'},
                {'name': 'Casual Cotton Dress', 'price': 1500, 'sizes': ['XS', 'S', 'M'], 'colors': ['White', 'Black', 'Navy'], 'category': 'casual'}
            ],
            'suits': [
                {'name': 'Business Suit', 'price': 6000, 'sizes': ['M', 'L', 'XL'], 'colors': ['Navy', 'Charcoal', 'Black'], 'category': 'formal'},
                {'name': 'Ladies Blazer Set', 'price': 4500, 'sizes': ['S', 'M', 'L'], 'colors': ['Navy', 'Grey', 'Burgundy'], 'category': 'office'},
                {'name': 'Traditional Suit', 'price': 5500, 'sizes': ['M', 'L', 'XL'], 'colors': ['Kente', 'Ankara', 'Kitenge'], 'category': 'traditional'}
            ],
            'casual': [
                {'name': 'Cotton T-Shirt', 'price': 800, 'sizes': ['S', 'M', 'L'], 'colors': ['White', 'Black', 'Blue'], 'category': 'casual'},
                {'name': 'Designer Jeans', 'price': 2000, 'sizes': [30, 32, 34], 'colors': ['Blue', 'Black', 'Grey'], 'category': 'casual'},
                {'name': 'Casual Blouse', 'price': 1200, 'sizes': ['XS', 'S', 'M'], 'colors': ['Floral', 'Solid', 'Striped'], 'category': 'casual'}
            ]
        }
        
    def extract_sentiment(self, text: str) -> str:
        """Extract sentiment from user message"""
        try:
            blob = TextBlob(text)
            polarity = blob.sentiment.polarity
            return 'positive' if polarity > 0.1 else 'negative' if polarity < -0.1 else 'neutral'
        except:
            return 'neutral'
            
    def detect_language(self, text: str) -> str:
        """Enhanced language detection for English/Swahili"""
        swahili_keywords = ['jambo', 'mambo', 'habari', 'asante', 'karibu', 'sawa', 'nzuri', 'bei', 'nguo', 'duka', 'vipi']
        swahili_count = sum(1 for word in swahili_keywords if word in text.lower())
        return 'sw' if swahili_count >= 2 else 'en'
        
    def find_matching_pattern(self, user_input: str) -> Tuple[Optional[str], Optional[str]]:
        """Find matching response pattern with priority"""
        user_input_lower = user_input.lower()
        
        # Priority matching for specific intents
        for category in ['sizing', 'payment', 'delivery', 'thanks']:
            for pattern in self.responses[category]['patterns']:
                if re.search(pattern, user_input_lower):
                    return category, random.choice(self.responses[category]['responses'])
        
        # General category matching
        for category, data in self.responses.items():
            if category in ['sizing', 'payment', 'delivery', 'thanks']:
                continue  # Already checked
            for pattern in data['patterns']:
                if re.search(pattern, user_input_lower):
                    return category, random.choice(data['responses'])
                    
        return None, None
        
    def handle_size_query(self, user_input: str) -> str:
        """Handle detailed size requests"""
        # Detect clothing type from input
        clothing_types = {
            'dress': 'women_dresses',
            'shirt': 'men_shirts',
            'trouser': 'men_trousers',
            'blouse': 'women_tops',
            'skirt': 'women_tops',
            'suit': 'men_shirts'
        }
        
        # Try to detect clothing type
        detected_type = None
        for key, value in clothing_types.items():
            if re.search(r'\b' + key + r's?\b', user_input.lower()):
                detected_type = value
                break
        
        # Default to women's dresses if no type detected
        category = detected_type or 'women_dresses'
        gender, item = category.split('_')
        
        # Get size info
        size_info = self.size_guide[gender][item]
        response = f"📏 Size Guide for {item.replace('_', ' ').title()}:\n\n"
        
        # Build size table
        response += "Size | Measurements\n"
        response += "---- | ------------\n"
        for size, measurements in size_info['measurements'].items():
            meas_str = ', '.join([f"{k}: {v}" for k, v in measurements.items()])
            response += f"{size} | {meas_str}\n"
        
        # Add Kenyan size conversion if available
        if 'kenyan_sizes' in size_info:
            response += "\n🇰🇪 Kenyan Size Conversion:\n"
            for intl, kenyan in size_info['kenyan_sizes'].items():
                response += f"{intl} → Size {kenyan}\n"
        
        # Add general tips
        response += "\n📌 Tips:\n" + "\n".join(self.size_guide['general_tips'])
        response += "\n\nNeed help choosing? Share your measurements!"
        
        return response
        
    def generate_response(self, user_input: str, user_context: dict = None) -> str:
        """Generate context-aware response"""
        # Update context
        if user_context:
            self.user_context.update(user_context)
            
        # Check for size guide request
        if any(word in user_input.lower() for word in ['size guide', 'size chart', 'sizing help', 'measurement chart']):
            return self.handle_size_query(user_input)
            
        # Handle specific size questions
        if re.search(r'\b(size|fit|measurement)\b', user_input.lower()) and \
           any(word in user_input.lower() for word in ['dress', 'shirt', 'trouser', 'blouse', 'skirt']):
            return self.handle_size_query(user_input)
            
        # Find matching pattern
        category, response = self.find_matching_pattern(user_input)
        
        if response:
            # Personalization
            if self.user_context.get('name') and category == 'greetings':
                response = f"Jambo {self.user_context['name']}! " + response.split('!', 1)[1]
            
            # Add conversational follow-up
            follow_ups = {
                'products': "\n\nWould you like size recommendations for any item?",
                'traditional_wear': "\n\nShould I show you our best sellers?",
                'delivery': "\n\nWould you like to check delivery times for your area?"
            }
            response += follow_ups.get(category, "")
            
            return response
        
        # Default responses with conversation flow
        sentiment = self.extract_sentiment(user_input)
        
        if sentiment == 'negative':
            return "Pole! Let me help you better. Try asking about:\n- Product availability\n- Sizing help\n- Delivery options\n- Payment methods\nHow can I assist?"
        else:
            return random.choice([
                "Great question! I can help with:\n\n• Product info\n• Size guides\n• Payment options\n• Delivery details\n• Store location\n\nWhat would you like to know?",
                "I'd love to help! Try asking:\n\"Show me casual dresses\"\n\"What's your size guide?\"\n\"How do I pay via M-Pesa?\"\nWhat can I do for you?",
                "Karibu! I specialize in:\n\n🛍️ Product recommendations\n📏 Size assistance\n🚚 Delivery info\n💳 Payment help\n\nHow may I assist you today?"
            ])
                
    def add_message(self, content: str, sender: str, language: str = 'en'):
        """Add message to conversation history"""
        message = Message(
            content=content,
            sender=sender,
            timestamp=datetime.datetime.now(),
            language=language
        )
        self.conversation_history.append(message)
        
    def process_message(self, user_input: str, context: dict = None) -> dict:
        """Process user message and return response"""
        language = self.detect_language(user_input)
        self.add_message(user_input, 'user', language)
        
        bot_response = self.generate_response(user_input, context)
        self.add_message(bot_response, 'bot', 'en')
        
        return {
            'response': bot_response,
            'language': language,
            'timestamp': datetime.datetime.now().isoformat(),
            'conversation_stats': self.get_conversation_summary()
        }
        
    def get_products(self) -> dict:
        """Get product catalog"""
        return self.products
        
    def get_conversation_history(self) -> list:
        """Get conversation history"""
        return [{
            'content': msg.content,
            'sender': msg.sender,
            'timestamp': msg.timestamp.isoformat(),
            'language': msg.language
        } for msg in self.conversation_history[-20:]]
        
    def clear_conversation(self):
        """Clear conversation history"""
        self.conversation_history.clear()
        self.user_context.clear()
        
    def get_conversation_summary(self) -> dict:
        """Get conversation statistics"""
        total = len(self.conversation_history)
        user = sum(1 for msg in self.conversation_history if msg.sender == 'user')
        bot = sum(1 for msg in self.conversation_history if msg.sender == 'bot')
        
        return {
            'total_messages': total,
            'user_messages': user,
            'bot_messages': bot,
            'duration': (datetime.datetime.now() - self.conversation_history[0].timestamp).seconds if total else 0
        }

# Example usage
if __name__ == "__main__":
    bot = KenyanFashionChatbot()
    print(bot.process_message("Hello")['response'])
    print(bot.process_message("What's your size guide for dresses?")['response'])
    print(bot.process_message("How about shirts?")['response'])