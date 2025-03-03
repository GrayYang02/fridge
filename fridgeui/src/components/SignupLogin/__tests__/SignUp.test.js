/**
 * @jest-environment jsdom
 */
import React from 'react';
import { render, screen, waitFor, act } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { MemoryRouter, Routes, Route } from 'react-router-dom';
import SignUp from '../SignUp';
import api from '../../../api';

// ✅ Mock useNavigate (Correct approach)
const mockNavigate = jest.fn();
jest.mock('react-router-dom', () => ({
  ...jest.requireActual('react-router-dom'),
  useNavigate: () => mockNavigate, // Directly return mock function
}));

// ✅ Mock API requests
jest.mock('../../../api', () => ({
  post: jest.fn()
}));

beforeEach(() => {
  jest.spyOn(window, 'alert').mockImplementation(() => {});
  jest.clearAllMocks(); // Clear all mocks
  mockNavigate.mockClear(); // Ensure navigate is cleared before each test
});

afterEach(() => {
  jest.restoreAllMocks();
});

// ✅ Ensure `MemoryRouter` provides `/signup` as the initial path
function renderWithRouter(ui) {
  return render(
    <MemoryRouter initialEntries={["/signup"]}>
      <Routes>
        <Route path="/signup" element={ui} />
        <Route path="/login" element={<p>Login Page</p>} />
      </Routes>
    </MemoryRouter>
  );
}

describe('SignUp Component Tests', () => {
  test('Render Test: Component should correctly display input fields and button', () => {
    renderWithRouter(<SignUp />);
    expect(screen.getByLabelText(/EMAIL/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/PASSWORD/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/USERNAME/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /sign up/i })).toBeInTheDocument();
  });

  test('Successful Registration Test: Should display success message and navigate to /login after form submission', async () => {
    api.post.mockResolvedValueOnce({ data: { message: 'ok' } });

    renderWithRouter(<SignUp />);

    await userEvent.type(screen.getByLabelText(/EMAIL/i), 'test@example.com');
    await userEvent.type(screen.getByLabelText(/USERNAME/i), 'testuser');
    await userEvent.type(screen.getByLabelText(/PASSWORD/i), 'password123');

    await act(async () => {
      await userEvent.click(screen.getByRole('button', { name: /sign up/i }));
    });

    await waitFor(() => {
      expect(window.alert).toHaveBeenCalledWith('Sign Up Successful!');
    });

    await waitFor(() => {
      expect(mockNavigate).toHaveBeenCalledWith('/login');
    });
  });

  test('Failed Registration Test: Should display failure message after form submission', async () => {
    api.post.mockRejectedValueOnce(new Error('Network Error'));

    renderWithRouter(<SignUp />);

    await userEvent.type(screen.getByLabelText(/EMAIL/i), 'test@example.com');
    await userEvent.type(screen.getByLabelText(/USERNAME/i), 'testuser');
    await userEvent.type(screen.getByLabelText(/PASSWORD/i), 'password123');

    await act(async () => {
      await userEvent.click(screen.getByRole('button', { name: /sign up/i }));
    });

    await waitFor(() => {
      expect(window.alert).toHaveBeenCalledWith('Sign Up Failed!');
    });
  });
});
