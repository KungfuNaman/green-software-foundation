import "./App.css";
import "@fontsource/nunito-sans";
import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import "./App.css";
import Header from "./components/common/Header/Header";
import Footer from "./components/common/Footer/Footer";
import Home from "./pages/Home/Home";
import Analysis from "./pages/Analysis/Analysis";

function App() {
  return (
    <Router>
      <div className="App">
        <Header />
        <div className="App-content">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/analysis" element={<Analysis />} />
          </Routes>
        </div>
        <Footer />
      </div>
    </Router>
  );
}

export default App;
