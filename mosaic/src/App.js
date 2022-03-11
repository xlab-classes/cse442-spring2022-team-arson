import './App.css';
import menu from "./Component/menu.module.css";

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <div className={menu.Menu}></div>
        <div className={menu.Line1}></div>
        <div className={menu.Line2}></div>
        <div className={menu.Line3}></div>
        <div className={menu.Rectangle1}></div>
        <h className={menu.Home}></h>
        <div className={menu.Rectangle2}></div>
      </header>
    </div>
  );
}

export default App;
