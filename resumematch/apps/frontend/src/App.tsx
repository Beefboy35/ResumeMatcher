import React from "react";
import { ServiceContainerProvider } from "./di/ServiceContainer";
import { CandidatesListPage } from "./presentation/pages/CandidatesListPage";
import { UploadPage } from "./presentation/pages/UploadPage";

export default function App() {
  return (
    <ServiceContainerProvider>
      <div style={{ display: "grid", gap: 16 }}>
        <UploadPage />
        <CandidatesListPage vacancyId="vac-1" />
      </div>
    </ServiceContainerProvider>
  );
}