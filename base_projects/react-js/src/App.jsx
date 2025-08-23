import React from 'react';
import { Routes, Route } from "react-router"
import Header from './components/Header';
import ProductList from './components/ProductList';
import Footer from './components/Footer';

const App = () => {
    return (
        <>
            <Routes>
                <Route path="/" element={<Home />}/>
            </Routes>
        </>
    );
};

export default App;
