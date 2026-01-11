import React, { useEffect, useState } from "react";
import "./App.css";
import Navbar from "./components/Navbar";
import Wallet from "./components/Wallet";

const backendUrl = process.env.REACT_APP_BACKEND_URL || "http://127.0.0.1:5000";

function App() {
  const [health, setHealth] = useState("checking...");
  const [metrics, setMetrics] = useState(null);

  useEffect(() => {
    fetch(`${backendUrl}/health`)
      .then((res) => res.json())
      .then((data) => setHealth(`chain=${data.chain_id}`))
      .catch(() => setHealth("unavailable"));
  }, []);

  const loadMetrics = async () => {
    const response = await fetch(`${backendUrl}/metrics`);
    const data = await response.json();
    setMetrics(data);
  };

  return (
    <div className="app">
      <Navbar />
      <header className="app-header">
        <h1>ACBF Demo DApp</h1>
        <p>Backend status: {health}</p>
      </header>
      <main>
        <section className="panel">
          <h2>Wallet</h2>
          <Wallet backendUrl={backendUrl} />
        </section>
        <section className="panel">
          <h2>Chain Metrics</h2>
          <button onClick={loadMetrics}>Refresh Metrics</button>
          {metrics ? (
            <ul>
              <li>Blocks: {metrics.block_count}</li>
              <li>Transactions: {metrics.transaction_count}</li>
              <li>Pending: {metrics.pending_transactions}</li>
              <li>Unique addresses: {metrics.unique_addresses}</li>
              <li>Total supply: {metrics.total_supply}</li>
            </ul>
          ) : (
            <p>No metrics loaded yet.</p>
          )}
        </section>
        <section className="panel">
          <h2>Getting Started</h2>
          <p>
            Use the wallet actions above to create an address and refresh its balance.
            You can also fund it using the backend API and see metrics update.
          </p>
        </section>
      </main>
    </div>
  );
}

export default App;
