from flask import Flask, render_template, request, jsonify
from chatbot import KenyanFashionChatbot
import os

app = Flask(__name__)
app.secret_key = 'fashionhub_kenya_2024'

# Initialize the chatbot
chatbot = KenyanFashionChatbot()

@app.route('/')
def home():
    """Render the main chat interface"""
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat_api():
    """API endpoint for chat messages"""
    try:
        data = request.get_json()
        user_message = data.get('message', '')
        user_context = data.get('context', {})
        
        if not user_message.strip():
            return jsonify({'error': 'Empty message'}), 400
            
        # Process message through chatbot
        response = chatbot.process_message(user_message, user_context)
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/products')
def get_products():
    """API endpoint to get product catalog"""
    return jsonify(chatbot.get_products())

@app.route('/api/conversation/history')
def get_conversation_history():
    """Get conversation history"""
    return jsonify(chatbot.get_conversation_history())

@app.route('/api/conversation/clear', methods=['POST'])
def clear_conversation():
    """Clear conversation history"""
    chatbot.clear_conversation()
    return jsonify({'message': 'Conversation cleared successfully'})

if __name__ == '__main__':
    print("🇰🇪 FashionHub Kenya Chatbot Starting...")
    print("📱 Visit: http://localhost:5000")
    print("🛍️ Ready to help customers with fashion needs!")
    
    # Create necessary directories if they don't exist
    os.makedirs('static/css', exist_ok=True)
    os.makedirs('static/js', exist_ok=True)
    os.makedirs('templates', exist_ok=True)
    
    app.run(debug=True, host='0.0.0.0', port=5000)