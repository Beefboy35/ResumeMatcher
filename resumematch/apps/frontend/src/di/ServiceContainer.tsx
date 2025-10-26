import React, { createContext, useContext } from "react";
import { GraphQLLabelService, GraphQLMatchService } from "../infrastructure/graphql/clients";
import { RestUploadService } from "../infrastructure/rest/upload";
import { LabelServicePort, MatchServicePort, UploadServicePort } from "../core/types";

export type Services = {
  matchService: MatchServicePort;
  labelService: LabelServicePort;
  uploadService: UploadServicePort;
};

const ServiceContainerContext = createContext<Services | null>(null);

export function ServiceContainerProvider({ children }: { children: React.ReactNode }) {
  const services: Services = {
    matchService: new GraphQLMatchService(),
    labelService: new GraphQLLabelService(),
    uploadService: new RestUploadService(),
  };
  return (
    <ServiceContainerContext.Provider value={services}>{children}</ServiceContainerContext.Provider>
  );
}

export function useServices() {
  const ctx = useContext(ServiceContainerContext);
  if (!ctx) throw new Error("ServiceContainer not provided");
  return ctx;
}