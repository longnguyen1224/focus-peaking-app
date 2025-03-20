import React, { useState } from "react";
import { Button } from "@/components/ui/button";

const App = () => {
  const [focusPeaking, setFocusPeaking] = useState(false);
  const [isPaused, setIsPaused] = useState(false);

  const videoSrc = focusPeaking ? "http://localhost:5000/video_feed" : "http://localhost:5000/video_original";

  const togglePause = async () => {
    try {
      await fetch("http://localhost:5000/toggle_pause", { method: "POST" });
      setIsPaused(!isPaused);
    } catch (error) {
      console.error("Error toggling pause:", error);
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-900 text-white">
      <h1 className="text-3xl font-bold mb-6">Focus Peaking Video App</h1>

      <div className="p-6 bg-white rounded-lg shadow-lg text-center">
        <h2 className="text-xl font-bold text-black mb-4">Live Video</h2>

        <div className="relative w-[800px] h-[450px] overflow-hidden rounded-lg cursor-pointer" onClick={togglePause}>
          <img src={videoSrc} alt="Focus Peaking Video" className="w-full h-full object-cover" />
        </div>

        <Button
          variant="default"
          className="mt-4 px-6 py-3 text-lg font-semibold bg-blue-600 hover:bg-blue-700 transition-opacity"
          onClick={() => setFocusPeaking(!focusPeaking)}
        >
          {focusPeaking ? "Disable Focus Peaking" : "Enable Focus Peaking"}
        </Button>
      </div>
    </div>
  );
};

export default App;
