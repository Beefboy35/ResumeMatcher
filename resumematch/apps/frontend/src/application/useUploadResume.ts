import { useCallback, useState } from "react";
import { useServices } from "../di/ServiceContainer";

export function useUploadResume() {
  const { uploadService } = useServices();
  const [loading, setLoading] = useState(false);

  const upload = useCallback(
    async (file: File) => {
      setLoading(true);
      try {
        return await uploadService.uploadResume(file);
      } finally {
        setLoading(false);
      }
    },
    [uploadService]
  );

  return { upload, loading };
}