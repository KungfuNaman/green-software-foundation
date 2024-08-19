import React from 'react';
import './Home.css';
import AddDocument from '../../components/AddDocument';
import MetricsContainer from '../../components/MetricsContainer/index';
import OutputContainer from '../../components/OutputContainer/index';
import SampleDocumentList from '../../components/SampleDocumentList';
import GSFLogo from '../../assets/GSFLogoAlternate.jpg';

const Home = () => {
  return (
    <>
     <h1 class="home-title">EcoDoc Sense</h1>
     <h2 class="home-description">EcoDoc Sense is an AI-powered tool that assesses the adherence of software designs, as described in design documents, to GSF-recognized green practices.</h2>
     <SampleDocumentList/>
     <AddDocument/>
     <div class="container">
        <div class = "container-header">
          <h2 class="concept-title">Our Green Practice Categories</h2>
          <img class="GSFLogo" src={GSFLogo} alt="GSF Logo"/>
        </div>
        <div class="concept-card">
            <h3>Resource Optimization</h3>
            <p>Maximizing the efficient use of resources to achieve the best performance and cost efficiency.</p>
        </div>
        <div class="concept-card">
            <h3>Data Efficiency</h3>
            <p>Enhancing the effectiveness of data storage, retrieval, and processing to minimize redundancy and maximize utility.</p>
        </div>
        <div class="concept-card">
            <h3>Performance Management</h3>
            <p>Monitoring and managing system performance to ensure optimal operation and user satisfaction.</p>
        </div>
        <div class="concept-card">
            <h3>Security</h3>
            <p>Implementing measures to protect systems and data from unauthorized access and cyber threats.</p>
        </div>
        <div class="concept-card">
            <h3>User Impact</h3>
            <p>Assessing and enhancing the effect of system changes and improvements on the end-users.</p>
        </div>
     </div>
    </>
  );
};

export default Home;
