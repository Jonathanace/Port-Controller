"use client"

import React from 'react'
import { useHeader } from '@/context/HeaderContext'

const Header: React.FC = () => {
  const { headerText } = useHeader();

  return (
    <header className="w-full bg-gray-800 text-white p-4">
      <h1>{headerText}</h1>
    </header>
  );
}

export default Header