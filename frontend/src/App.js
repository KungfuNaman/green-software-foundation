import './App.css';
import AddDocumentForm from './components/AddDocumentForm';
import OutputViewer from './components/OutputViewer';
import "@fontsource/nunito-sans";
import GSFLogo from './assets/GSFLogo.jpg';
import MetricTable from './components/MetricTable';

function App() {

  return (
    <div className="App">
      <header className="App-header">
       <img class="GSFLogo" src={GSFLogo} alt="GSF Logo"/>
       Eco Doc Sense
      </header>
      <h3 className='UploadTitle'>File Upload and Analysis Tool</h3> 
      <div className="form-container">
        <AddDocumentForm/>
      </div>
      <div className="output-container">
        <h4>Analysis Output</h4>
        <OutputViewer/>
      </div>
      <div className="metrics-container">
        <h4>Output Metrics</h4>
        <MetricTable/>
      </div>
      <footer className="App-footer">By the Eco Doc Sense team</footer>
    </div>
  );
}

export default App;
