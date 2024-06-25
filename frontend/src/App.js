import './App.css';
import AddDocumentForm from './components/AddDocumentForm';
import OutputViewer from './components/OutputViewer';;

function App() {

  return (
    <div className="App">
      <header className="App-header">
       Eco Doc Sense
      </header>
      <div className="form-container">
        <AddDocumentForm/>
      </div>
      <div className="output-container">
        <OutputViewer/>
      </div>
    </div>
  );
}

export default App;
