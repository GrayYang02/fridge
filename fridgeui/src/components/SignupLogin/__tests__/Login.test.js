import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import Login from '../Login'; 
import api from '../../../api';
import { ACCESS_TOKEN, REFRESH_TOKEN } from '../../../constants';

jest.mock('../../../api', () => ({
  post: jest.fn(),
}));

const mockNavigate = jest.fn();
jest.mock('react-router-dom', () => {
  const originalModule = jest.requireActual('react-router-dom');
  return {
    ...originalModule,
    useNavigate: () => mockNavigate,
  };
});

beforeEach(() => {
  jest.spyOn(Storage.prototype, 'setItem');
});
afterEach(() => {
  Storage.prototype.setItem.mockRestore();
});

describe('Login component', () => {
  test('should call api.post and navigate to /profile on successful login', async () => {
    api.post.mockResolvedValue({
      data: {
        access: 'mock_access_token',
        refresh: 'mock_refresh_token',
      },
    });

    render(<Login />);

    await waitFor(() => expect(screen.getByLabelText(/email/i)).toBeInTheDocument());

    fireEvent.change(screen.getByLabelText(/email/i), {
      target: { value: 'test@example.com' },
    });
    fireEvent.change(screen.getByLabelText(/password/i), {
      target: { value: 'password123' },
    });

    fireEvent.click(screen.getByRole('button', { name: /log in/i }));

    await waitFor(() => {
      expect(api.post).toHaveBeenCalledWith('/core/token/', {
        email: 'test@example.com',
        password: 'password123',
      });

      expect(localStorage.setItem).toHaveBeenCalledWith(
        ACCESS_TOKEN,
        'mock_access_token'
      );
      expect(localStorage.setItem).toHaveBeenCalledWith(
        REFRESH_TOKEN,
        'mock_refresh_token'
      );

      expect(mockNavigate).toHaveBeenCalledWith('/profile');
    });
  });

  test('should show an alert on failed login', async () => {
    api.post.mockRejectedValue(new Error('Login failed'));
    const mockAlert = jest.spyOn(window, 'alert').mockImplementation(() => {});

    render(<Login />);

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
