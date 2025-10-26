import { useCallback } from "react";
import { useServices } from "../di/ServiceContainer";

export function useLabelCandidate() {
  const { labelService } = useServices();

  const mark = useCallback(
    (vacancyId: string, candidateId: string, label: "pos" | "neg" | "later") =>
      labelService.label(vacancyId, candidateId, label),
    [labelService]
  );

  return { mark };
}