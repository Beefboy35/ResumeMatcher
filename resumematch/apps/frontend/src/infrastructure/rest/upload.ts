import { UploadServicePort } from "../../core/types";

const UPLOAD_URL = "/api/upload";

export class RestUploadService implements UploadServicePort {
  async uploadResume(file: File): Promise<{ candidateId: string }> {
    const form = new FormData();
    form.append("file", file);
    const res = await fetch(UPLOAD_URL, { method: "POST", body: form });
    const data = await res.json();
    return { candidateId: data.file_id };
  }
}