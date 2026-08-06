import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import { EssayInput } from '../EssayInput';

describe('EssayInput', () => {
  it('renders with placeholder', () => {
    render(<EssayInput value="" onChange={() => {}} />);
    expect(screen.getByPlaceholderText(/paste your essay here/i)).toBeInTheDocument();
  });

  it('displays current value', () => {
    render(<EssayInput value="Test essay" onChange={() => {}} />);
    const textarea = screen.getByRole('textbox');
    expect(textarea).toHaveValue('Test essay');
  });

  it('calls onChange when text changes', () => {
    const handleChange = vi.fn();
    render(<EssayInput value="" onChange={handleChange} />);
    
    const textarea = screen.getByRole('textbox');
    fireEvent.change(textarea, { target: { value: 'New text' } });
    
    expect(handleChange).toHaveBeenCalledWith('New text');
  });

  it('shows character count', () => {
    render(<EssayInput value="Hello" onChange={() => {}} />);
    expect(screen.getByText('5 characters')).toBeInTheDocument();
  });

  it('can be disabled', () => {
    render(<EssayInput value="" onChange={() => {}} disabled={true} />);
    const textarea = screen.getByRole('textbox');
    expect(textarea).toBeDisabled();
  });
});
