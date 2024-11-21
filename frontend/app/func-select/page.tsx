import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"

export function InputFile() {
  return (
    <div className="grid w-full max-w-sm items-center gap-1.5">
      <Label htmlFor="Manifest">Upload Manifest</Label>
      <Input id="manifest" type="file" />
    </div>
  )
}

export default function Page() {
    return (
        <> 
        

        <div className="grid grid-rows-[20px_1fr_20px] items-center justify-items-center min-h-screen p-8 pb-20 gap-16 sm:p-20 font-[family-name:var(--font-geist-sans)]">
            <InputFile />
        </div>
        </>
    )
  }