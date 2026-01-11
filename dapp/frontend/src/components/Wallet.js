import React, { useState } from "react";

function Wallet({ backendUrl }) {
  const [wallet, setWallet] = useState(null);
  const [balance, setBalance] = useState(0);
  const [status, setStatus] = useState("Idle");

  const createWallet = async () => {
    setStatus("Creating wallet...");
    const response = await fetch(`${backendUrl}/wallet`, { method: "POST" });
    const data = await response.json();
    setWallet(data);
    setStatus("Wallet created");
  };

  const refreshBalance = async () => {
    if (!wallet) return;
    const response = await fetch(`${backendUrl}/balance?address=${wallet.address}`);
    const data = await response.json();
    setBalance(data.balance);
    setStatus("Balance refreshed");
  };

  return (
    <div className="wallet">
      <button onClick={createWallet}>Create Wallet</button>
      {wallet && (
        <div className="wallet-details">
          <p>
            <strong>Address:</strong> {wallet.address}
          </p>
          <p>
            <strong>Secret:</strong> {wallet.secret}
          </p>
          <button onClick={refreshBalance}>Refresh Balance</button>
          <p>
            <strong>Balance:</strong> {balance}
          </p>
        </div>
      )}
      <p className="wallet-status">Status: {status}</p>
    </div>
  );
}

export default Wallet;
