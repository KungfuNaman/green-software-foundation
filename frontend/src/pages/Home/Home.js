import React from 'react';
import './Home.css';
import AddDocument from '../../components/AddDocument';
import MetricsContainer from '../../components/MetricsContainer/index';
import OutputContainer from '../../components/OutputContainer/index';

const Home = () => {
  return (
    <>
     <AddDocument/>
     <OutputContainer/>
     <MetricsContainer/>
    </>
  );
};

export default Home;
