import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group"


export function ManifestUpload() {
  return (
    <div className="grid w-full max-w-sm items-center gap-1.5">
      <Label htmlFor="Manifest">Upload Manifest</Label>
      <Input id="manifest" type="file" />
    </div>
  )
}

export function FuncSelect() {
  return (
    <RadioGroup defaultValue="comfortable">
      <div className="flex items-center space-x-2">
        <RadioGroupItem value="default" id="r1" />
        <Label htmlFor="r1">Balance Operation</Label>
      </div>
      <div className="flex items-center space-x-2">
        <RadioGroupItem value="comfortable" id="r2" />
        <Label htmlFor="r2">Load/ Unload</Label>
      </div>
    </RadioGroup>
  )
}


export default function Page() {
    return (
        <> 
        <div className="grid grid-rows-[20px_1fr_20px] items-center justify-items-center min-h-screen p-8 pb-20 gap-16 sm:p-20 font-[family-name:var(--font-geist-sans)]">
            <FuncSelect />
            <ManifestUpload />
        </div>
        </>
    )
  }