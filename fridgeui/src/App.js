import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Profile from "./components/Profile/Profile";
import Fridge from "./components/Fridge/Fridge";  // ✅ 引入 Fridge 组件

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/profile" element={<Profile />} />
        <Route path="/fridge" element={<Fridge />} />  {/* ✅ 新增 Fridge 页面 */}
      </Routes>
    </Router>
  );
}

export default App;
