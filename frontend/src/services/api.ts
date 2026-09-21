import type {
  QueryRequest,
  QueryResponse,
} from "../types/api";

const API_URL = "http://localhost:8000/api/v1";

export async function askQuestion(
  question: string,
): Promise<QueryResponse> {
  const request: QueryRequest = {
    question,
  };

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
      // Ignore JSON parsing errors and use the default message
    }

    throw new Error(message);
  }

  return response.json();
}


interface StreamTokenEvent {
  type: "token";
  content: string;
}

interface StreamMetadataEvent {
  type: "metadata";
  citations: {
    law: string;
    article: string;
  }[];
  grounded: boolean;
}

interface StreamDoneEvent {
  type: "done";
}

type StreamEvent =
  | StreamTokenEvent
  | StreamMetadataEvent
  | StreamDoneEvent;


interface StreamCallbacks {
  onToken: (content: string) => void;
  onMetadata: (
    citations: StreamMetadataEvent["citations"],
    grounded: boolean,
  ) => void;
}


export async function streamQuestion(
  question: string,
  callbacks: StreamCallbacks,
): Promise<void> {
  const response = await fetch(
    `${API_URL}/query/stream`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        question,
      }),
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
      // Ignore JSON parsing errors and use the default message
    }

    throw new Error(message);
  }

  if (!response.body) {
    throw new Error(
      "Streaming is not supported by this browser.",
    );
  }

  const reader = response.body.getReader();

  const decoder = new TextDecoder();

  let buffer = "";

  try {
    while (true) {
      const {
        value,
        done,
      } = await reader.read();

      if (done) {
        break;
      }

      buffer += decoder.decode(
        value,
        {
          stream: true,
        },
      );

      const lines = buffer.split("\n");

      buffer = lines.pop() ?? "";

      for (const line of lines) {
        const trimmedLine = line.trim();

        if (!trimmedLine) {
          continue;
        }

        let event: StreamEvent;

        try {
          event = JSON.parse(
            trimmedLine,
          ) as StreamEvent;
        } catch {
          continue;
        }

        if (event.type === "token") {
          callbacks.onToken(
            event.content,
          );
        }

        if (event.type === "metadata") {
          callbacks.onMetadata(
            event.citations,
            event.grounded,
          );
        }

        if (event.type === "done") {
          return;
        }
      }
    }

    if (buffer.trim()) {
      try {
        const event = JSON.parse(
          buffer.trim(),
        ) as StreamEvent;

        if (event.type === "token") {
          callbacks.onToken(
            event.content,
          );
        }

        if (event.type === "metadata") {
          callbacks.onMetadata(
            event.citations,
            event.grounded,
          );
        }
      } catch {
        // Ignore any parsing errors for the remaining buffer
      }
    }
  } finally {
    reader.releaseLock();
  }
}