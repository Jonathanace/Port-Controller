"use client"

import React from 'react'
import { usePathname } from "next/navigation";
import { useHeader } from '@/context/HeaderContext'
import "@/app/globals.css"

const Header: React.FC = () => {
  const { headerText } = useHeader();
  const pathName = usePathname();

  return (
    <header className="w-full bg-gray-800 text-white p-4">
      <h1>{headerText}</h1>
      {pathName !== "/login" && (
        <i>Not you? <a href="/login" className="underline-on-hover">Click Here to Login</a></i>
      )}
    </header>
  );
}

export default Header