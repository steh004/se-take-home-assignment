import React, { useEffect, useState } from "react";
import axios from "axios";
import './App.css';

const API_BASE = "http://localhost:5000";

function App() {

  // implement hook concept
  const [status, setStatus] = useState({ pending: [], completed: [], bots: [] });

  const fetchStatus = async () => {
    try {
      const res = await axios.get(`${API_BASE}/status`);
      setStatus(res.data);
    } catch (err) {
      console.error("Error fetching status:", err);
      alert("Failed to fetch status from server.");
    }
  };

  // get status every 3 second interval
  useEffect(() => {
    fetchStatus();
    const interval = setInterval(fetchStatus, 3000);
    return () => clearInterval(interval);
  }, []);

  const placeOrder = async (isVip) => {
    try {
      await axios.post(`${API_BASE}/order`, { is_vip: isVip });
      fetchStatus();
    } catch (err) {
      console.error("Error placing order:", err);
      alert("Failed to place order.");
    }
  };

  const addBot = async () => {
    try {
      await axios.post(`${API_BASE}/bot`);
      fetchStatus();
    } catch (err) {
      console.error("Error adding bot:", err);
      alert("Failed to add bot.");
    }
  };

  const removeBot = async () => {
    try {
      await axios.delete(`${API_BASE}/bot`);
      fetchStatus();
    } catch (err) {
      console.error("Error removing bot:", err);
      alert("No bots to remove or server error.");
    }
  };

  return (
    <div className="container">
      <h1>🍟 McBot Order System</h1>

      <div className="buttons">
        <button onClick={() => placeOrder(false)} className="button normal">New Normal Order</button>
        <button onClick={() => placeOrder(true)} className="button vip">New VIP Order</button>
        <button onClick={addBot} className="button add">+ Bot</button>
        <button onClick={removeBot} className="button remove">- Bot</button>
      </div>

      <div className="grid">
        <div className="panel">
          <h2>Pending Orders</h2>
          <ul>{status.pending.map((o, i) => <li key={i}>{o}</li>)}</ul>
        </div>
        <div className="panel">
          <h2>Completed Orders</h2>
          <ul>{status.completed.map((o, i) => <li key={i}>{o}</li>)}</ul>
        </div>
      </div>

      <div className="panel mt-6">
        <h2>Active Bots</h2>
        <ul>{status.bots.map(bot => <li key={bot.bot_id}>Bot {bot.bot_id}: {bot.status}</li>)}</ul>
      </div>
    </div>

  );
}

export default App;
