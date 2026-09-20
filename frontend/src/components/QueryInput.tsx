interface QueryInputProps {
  question: string;
  loading: boolean;
  onQuestionChange: (value: string) => void;
  onSubmit: () => void;
}

export function QueryInput({
  question,
  loading,
  onQuestionChange,
  onSubmit,
}: QueryInputProps) {
  const handleSubmit = (
    event: React.FormEvent<HTMLFormElement>,
  ) => {
    event.preventDefault();

    if (!question.trim() || loading) {
      return;
    }

    onSubmit();
  };

  return (
    <form
      onSubmit={handleSubmit}
      className="w-full"
    >
      <div className="rounded-2xl border border-zinc-200 bg-white p-2 shadow-sm">
        <textarea
          value={question}
          onChange={(event) =>
            onQuestionChange(event.target.value)
          }
          placeholder="Postavite pitanje o zakonima Republike Srbije..."
          rows={4}
          maxLength={2000}
          disabled={loading}
          className="w-full resize-none rounded-xl border-0 bg-transparent px-4 py-3 text-base text-zinc-900 outline-none placeholder:text-zinc-400 disabled:cursor-not-allowed disabled:opacity-60"
        />

        <div className="flex items-center justify-between px-3 pb-2">
          <span className="text-xs text-zinc-400">
            {question.length}/2000
          </span>

          <button
            type="submit"
            disabled={!question.trim() || loading}
            className="rounded-xl bg-zinc-900 px-5 py-2.5 text-sm font-medium text-white transition hover:bg-zinc-700 disabled:cursor-not-allowed disabled:bg-zinc-300"
          >
            {loading ? "Istraživanje..." : "Postavi pitanje"}
          </button>
        </div>
      </div>
    </form>
  );
}