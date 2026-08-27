import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import App from './App';
import { expect, test, describe, vi } from 'vitest';

// Mock chart.js so it doesn't try to render canvas in JSDOM
vi.mock('react-chartjs-2', () => ({
  Bar: () => <div data-testid="mock-bar-chart" />
}));

describe('FinOps Cost Dashboard', () => {
  test('renders loading state initially', () => {
    render(<App />);
    expect(screen.getByText('FinOps Cost Dashboard')).toBeInTheDocument();
    expect(screen.getByText('Loading cost metrics...')).toBeInTheDocument();
  });

  test('renders chart after data loads', async () => {
    render(<App />);
    await waitFor(() => {
      expect(screen.getByTestId('mock-bar-chart')).toBeInTheDocument();
    }, { timeout: 1000 });
  });
});
