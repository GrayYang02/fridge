import { createContext, useState, useEffect } from "react";
import api from "../../../api"; 

export const UserContext = createContext();

export const UserProvider = ({ children }) => {
  const [userinfo, setUserinfo] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Fetch user info when the app loads
  useEffect(() => {
    const fetchUser = async () => {
      try {
        const response = await api.get("/core/profile/user-info/");
        if (response.status !== 200) throw new Error("Failed to fetch user");
        setUserinfo(response.data.data || response.data);
        // console.log("User info:", response.data.data);
      } catch (err) {
        setError(err.message);
      } finally {
        
        setLoading(false);
      }
    };

    fetchUser();
  }, []);

  return (
    <UserContext.Provider value={{ userinfo, setUserinfo, loading, error }}>
      {children}
    </UserContext.Provider>
  );
};
