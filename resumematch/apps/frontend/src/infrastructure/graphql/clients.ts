import { Candidate, MatchResult } from "../../core/types";
import { MatchServicePort, LabelServicePort } from "../../core/types";

const GRAPHQL_URL = "/graphql";

function gql(query: string, variables?: Record<string, unknown>) {
  return fetch(GRAPHQL_URL, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ query, variables }),
  }).then((res) => res.json());
}

export class GraphQLMatchService implements MatchServicePort {
  async match(vacancyId: string, topK = 10): Promise<MatchResult> {
    const query = `query($vacancyId: String!, $topK: Int){
      match(vacancyId: $vacancyId, topK: $topK){ candidate_id score matched_skills missing_skills }
    }`;
    const data = await gql(query, { vacancyId, topK });
    const items: Candidate[] = (data.data?.match || []).map((m: any) => ({
      id: m.candidate_id,
      fullName: m.candidate_id,
      location: "",
      yearsExp: 0,
      skills: m.matched_skills,
      score: m.score,
    }));
    return { items, total: items.length, vacancyId };
  }
}

export class GraphQLLabelService implements LabelServicePort {
  async label(vacancyId: string, candidateId: string, label: "pos" | "neg" | "later"): Promise<void> {
    const mutation = `mutation($vacancyId: String!, $candidateId: String!, $label: String!){
      labelCandidate(vacancyId: $vacancyId, candidateId: $candidateId, label: $label)
    }`;
    await gql(mutation, { vacancyId, candidateId, label });
  }
}