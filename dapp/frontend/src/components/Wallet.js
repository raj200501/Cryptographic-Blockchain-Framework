import React, { useState } from 'react';
import Web3 from 'web3';

function Wallet() {
  const [account, setAccount] = useState('');
  const [balance, setBalance] = useState('');

  async function loadWeb3() {
    if (window.ethereum) {
      const web3 = new Web3(window.ethereum);
      const accounts = await window.ethereum.request({ method: 'eth_requestAccounts' });
      setAccount(accounts[0]);
      const balance = await web3.eth.getBalance(accounts[0]);
      setBalance(web3.utils.fromWei(balance, 'ether'));
    } else {
      alert('Please install MetaMask!');
    }
  }

  return (
    <div className="wallet">
      <button onClick={loadWeb3}>Connect Wallet</button>
      <p>Account: {account}</p>
      <p>Balance: {balance} ETH</p>
    </div>
  );
}

export default Wallet;
