import LoginPanel from "./components/Login/Login";
import Register from "./components/Register/Register";  // Importing your Register component
import { Routes, Route } from "react-router-dom";

function App() {
  return (
    <Routes>
      <Route path="/login" element={<LoginPanel />} />
      <Route path="/register" element={<Register />} />  {/* New route for Register component */}
    </Routes>
  );
}

export default App;
