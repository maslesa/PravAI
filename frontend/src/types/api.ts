export interface QueryRequest {
  question: string;
}

export interface Citation {
  law: string;
  article: string;
}

export interface QueryResponse {
  answer: string;
  citations: Citation[];
  grounded: boolean;
}