/**
 * Analyze button component
 */

interface AnalyzeButtonProps {
  onClick: () => void;
  disabled?: boolean;
  loading?: boolean;
}

export function AnalyzeButton({
  onClick,
  disabled = false,
  loading = false,
}: AnalyzeButtonProps) {
  return (
    <button
      onClick={onClick}
      disabled={disabled || loading}
      style={{
        width: '100%',
        padding: '0.75rem 1.5rem',
        backgroundColor: disabled || loading ? '#9ca3af' : '#3b82f6',
        color: 'white',
        fontSize: '1rem',
        fontWeight: '600',
        border: 'none',
        borderRadius: '0.375rem',
        cursor: disabled || loading ? 'not-allowed' : 'pointer',
        transition: 'background-color 0.2s',
      }}
      onMouseEnter={(e) => {
        if (!disabled && !loading) {
          e.currentTarget.style.backgroundColor = '#2563eb';
        }
      }}
      onMouseLeave={(e) => {
        if (!disabled && !loading) {
          e.currentTarget.style.backgroundColor = '#3b82f6';
        }
      }}
    >
      {loading ? 'Analyzing...' : 'Analyze Essay'}
    </button>
  );
}
