import React, { useEffect, useState } from 'react';
import axios from "axios";
import { Menu, Spin } from 'antd';
import CurrencyCard from "./components/CurrencyCard.jsx"

const App = () => {
  const [currencies, setCurrencies] = useState([])
  const [currencyId, setCurrencyId] = useState(1)
  const [currencyData, setCurrencyData] = useState(null)

  const fetchCurrencies = () => {
    axios.get('http://127.0.0.1:8000/currencies/').then(r => {
      const currResponse = r.data
      const menuItems = [
        {
          key: 'g1',
          label: 'Currencies',
          type: 'group',
          children: currResponse.map(i => {
            return { label: i.name, key: i.id }
          })
        },
      ]
      setCurrencies(menuItems)
    })
  }

  const fetchCurrency = () => {
    axios.get(`http://127.0.0.1:8000/currencies/${currencyId}`).then(r => {
      setCurrencyData(r.data)
    })
  }

  useEffect(() => {
    fetchCurrencies()
  }, []);

  useEffect(() => {
    setCurrencyData(null)
    fetchCurrency()
  }, [currencyId]);

  const onClick = (e) => {
    setCurrencyId(e.key)
  };

  return (
    <div className="flex ">
      <Menu
        onClick={onClick}
        style={{
          width: 256,
        }}
        defaultSelectedKeys={['1']}
        defaultOpenKeys={['sub1']}
        mode="inline"
        items={currencies}
        className="h-screen overflow-scroll"
      />
      <div className="mx-auto my-auto">
        {currencyData ? <CurrencyCard currency={currencyData} /> : <Spin size="large" />}
      </div>
    </div>
  );
};

export default App
