"use client"

import React, { useEffect, useState } from "react";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { z } from "zod";
import { useRouter } from "next/navigation";


import { toast } from "@/hooks/use-toast";
import { Button } from "@/components/ui/button";
import {
  Form,
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { useHeader } from "@/context/HeaderContext";

// Define the form schema using Zod
const FormSchema = z.object({
  name: z.string().min(2, {
    message: "Name must be at least 2 characters.",
  }),
});

export const LogComment = (comment: string) => {
  fetch('http://localhost:5000/log-comment',
    {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({comment: comment})
    }
  )
}

export function InputForm({ onNameSubmit, setHeaderText, currentUser, setCurrentUser}: { onNameSubmit: (name: string) => void, setHeaderText: (text: string) => void, currentUser: string | null, setCurrentUser: (name: string | null) => void}) {
  const form = useForm<z.infer<typeof FormSchema>>({
    resolver: zodResolver(FormSchema),
    defaultValues: {
      name: "",
    },
  });
  const router = useRouter();

  function onSubmit(data: z.infer<typeof FormSchema>) {
    onNameSubmit(data.name);
    if (currentUser) {
      LogComment(`${currentUser} has logged out`)
    }
    
    setCurrentUser(data.name);
    setHeaderText(`Welcome, ${data.name}!`);  // This line updates the global header text
    toast({
      title: "You submitted the following values:",
      description: (
        <pre className="mt-2 w-[340px] rounded-md bg-slate-950 p-4">
          <code className="text-white">{JSON.stringify(data, null, 2)}</code>
        </pre>
      ),
    });
    LogComment(`${data.name} signs in.`)
    router.push('/func-select');
  }

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="w-2/3 space-y-6">
        <FormField
          control={form.control}
          name="name"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Your Name</FormLabel>
              <FormControl>
                <Input placeholder="Firstname Lastname" {...field} />
              </FormControl>
              <FormDescription>
                This is your full legal name as known to your employer.
              </FormDescription>
              <FormMessage />
            </FormItem>
          )}
        />
        <Button type="submit">Submit</Button>
      </form>
    </Form>
  );
}

export default function Page() {
  const { setHeaderText } = useHeader();
  const [submittedName, setSubmittedName] = useState<string | null>(null);
  const [currentUser, setCurrentUser] = useState<string | null>(null);

  useEffect(() => {
    setHeaderText('Welcome!');
  }, [setHeaderText]);

  return (
    <div className="grid grid-rows-[20px_1fr_20px] items-center justify-items-center min-h-screen p-8 pb-20 gap-16 sm:p-20 font-[family-name:var(--font-geist-sans)]">
      <div className="row-span-2 flex flex-col justify-center h-full">
        <h1 className="text-2xl font-bold mb-4">Login</h1>
        <InputForm 
        onNameSubmit={setSubmittedName} 
        setHeaderText={setHeaderText} 
        currentUser={currentUser} 
        setCurrentUser={setCurrentUser}
        />
        {submittedName && (
          <div className="mt-4 p-4 bg-blue-100 rounded-md">
            <h2 className="text-xl font-semibold">Submitted Name:</h2>
            <p>{submittedName}</p>
          </div>
        )}
      </div>
    </div>
  );
}
