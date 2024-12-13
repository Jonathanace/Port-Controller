"use client"
import React, { createContext, useState, useContext, ReactNode, useEffect } from 'react';

interface HeaderContextProps {
  headerText: string;
  setHeaderText: (text: string) => void;
}

const HeaderContext = createContext<HeaderContextProps | undefined>(undefined);

export const useHeader = () => { 
  const context = useContext(HeaderContext); 
  if (!context) { 
    throw new Error("useHeader must be used within a HeaderProvider"); 
  } return context; 
}

export const HeaderProvider = ({ children }: { children: ReactNode }) => {
  const [headerText, setHeaderText] = useState<string>(() => {
    return localStorage.getItem('headerText') || 'DEFAULT HEADER TEXT';
  });

  const updateHeaderText = (text: string) => {
    setHeaderText(text);
    localStorage.setItem('headerText', text);
  };

  useEffect(() => {
    const storedHeaderText = localStorage.getItem('headerText');
    if (storedHeaderText) {
      setHeaderText(storedHeaderText);
    }
  }, []);

  return (
    <HeaderContext.Provider value={{ headerText, setHeaderText }}>
      {children}
    </HeaderContext.Provider>
  );
}