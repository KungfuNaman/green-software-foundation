import React from 'react';
import './Home.css';
import AddDocument from '../../components/AddDocument';
import MetricsContainer from '../../components/MetricsContainer/index';
import OutputContainer from '../../components/OutputContainer/index';
import SampleDocumentList from '../../components/SampleDocumentList';

const Home = () => {
  return (
    <>
     <h1 class="home-title">Eco Doc Sense</h1>
     <h2 class="home-description">Eco Doc Sense is an AI-powered tool that assesses the adherence of software designs, as described in design documents, to GSF-recognized green practices.</h2>
     <SampleDocumentList/>
     <AddDocument/>
    </>
  );
};

export default Home;
