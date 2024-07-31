import React from 'react';
import './Home.css';
import AddDocument from '../../components/AddDocument';
import MetricsContainer from '../../components/MetricsContainer/index';
import OutputContainer from '../../components/OutputContainer/index';
import SampleDocumentList from '../../components/SampleDocumentList';

const Home = () => {
  return (
    <>
     <SampleDocumentList/>
     <AddDocument/>
    </>
  );
};

export default Home;
