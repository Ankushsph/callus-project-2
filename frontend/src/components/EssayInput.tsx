/**
 * Essay input component - textarea for user to paste essay
 */

interface EssayInputProps {
  value: string;
  onChange: (value: string) => void;
  disabled?: boolean;
  placeholder?: string;
}

export function EssayInput({
  value,
  onChange,
  disabled = false,
  placeholder = "Paste your essay here...",
}: EssayInputProps) {
  const handleChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    onChange(e.target.value);
  };

  return (
    <div style={{ marginBottom: '1rem' }}>
      <label
        htmlFor="essay-input"
        style={{
          display: 'block',
          marginBottom: '0.5rem',
          fontSize: '1rem',
          fontWeight: '600',
          color: '#374151',
        }}
      >
        Essay Text
      </label>
      <textarea
        id="essay-input"
        value={value}
        onChange={handleChange}
        disabled={disabled}
        placeholder={placeholder}
        rows={12}
        style={{
          width: '100%',
          padding: '0.75rem',
          border: '1px solid #d1d5db',
          borderRadius: '0.375rem',
          fontSize: '0.95rem',
          fontFamily: 'inherit',
          lineHeight: '1.5',
          resize: 'vertical',
          backgroundColor: disabled ? '#f9fafb' : 'white',
          color: '#1f2937',
        }}
      />
      <div
        style={{
          marginTop: '0.25rem',
          fontSize: '0.875rem',
          color: '#6b7280',
        }}
      >
        {value.length} characters
      </div>
    </div>
  );
}
