import React from "react";
import { ServiceContainerProvider } from "./di/ServiceContainer";
import { CandidatesListPage } from "./presentation/pages/CandidatesListPage";
import { UploadPage } from "./presentation/pages/UploadPage";

export default function App() {
  return (
    <ServiceContainerProvider>
      <div className="container">
        <UploadPage />
        <CandidatesListPage vacancyId="vac-1" />
      </div>
    </ServiceContainerProvider>
  );
}