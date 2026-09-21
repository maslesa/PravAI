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
      <div className="rounded-2xl border-2 border-mytxt bg-mybg p-2 shadow-sm">
        <textarea
          value={question}
          onChange={(event) =>
            onQuestionChange(event.target.value)
          }
          placeholder="Postavite pitanje o zakonima Republike Srbije..."
          rows={4}
          maxLength={2000}
          disabled={loading}
          className="w-full resize-none rounded-xl border-0 bg-transparent px-4 py-3 text-base text-mytxt outline-none placeholder:text-mytxt/50 disabled:cursor-not-allowed disabled:opacity-60"
        />

        <div className="flex items-center justify-between px-3 pb-2">
          <span className="text-xs text-mytxt/50">
            {question.length}/2000
          </span>

          <button
            type="submit"
            disabled={!question.trim() || loading}
            className="rounded-xl bg-mytxt px-5 py-2.5 text-sm font-medium cursor-pointer text-mybg transition hover:opacity-80 duration-150 disabled:cursor-not-allowed disabled:bg-mytxt/50 disabled:text-mybg"
          >
            {loading ? "Istraživanje..." : "Postavi pitanje"}
          </button>
        </div>
      </div>
    </form>
  );
}