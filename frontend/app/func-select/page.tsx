"use client"

import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group"
import { Separator } from "@/components/ui/separator"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { HeaderProvider } from "@/context/HeaderContext";
import Header from "@/components/ui/Header"
import { Button } from "@/components/ui/button"
import { Progress } from "@/components/ui/progress"
import React, { useState } from 'react';
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from "@/components/ui/tooltip"
import Link from 'next/link'

interface ManifestUploadProps {
  onUpload: () => void;
}

export function ManifestUpload({ onUpload } : ManifestUploadProps) {
  const handleUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files) {
      const file = event.target.files[0]
      const formData = new FormData();  
      formData.append('file', file)
      const response = await fetch('http://localhost:5000/upload', {
        method: 'POST',
        body: formData
      });
    }
    onUpload();
  };

  return (
    <div className="grid w-full max-w-sm items-center gap-1.5">
      <Input id="manifest" type="file" onChange={handleUpload}/>
    </div>
  )
}

interface FuncSelectProps {
  selectedOperation: string;
  onSelect: (value: string) => void;
}

export function FuncSelect({ onSelect } : FuncSelectProps) {
  const [selectedOperation, setSelectedOperation] = useState<string>('default');

  const handleSelect = (value: string) => {
    setSelectedOperation(value);
    onSelect(value);
  }

  return (
    <RadioGroup onValueChange={handleSelect}>
      <div className="flex items-center space-x-2">
        <RadioGroupItem value="default" id="r1" />
        <Label htmlFor="r1">Balance Operation</Label>
      </div>
      <div className="flex items-center space-x-2">
        <RadioGroupItem value="comfortable" id="r2" />
        <Label htmlFor="r2">Load/Unload Operation</Label>
      </div>
    </RadioGroup>
  )
}

export default function Page() {
  const [funcSelected, setFuncSelected] = useState(false);
  const [manifestUploaded, setManifestUploaded] = useState(false);
  const [selectedOperation, setSelectedOperation] = useState<string>('default');

  const progress = (funcSelected ? 50 : 0) + (manifestUploaded ? 50 : 0)

  return (
    <> 
      <div className="grid grid-rows-[auto, 1fr, auto] justify-items-center min-h-screen p-10 pb-20 gap-4 sm:p-10 font-[family-name:var(--font-geist-sans)]">
        <span className="w-[400px]">
          <div className="mb-5">
            Progress ({progress / 50}/2)
            <Progress value={progress} />
          </div>
          <div className="mb-20">
            <Tabs defaultValue="select operation" className="w-[400px]">
              <TabsList>
                <TabsTrigger value="select operation">Select Operation</TabsTrigger>
                <TabsTrigger value="upload manifest">Upload Manifest</TabsTrigger>
              </TabsList>
              <TabsContent value="select operation">
                Select your desired operation.
                <div>
                  <FuncSelect selectedOperation={selectedOperation} onSelect={() => setFuncSelected(true)}/>
                </div>
              </TabsContent>
              <TabsContent value="upload manifest">
                Upload your manifest here.
                <ManifestUpload onUpload={() => setManifestUploaded(true)}/>
              </TabsContent>
            </Tabs>
          </div>

          <div className="flex justify-center"> 
            {progress == 100 ? (
              <Button asChild>
                <Link href="/plan">Continue</Link>
              </Button>
            ) : (
              <TooltipProvider>
                <Tooltip>
                  <TooltipTrigger asChild>
                    <Button disabled >Continue</Button>
                  </TooltipTrigger>
                  <TooltipContent>
                    Select an operation and upload a manifest to continue.
                  </TooltipContent>
                </Tooltip>
              </TooltipProvider>
            )}
            
          </div>
        </span>
      </div>
    </>
  );
}
