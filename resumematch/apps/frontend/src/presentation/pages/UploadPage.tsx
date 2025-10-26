import React, { useState } from "react";
import { useUploadResume } from "../../application/useUploadResume";

export function UploadPage() {
  const { upload, loading } = useUploadResume();
  const [file, setFile] = useState<File | null>(null);

  return (
    <div>
      <h2>Upload Resume</h2>
      <input type="file" onChange={(e) => setFile(e.target.files?.[0] || null)} />
      <button disabled={!file || loading} onClick={() => file && upload(file)}>
        Upload
      </button>
    </div>
  );
}