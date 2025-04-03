import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { MemoryRouter, Routes, Route } from 'react-router-dom';
import Login from '../Login';
import api from '../../../api';
import { ACCESS_TOKEN, REFRESH_TOKEN } from '../../../constants';
import { jwtDecode } from 'jwt-decode';

jest.mock('../../../api', () => ({
  post: jest.fn(),
}));

jest.mock('jwt-decode', () => ({
  jwtDecode: jest.fn(),
}));

const mockNavigate = jest.fn();
jest.mock('react-router-dom', () => ({
  ...jest.requireActual('react-router-dom'),
  useNavigate: () => mockNavigate,
}));

beforeEach(() => {
  jest.spyOn(window, 'alert').mockImplementation(() => {});
  localStorage.clear();
  jest.clearAllMocks();
});

function renderWithRouter(ui) {
  return render(
    <MemoryRouter initialEntries={['/login']}>
      <Routes>
        <Route path="/login" element={ui} />
        <Route path="/profile" element={<div>Profile Page</div>} />
      </Routes>
    </MemoryRouter>
  );
}

describe('Login Component', () => {
  test('renders login form fields and button', () => {
    renderWithRouter(<Login />);
    expect(screen.getByLabelText(/EMAIL/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/PASSWORD/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /Log in/i })).toBeInTheDocument();
  });

  test('successful login stores tokens and redirects', async () => {
    const fakeToken = {
      access: 'fake-access-token',
      refresh: 'fake-refresh-token',
    };
    const fakeUserId = 123;

    api.post.mockResolvedValueOnce({ data: fakeToken });
    jwtDecode.mockReturnValueOnce({ user_id: fakeUserId });

    renderWithRouter(<Login />);

    await userEvent.type(screen.getByLabelText(/EMAIL/i), 'test@example.com');
    await userEvent.type(screen.getByLabelText(/PASSWORD/i), 'password123');
    await userEvent.click(screen.getByRole('button', { name: /Log in/i }));

    await waitFor(() => {
      expect(api.post).toHaveBeenCalledWith('/core/token/', {
        email: 'test@example.com',
        password: 'password123',
      });
      expect(localStorage.getItem(ACCESS_TOKEN)).toBe('fake-access-token');
      expect(localStorage.getItem(REFRESH_TOKEN)).toBe('fake-refresh-token');
      expect(localStorage.getItem('user_id')).toBe(fakeUserId.toString());
      expect(mockNavigate).toHaveBeenCalledWith('/profile');
    });
  });

  test('failed login shows alert', async () => {
    api.post.mockRejectedValueOnce(new Error('Invalid credentials'));

    renderWithRouter(<Login />);
    await userEvent.type(screen.getByLabelText(/EMAIL/i), 'wrong@example.com');
    await userEvent.type(screen.getByLabelText(/PASSWORD/i), 'wrongpass');
    await userEvent.click(screen.getByRole('button', { name: /Log in/i }));

    await waitFor(() => {
      expect(api.post).toHaveBeenCalled();
      expect(window.alert).toHaveBeenCalledWith('Login Failed!');
    });
  });
});
