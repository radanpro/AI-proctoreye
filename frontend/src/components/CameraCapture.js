import React, { useRef, useState } from "react";

const CameraCapture = ({ setCapturedImage }) => {
  const videoRef = useRef(null);
  const [isCameraActive, setIsCameraActive] = useState(false);
  const [capturedPhotoURL, setCapturedPhotoURL] = useState(null);

  const startCamera = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        video: true,
      });
      videoRef.current.srcObject = stream;
      setIsCameraActive(true);
      setCapturedPhotoURL(null);
    } catch (err) {
      alert("Camera access denied.");
    }
  };

  const takeSnapshot = () => {
    const video = videoRef.current;
    const canvas = document.createElement("canvas");
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    const context = canvas.getContext("2d");
    context.drawImage(video, 0, 0, canvas.width, canvas.height);
    canvas.toBlob(
      (blob) => {
        // تحويل Blob إلى ملف (File) مع اسم وامتداد
        const file = new File([blob], "captured_image.jpg", {
          type: "image/jpeg",
        });
        setCapturedPhotoURL(URL.createObjectURL(blob)); // عرض الصورة
        setCapturedImage(file); // إرسال الملف للأب
        stopCamera();
      },
      "image/jpeg",
      0.95
    );
  };

  const stopCamera = () => {
    if (videoRef.current && videoRef.current.srcObject) {
      const stream = videoRef.current.srcObject;
      stream.getTracks().forEach((track) => track.stop());
      setIsCameraActive(false);
    }
  };

  return (
    <div className="w-full mt-4">
      {!capturedPhotoURL && (
        <div className="relative w-full aspect-video bg-gray-200 rounded-md">
          <video
            ref={videoRef}
            autoPlay
            className="w-full h-full object-cover rounded-md"
          />
        </div>
      )}

      {capturedPhotoURL && (
        <div className="relative w-full aspect-video bg-gray-200 rounded-md">
          <img
            src={capturedPhotoURL}
            alt="Captured"
            className="w-full h-full object-cover rounded-md"
          />
        </div>
      )}

      {!isCameraActive && !capturedPhotoURL && (
        <button
          type="button"
          onClick={startCamera}
          className="w-full mt-2 p-2 bg-green-500 text-white rounded"
        >
          Start Camera
        </button>
      )}

      {isCameraActive && !capturedPhotoURL && (
        <button
          type="button"
          onClick={takeSnapshot}
          className="w-full mt-2 p-2 bg-red-500 text-white rounded"
        >
          Capture Image
        </button>
      )}

      {capturedPhotoURL && (
        <button
          type="button"
          onClick={() => setCapturedPhotoURL(null)}
          className="w-full mt-2 p-2 bg-blue-500 text-white rounded"
        >
          Retake
        </button>
      )}
    </div>
  );
};

export default CameraCapture;
