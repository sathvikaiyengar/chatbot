
import './App.css';
import InstructionSidePanel from './instructionSidePanel/instructionSidePanel';
import ChatbotResponse from './chatbotResponse/chatbotResponse';
import "./styles.css";


function App() {
  return (
    <div className="container">
      <InstructionSidePanel />
      <div className="main-panel">
        <ChatbotResponse />
      </div>
    </div>
  );
}

export default App;
