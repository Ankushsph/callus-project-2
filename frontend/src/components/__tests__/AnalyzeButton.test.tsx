import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import { AnalyzeButton } from '../AnalyzeButton';

describe('AnalyzeButton', () => {
  it('renders with default text', () => {
    render(<AnalyzeButton onClick={() => {}} />);
    expect(screen.getByText('Analyze Essay')).toBeInTheDocument();
  });

  it('calls onClick when clicked', () => {
    const handleClick = vi.fn();
    render(<AnalyzeButton onClick={handleClick} />);
    
    const button = screen.getByRole('button');
    fireEvent.click(button);
    
    expect(handleClick).toHaveBeenCalledTimes(1);
  });

  it('shows loading text when loading', () => {
    render(<AnalyzeButton onClick={() => {}} loading={true} />);
    expect(screen.getByText('Analyzing...')).toBeInTheDocument();
  });

  it('is disabled when disabled prop is true', () => {
    render(<AnalyzeButton onClick={() => {}} disabled={true} />);
    const button = screen.getByRole('button');
    expect(button).toBeDisabled();
  });

  it('is disabled when loading', () => {
    render(<AnalyzeButton onClick={() => {}} loading={true} />);
    const button = screen.getByRole('button');
    expect(button).toBeDisabled();
  });

  it('does not call onClick when disabled', () => {
    const handleClick = vi.fn();
    render(<AnalyzeButton onClick={handleClick} disabled={true} />);
    
    const button = screen.getByRole('button');
    fireEvent.click(button);
    
    expect(handleClick).not.toHaveBeenCalled();
  });
});
