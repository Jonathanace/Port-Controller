import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"

export function InputWithButton() {
  return (
    <div className="flex w-full max-w-sm items-center space-x-2">
      <Input type="name" placeholder="Enter Your Full Name" />
      <Button type="submit">Submit</Button>
    </div>
  )
}

export default function Page() {
    return <div className="grid grid-rows-[20px_1fr_20px] items-center justify-items-center min-h-screen p-8 pb-20 gap-16 sm:p-20 font-[family-name:var(--font-geist-sans)]">
      <div className="row-span-2 flex flex-col justify-center h-full">
        <h1 className="text-2xl font-bold mb-4">Login</h1>
        <InputWithButton />
      </div>
    </div>
  }