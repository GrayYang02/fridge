import React from 'react';
import { render, screen, fireEvent, waitFor, act } from '@testing-library/react';
import Login from '../Login'; // Adjust path as needed
import api from '../../../api';
import { ACCESS_TOKEN } from '../../../constants';

// 1. Mock api.post
jest.mock('../../../api', () => ({
  post: jest.fn(),
}));

// 2. Mock useNavigate from react-router-dom
const mockNavigate = jest.fn();
jest.mock('react-router-dom', () => {
  const originalModule = jest.requireActual('react-router-dom');
  return {
    ...originalModule,
    useNavigate: () => mockNavigate,
  };
});

// 3. Mock localStorage (simulate Storage.prototype.setItem)
beforeEach(() => {
  jest.spyOn(Storage.prototype, 'setItem');
});
afterEach(() => {
  Storage.prototype.setItem.mockRestore();
});

describe('Login component', () => {
  test('should call api.post and navigate to /profile on successful login', async () => {
    // Mock backend response returning token
    api.post.mockResolvedValue({
      data: {
        access: 'mock_access_token',
        refresh: 'mock_refresh_token',
      },
    });

    render(<Login />);

    // **Wait for input fields to render**
    await waitFor(() => expect(screen.getByLabelText(/email/i)).toBeInTheDocument());

    // Fill out the form
    fireEvent.change(screen.getByLabelText(/email/i), {
      target: { value: 'test@example.com' },
    });
    fireEvent.change(screen.getByLabelText(/password/i), {
      target: { value: 'password123' },
    });

    // Click the login button
    fireEvent.click(screen.getByRole('button', { name: /log in/i }));

    // Wait for API call to complete
    await waitFor(() => {
      expect(api.post).toHaveBeenCalledWith('/core/token/', {
        email: 'test@example.com',
        password: 'password123',
      });

      // Check localStorage values
      expect(localStorage.setItem).toHaveBeenCalledWith(
        ACCESS_TOKEN,
        'mock_access_token'
      );
      expect(localStorage.setItem).toHaveBeenCalledWith(
        ACCESS_TOKEN,
        'mock_refresh_token'
      );

      // Ensure navigation occurs
      expect(mockNavigate).toHaveBeenCalledWith('/profile');
    });
  });

  test('should show an alert on failed login', async () => {
    api.post.mockRejectedValue(new Error('Login failed'));
    const mockAlert = jest.spyOn(window, 'alert').mockImplementation(() => {});

    render(<Login />);

    // **Wait for input fields to render**
    await waitFor(() => expect(screen.getByLabelText(/email/i)).toBeInTheDocument());

    fireEvent.change(screen.getByLabelText(/email/i), {
      target: { value: 'wrong@example.com' },
    });
    fireEvent.change(screen.getByLabelText(/password/i), {
      target: { value: 'wrongpassword' },
    });
    fireEvent.click(screen.getByRole('button', { name: /log in/i }));

    await waitFor(() => {
      expect(api.post).toHaveBeenCalled();
      expect(mockAlert).toHaveBeenCalledWith('Login Failed!');
    });

    mockAlert.mockRestore();
  });
});
