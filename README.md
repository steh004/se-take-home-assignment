## FeedMe Software Engineer Take Home Assignment
Below is a take home assignment before the interview of the position. You are required to
1. Understand the situation and use case. You may contact the interviewer for further clarification.
2. Fork this repo and implement the requirement with your most familiar tools.
3. Complete the requirement and perform your own testing.
4. Provide documentation for the any part that you think is needed.
5. Commit into your own github and share your repo with the interviewer.
6. Bring the source code and functioning prototype to the interview session.

### Situation
McDonald is transforming their business during COVID-19. They wish to build the automated cooking bots to reduce workforce and increase their efficiency. As one of the software engineer in the project. You task is to create an order controller which handle the order control flow. 

### User Story
As below is part of the user story:
1. As McDonald's normal customer, after I submitted my order, I wish to see my order flow into "PENDING" area. After the cooking bot process my order, I want to see it flow into to "COMPLETE" area.
2. As McDonald's VIP member, after I submitted my order, I want my order being process first before all order by normal customer.  However if there's existing order from VIP member, my order should queue behind his/her order.
3. As McDonald's manager, I want to increase or decrease number of cooking bot available in my restaurant. When I increase a bot, it should immediately process any pending order. When I decrease a bot, the processing order should remain un-process.
4. As McDonald bot, it can only pickup and process 1 order at a time, each order required 10 seconds to complete process.

### Requirements
1. When "New Normal Order" clicked, a new order should show up "PENDING" Area.
2. When "New VIP Order" clicked, a new order should show up in "PENDING" Area. It should place in-front of all existing "Normal" order but behind of all existing "VIP" order.
3. The order number should be unique and increasing.
4. When "+ Bot" clicked, a bot should be created and start processing the order inside "PENDING" area. after 10 seconds picking up the order, the order should move to "COMPLETE" area. Then the bot should start processing another order if there is any left in "PENDING" area.
5. If there is no more order in the "PENDING" area, the bot should become IDLE until a new order come in.
6. When "- Bot" clicked, the newest bot should be destroyed. If the bot is processing an order, it should also stop the process. The order now back to "PENDING" and ready to process by other bot.
7. No data persistance is needed for this prototype, you may perform all the process inside memory.

### Functioning Prototype
You may demostrate your final funtioning prototype with **one and only one** of the following method:
- CLI application
- UI application
- E2E test case

### Tips on completing this task
- Testing, testing and testing. Make sure the prototype is functioning and meeting all the requirements.
- Do not over engineering. Try to scope your working hour within 3 hours (1 hour per day). You may document all the optimization or technology concern that you think good to bring in the solution.
- Complete the implementation as clean as possible, clean code is a strong plus point, do not bring in all the fancy tech stuff.

---

# 🛠️ SE Take-Home Assignment: MCBOT ORDER SYSTEM

This is a simple Flask + React.js application that simulates a bot-driven order processing system. Users can place VIP or Normal orders, and bots will process them based on priority.

---

## 📦 Requirements

Before starting, make sure you have **Python** and **Node.js** installed.
Ensure the following versions are installed

- Python 3.8 and above
- Node.js v16 and above


### Install Python Libraries
```bash
cd backend
pip install -r requirements.txt
```

### Install Frontend Dependencies
```bash
cd frontend
npm install
```

---

## 🚀 Running the App

### Step 1: Start Flask Backend
1. Ensure your directory is in the project directory
2. Then proceed to follow the commands below
```bash
cd backend
python app.py
```

### Step 2: Start React Frontend (in a new terminal)
1. Ensure your directory is in the project directory
2. Then proceed to follow the commands below
```bash
cd frontend
npm start
```

The frontend will open at: [http://localhost:3000](http://localhost:3000)

---

## 🧪 How to Use

Open your browser at [http://localhost:3000](http://localhost:3000)

Use the UI to:
- ➕ Place Normal or VIP orders
- 🤖 Add or remove bot workers
- 📊 Monitor real-time status of pending and completed orders

---

## ⚙️ How It Works

- Orders are stored in a `PriorityQueue` (`queue.PriorityQueue`)
- VIP = higher priority (`0`)
- Normal = lower priority (`1`)
- `BotThread` workers process orders in the background (`threading.Thread`)
- Completed orders are saved in a list
- React app polls `/status` to display current queue and bot statuses

---

## 🚀 Flask API Endpoints

### `POST /order`
- **Description:** Place a new order (VIP or Normal)
- **Request Body:**  
  ```json
  {
    "is_vip": true // or false
  }
  ```
- **Response:**  
  ```json
  {
    "order_id": 1,
    "is_vip": true
  }
  ```

---

### `POST /bot`
- **Description:** Add a new bot worker
- **Response:**  
  ```json
  {
    "bot_id": 1
  }
  ```

---

### `DELETE /bot`
- **Description:** Remove the most recently added bot
- **Response:**  
  ```json
  {
    "removed_bot_id": 1
  }
  ```
- **If no bots to remove:**  
  ```json
  {
    "error": "No bots to remove"
  }
  ```

---

### `GET /status`
- **Description:** Get the status of pending/completed orders and active bots
- **Response:**  
  ```json
  {
    "pending": ["VIP Order #2", "Normal Order #3"],
    "completed": ["Normal Order #1"],
    "bots": [
      { "bot_id": 1, "status": "VIP Order #2" },
      { "bot_id": 2, "status": "IDLE" }
    ]
  }
  ```

---