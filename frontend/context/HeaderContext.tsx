"use client"
import React, { createContext, useState, useContext, ReactNode } from 'react';

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
  const [headerText, setHeaderText] = useState('default header text (not placeholder!)');

  return (
    <HeaderContext.Provider value={{ headerText, setHeaderText }}>
      {children}
    </HeaderContext.Provider>
  );
}
