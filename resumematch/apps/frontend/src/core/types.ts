export type Candidate = {
  id: string;
  fullName: string;
  location: string;
  yearsExp: number;
  skills: string[];
  score?: number;
};

export type Vacancy = {
  id: string;
  title: string;
  jdText?: string;
};

export type MatchResult = {
  items: Candidate[];
  total: number;
  vacancyId: string;
};

export interface MatchServicePort {
  match(vacancyId: string, topK?: number): Promise<MatchResult>;
}

export interface LabelServicePort {
  label(vacancyId: string, candidateId: string, label: "pos" | "neg" | "later"): Promise<void>;
}

export interface UploadServicePort {
  uploadResume(file: File): Promise<{ candidateId: string }>;
}