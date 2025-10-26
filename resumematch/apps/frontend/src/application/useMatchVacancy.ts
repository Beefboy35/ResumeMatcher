import { useEffect, useState } from "react";
import { Candidate, MatchResult } from "../core/types";
import { useServices } from "../di/ServiceContainer";

export function useMatchVacancy(vacancyId: string) {
  const { matchService } = useServices();
  const [items, setItems] = useState<Candidate[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    let mounted = true;
    setLoading(true);
    matchService
      .match(vacancyId)
      .then((res: MatchResult) => {
        if (mounted) setItems(res.items);
      })
      .finally(() => mounted && setLoading(false));
    return () => {
      mounted = false;
    };
  }, [vacancyId, matchService]);

  return { items, loading };
}