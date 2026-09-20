import type {
  QueryRequest,
  QueryResponse,
} from "../types/api";

const API_URL = "http://localhost:8000/api/v1";

export async function askQuestion(question: string): Promise<QueryResponse> {
  const request: QueryRequest = {question};

  const response = await fetch(
    `${API_URL}/query`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(request),
    },
  );

  if (!response.ok) {
    let message = "An error occurred.";

    try {
      const errorData = await response.json();

      if (typeof errorData.detail === "string") {
        message = errorData.detail;
      }
    } catch {
      // Keep the default error message.
    }

    throw new Error(message);
  }

  return response.json();
}