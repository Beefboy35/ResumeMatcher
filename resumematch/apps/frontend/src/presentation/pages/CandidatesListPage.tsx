import React from "react";
import { useMatchVacancy } from "../../application/useMatchVacancy";

export function CandidatesListPage({ vacancyId }: { vacancyId: string }) {
  const { items, loading } = useMatchVacancy(vacancyId);
  return (
    <div>
      <h2>Candidates</h2>
      {loading && <div>Loading...</div>}
      <table>
        <thead>
          <tr>
            <th>Name</th>
            <th>Location</th>
            <th>Score</th>
          </tr>
        </thead>
        <tbody>
          {items.map((c) => (
            <tr key={c.id}>
              <td>{c.fullName}</td>
              <td>{c.location}</td>
              <td>{c.score?.toFixed(3)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}