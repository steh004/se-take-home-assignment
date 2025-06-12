from flask import Flask, request, jsonify
from flask_cors import CORS
import threading
import time
import queue
import itertools

app = Flask(__name__)
CORS(app)  # Enable CORS for React

# --- Order Structure and Shared State ---
class Order:
    def __init__(self, order_id, is_vip):
        self.order_id = order_id
        self.is_vip = is_vip

    def __str__(self):
        return f"{'VIP' if self.is_vip else 'Normal'} Order #{self.order_id}"

order_queue = queue.PriorityQueue()  # priority type queue
complete_orders = []
order_id_counter = itertools.count(1)  # auto-incrementing number generator
bots = []
bots_lock = threading.Lock()
order_lock = threading.Lock()  # protects complete_orders

# --- Bot Worker Thread ---
class BotThread(threading.Thread):
    def __init__(self, bot_id):
        super().__init__()
        self.bot_id = bot_id
        self.active = True
        self.current_order = None

    def run(self):
        while self.active:
            try:
                priority, order_id, order = order_queue.get(timeout=1)
                self.current_order = order
                time.sleep(10)  # Simulate processing time
                with order_lock:
                    if order not in complete_orders:
                        complete_orders.append(order)
                self.current_order = None
            except queue.Empty:
                time.sleep(1)

    def stop(self):
        self.active = False
        if self.current_order:
            with order_lock:
                if self.current_order not in complete_orders:
                    order_queue.put(
                        (0 if self.current_order.is_vip else 1,
                         self.current_order.order_id,
                         self.current_order)
                    )

def add_order(is_vip):
    order_id = next(order_id_counter)
    priority = 0 if is_vip else 1
    order = Order(order_id, is_vip)
    order_queue.put((priority, order_id, order))
    return order

def add_bot():
    with bots_lock:
        bot = BotThread(len(bots) + 1)
        bots.append(bot)
        bot.start()
        return bot.bot_id

def remove_bot():
    with bots_lock:
        if bots:
            bot = bots.pop()
            bot.stop()
            return bot.bot_id
        return None

# --- Flask API Routes ---
@app.route("/order", methods=["POST"])
def place_order():
    is_vip = request.json.get("is_vip", False)
    order = add_order(is_vip)
    return jsonify({"order_id": order.order_id, "is_vip": order.is_vip})

@app.route("/bot", methods=["POST"])
def add_bot_endpoint():
    bot_id = add_bot()
    return jsonify({"bot_id": bot_id})

@app.route("/bot", methods=["DELETE"])
def remove_bot_endpoint():
    bot_id = remove_bot()
    if bot_id:
        return jsonify({"removed_bot_id": bot_id})
    return jsonify({"error": "No bots to remove"}), 400

@app.route("/status")
def get_status():
    with order_lock:
        pending = [str(ord[2]) for ord in sorted(list(order_queue.queue))]
        completed = [str(ord) for ord in complete_orders]
    with bots_lock:
        bots_status = [
            {"bot_id": bot.bot_id, "status": str(bot.current_order) if bot.current_order else "IDLE"}
            for bot in bots
        ]
    return jsonify({"pending": pending, "completed": completed, "bots": bots_status})

if __name__ == "__main__":
    app.run(debug=True)
