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
import React, { useEffect, useState } from 'react';
import { toast } from "@/hooks/use-toast";
import { useHeader } from "@/context/HeaderContext";
import { useRouter } from "next/navigation";
import { Textarea } from "@/components/ui/textarea"
import { Dialog, DialogTrigger, DialogContent, DialogHeader, DialogTitle, DialogDescription } from "@/components/ui/dialog"



import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from "@/components/ui/tooltip"

import Link from 'next/link'

import { zodResolver } from "@hookform/resolvers/zod"
import { useForm } from "react-hook-form"
import { z } from "zod"

import { Checkbox } from "@/components/ui/checkbox"
import {
  Form,
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form"


const FormSchema = z.object({
  items: z.array(z.string()).refine((value) => value.some((item) => item), {
    message: "You have to select at least one item.",
  }),
})

export function LoadUnloadManifest() {
  const router = useRouter();
  const [isDisabled, setIsDisabled] = useState(false);
  const [items, setItems] = useState<{ id: string; label: string }[]>([]);
  const [namesAndWeights, setNamesAndWeights] = useState('');
  const form = useForm<z.infer<typeof FormSchema>>({
    resolver: zodResolver(FormSchema),
    defaultValues: {
      items: [],
    },
  })

  useEffect(() => {
    const fetchItems = async () => {
      const response = await fetch('http://localhost:5000/get-containers');
      const containers = await response.json();
      setItems(containers);
    }
    fetchItems();
  }, []);

  function onSubmit(data: z.infer<typeof FormSchema>) {
    setIsDisabled(true);
    const payload = {
      ...data,
      namesAndWeights,
    };
    fetch('http://localhost:5000/load-unload-manifest', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(payload),
    }).then(response => {
      setIsDisabled(false);
      router.push('/plan')
  });
  }

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-8">
        <FormField
          control={form.control}
          name="items"
          render={() => (
            <FormItem>
              <div className="mb-4">
                <FormLabel className="text-base">Cargo Select</FormLabel>
                <FormDescription>
                  Select the containers you would like to offload.
                </FormDescription>
              </div>
              {items.map((item) => (
                <FormField
                  key={item.id}
                  control={form.control}
                  name="items"
                  render={({ field }) => {
                    return (
                      <FormItem
                        key={item.id}
                        className="flex flex-row items-start space-x-3 space-y-0"
                      >
                        <FormControl>
                          <Checkbox
                            checked={field.value?.includes(item.id)}
                            onCheckedChange={(checked) => {
                              return checked
                                ? field.onChange([...field.value, item.id])
                                : field.onChange(
                                    field.value?.filter(
                                      (value) => value !== item.id
                                    )
                                  )
                            }}
                          />
                        </FormControl>
                        <FormLabel className="font-normal">
                          {item.label}
                        </FormLabel>
                      </FormItem>
                    )
                  }}
                />
              ))}
              <FormMessage />
            </FormItem>
          )}
        />
        <Separator />
        <Label>
          <br />
          Enter the names and weights of the container to be loaded. <br />
          Separate the name and weight of a container with a dash. <br />
          Separate multiple containers with a comma.
        </Label>
        <Textarea
        placeholder="Cat-1000,Dog-750"
        value={namesAndWeights}
        onChange={(e) => setNamesAndWeights(e.target.value)}
        />
        <Button
        disabled={isDisabled}
        type="submit">
          {isDisabled ? 'Processing manifest. Please wait.' : 'Submit Manifest'}
        </Button>
      </form>
    </Form>
  )
}

interface ManifestUploadProps {
  onUpload: (shipName: string) => void;
}

interface ManifestDialogButtonProps { 
  operation: string; 
  shipName: string;
}

export function ManifestUpload({ onUpload }: ManifestUploadProps) {
  const handleUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files) {
      const file = event.target.files[0];
      const shipName = file.name;
      const formData = new FormData();
      formData.append('file', file)
      formData.append('shipName', shipName)
      const response = await fetch('http://localhost:5000/upload', {
        method: 'POST',
        body: formData
      })
      onUpload(shipName);      
    }
    
  };

  return (
    <div className="grid w-full max-w-sm items-center gap-1.5">
      <Input id="manifest" type="file" onChange={handleUpload} />
    </div>
  )
}

interface FuncSelectProps {
  selectedOperation: string;
  onSelect: (value: string) => void;
}

export function FuncSelect({ selectedOperation, onSelect }: FuncSelectProps) {
  const handleSelect = (value: string) => {
    onSelect(value);
  };

  return (
    <RadioGroup value={selectedOperation} onValueChange={handleSelect}>
      <div className="flex items-center space-x-2">
        <RadioGroupItem value="Balance" id="r1" />
        <Label htmlFor="r1">Balance Operation</Label>
      </div>
      <div className="flex items-center space-x-2">
        <RadioGroupItem value="Load/Unload" id="r2" />
        <Label htmlFor="r2">Load/Unload Operation</Label>
      </div>
    </RadioGroup>
  );
}



export const ManifestDialogButton: React.FC<ManifestDialogButtonProps> = ({ operation, shipName }) => {
  return (
    <Dialog>
      <DialogTrigger asChild>
        <Button>Continue</Button>
        {/* <Button onClick={() => ProcessManifest(operation)}>Continue</Button> */}
      </DialogTrigger>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>
            { operation === 'Balance' 
              ? `Balance Operation Selected for ${shipName.replace(/\.txt$/, "")}`
              : `Load/Unload Operation Selected for ${shipName.replace(/\.txt$/, "")}`
            }
          </DialogTitle>
          <DialogDescription>
          {operation === 'Load/Unload' ? (
              <LoadUnloadManifest />
          ) : (
            <BalanceManifest />
          )}
          </DialogDescription>
        </DialogHeader>
      </DialogContent>
    </Dialog>
  )
}

export const ProcessManifest = (operation: string) => {
  fetch('http://localhost:5000/process-manifest',
    {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ parse_option: operation })
    }
  )
}

export const BalanceManifest = () => {
  const router = useRouter();
  const [isDisabled, setIsDisabled] = useState(false);

  const handleBalanceManifest = () => {
    setIsDisabled(true);

  fetch('http://localhost:5000/balance-manifest',
    {
      method: 'POST'
    }).then(response => {
        setIsDisabled(false);
        router.push('/plan')
    });
  };
  return (
    <Button onClick={handleBalanceManifest} disabled={isDisabled}>
      {isDisabled ? 'Processing manifest. Please wait.' : 'Submit Manifest'}
    </Button>
  )
}

export default function Page() {
  const [funcSelected, setFuncSelected] = useState(false);
  const [manifestUploaded, setManifestUploaded] = useState(false);
  const [selectedOperation, setSelectedOperation] = useState<string>('default');
  const [shipName, setShipName] = useState<string>('');

  const select_progress = (funcSelected ? 50 : 0) + (manifestUploaded ? 50 : 0)

  return (
    <>
      <div className="grid grid-rows-[auto, 1fr, auto] justify-items-center min-h-screen p-10 pb-20 gap-4 sm:p-10 font-[family-name:var(--font-geist-sans)]">
        <span className="w-[400px]">
          <div className="mb-5">
            Progress ({select_progress / 50}/2)
            <Progress value={select_progress} />
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
                  <FuncSelect
                    selectedOperation={selectedOperation}
                    onSelect={(value) => {
                      setSelectedOperation(value);
                      setFuncSelected(true);
                    }}
                  />
                </div>
              </TabsContent>
              <TabsContent value="upload manifest">
                Upload your manifest here.
                <ManifestUpload onUpload={(name) => {
                  setManifestUploaded(true);
                  setShipName(name);
                 }} />
              </TabsContent>
            </Tabs>
          </div>

          <div className="flex justify-center">
            {select_progress == 100 ? (
              <ManifestDialogButton operation={selectedOperation} shipName={shipName} />
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