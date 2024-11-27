import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group"
import { Separator } from "@/components/ui/separator"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { HeaderProvider } from "@/context/HeaderContext";
import Header from "@/components/ui/Header"
import { Button } from "@/components/ui/button"
import { Progress } from "@/components/ui/progress"

export function ManifestUpload() {
  return (
    <div className="grid w-full max-w-sm items-center gap-1.5">
      {/* <Label htmlFor="Manifest">Upload Manifest</Label> */}
      <Input id="manifest" type="file" />
    </div>
  )
}

export function FuncSelect() {
  return (
    <RadioGroup>
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
  return (
    <> 
      <div className="grid grid-rows-[auto, 1fr, auto] justify-items-center min-h-screen p-10 pb-20 gap-4 sm:p-10 font-[family-name:var(--font-geist-sans)]">
        <span className="w-[400px]">
          <div className="mb-5">
            Progress
            <Progress value={50} />
          </div>
          
          <Tabs defaultValue="select operation" className="w-[400px]">
            <TabsList>
              <TabsTrigger value="select operation">Select Operation</TabsTrigger>
              <TabsTrigger value="upload manifest">Upload Manifest</TabsTrigger>
            </TabsList>
            <TabsContent value="select operation">
              Select your desired operation.
              <div className="mb-10">
                <FuncSelect />
              </div>
            </TabsContent>
            <TabsContent value="upload manifest">
              Upload your manifest here.
              <ManifestUpload />
            </TabsContent>
          </Tabs>
          <div className="flex justify-center"> 
            <Button variant="outline">Continue</Button>
          </div>
        </span>
      </div>
    </>
  );
}
