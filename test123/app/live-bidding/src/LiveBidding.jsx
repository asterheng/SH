import React, { useEffect, useState, useRef } from "react";
import axios from "axios";

const LiveBidding = () => {
  const [bids, setBids] = useState([]);
  const [newBid, setNewBid] = useState("");
  const ws = useRef(null);

  // Unique user identifier
  const user = useRef(`User_${Math.floor(Math.random() * 1000)}`);

  useEffect(() => {
    ws.current = new WebSocket("ws://localhost:5000");

    ws.current.onopen = () => console.log("WebSocket connected");

    ws.current.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.listingId === 1) {
        setBids(prevBids => [
          ...prevBids, 
          { ...data, timestamp: new Date().toLocaleTimeString() }
        ]);
      }
    };

    ws.current.onclose = () => console.log("WebSocket disconnected");

    return () => ws.current.close();
  }, []);

  const handlePlaceBid = async () => {
    try {
      const response = await axios.post("http://localhost:5000/bid/make", {
        listingId: 1,
        amount: parseFloat(newBid),
        bidder: user.current,
      });
      console.log(response.data.message);
    } catch (error) {
      console.error("Error placing bid:", error.response?.data?.message || error.message);
      alert("Error placing bid");
    }
  };

  return (
    <div style={{ textAlign: "center", marginTop: "20px" }}>
      <h1>Live Bidding for Listing 1</h1>
      {bids.length > 0 ? (
        <table style={{ margin: "20px auto", width: "90%" }}>
          <thead>
            <tr>
              <th>Timestamp</th>
              <th>Bid Amount</th>
              <th>Bidder</th>
            </tr>
          </thead>
          <tbody>
            {bids.map((bid, index) => (
              <tr key={index}>
                <td>{bid.timestamp}</td>
                <td>${bid.amount}</td>
                <td>{bid.bidder}</td>
              </tr>
            ))}
          </tbody>
        </table>
      ) : (
        <p>No bids yet.</p>
      )}
      <div>
        <input
          type="number"
          placeholder="Enter your bid"
          value={newBid}
          onChange={(e) => setNewBid(e.target.value)}
        />
        <button onClick={handlePlaceBid}>Place Bid</button>
      </div>
      <p>
        <strong>Your User:</strong> {user.current}
      </p>
    </div>
  );
};

export default LiveBidding;
